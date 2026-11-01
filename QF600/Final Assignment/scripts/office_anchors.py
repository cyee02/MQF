"""Read and write sync anchors in the project's Word and PowerPoint files.

Anchors are stable IDs that let the sync tools find a number, figure or text
block without regenerating the document, so hand edits elsewhere survive.

Word (.docx)
    num_<key> / txt_<key>  bookmark around the run(s) holding the value
    fig:<fig_id>           alt text (wp:docPr/@descr) of an inline picture

PowerPoint (.pptx)
    num:<key> / txt:<key>  shape name of a text box holding the value
    fig:<fig_id>           shape name of a picture
    tag:speaker            shape name of the speaker tag (top-right corner)
    Notes start with "[NAME · m:ss–m:ss]"; "[CLICK n]" marks animation clicks.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]

NOTE_HEADER = re.compile(r"^\[(?P<name>[^\]·]+?)\s*·\s*(?P<start>\d+:\d{2})\s*[–-]\s*(?P<end>\d+:\d{2})\]")
CLICK = re.compile(r"\[CLICK\s+(\d+)\]")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


def mmss(s: str) -> int:
    m, sec = s.split(":")
    return int(m) * 60 + int(sec)


# ----------------------------------------------------------------- Word ---

def _bookmark_spans(doc):
    """Yield (name, bookmarkStart element, list of w:r elements inside)."""
    body = doc.element.body
    for start in body.iter(qn("w:bookmarkStart")):
        name = start.get(qn("w:name"))
        bid = start.get(qn("w:id"))
        runs, node = [], start.getnext()
        while node is not None:
            if node.tag == qn("w:bookmarkEnd") and node.get(qn("w:id")) == bid:
                break
            if node.tag == qn("w:r"):
                runs.append(node)
            node = node.getnext()
        yield name, start, runs


def _run_text(r) -> str:
    return "".join(t.text or "" for t in r.iter(qn("w:t")))


def docx_anchors(doc) -> dict[str, str]:
    out = {}
    for name, _, runs in _bookmark_spans(doc):
        if name.startswith(("num_", "txt_")):
            out[name] = "".join(_run_text(r) for r in runs)
    return out


def docx_set_anchor(doc, name: str, text: str) -> bool:
    for n, _, runs in _bookmark_spans(doc):
        if n == name and runs:
            ts = list(runs[0].iter(qn("w:t")))
            ts[0].text = text
            for t in ts[1:]:
                t.text = ""
            for r in runs[1:]:
                for t in r.iter(qn("w:t")):
                    t.text = ""
            return True
    return False


_next_bm = [9000]


def docx_add_anchor(paragraph, name: str, text: str):
    """Append a bookmarked run (used by builders when inserting a value)."""
    _next_bm[0] += 1
    bid = str(_next_bm[0])
    start = OxmlElement("w:bookmarkStart")
    start.set(qn("w:id"), bid)
    start.set(qn("w:name"), name)
    end = OxmlElement("w:bookmarkEnd")
    end.set(qn("w:id"), bid)
    paragraph._p.append(start)
    run = paragraph.add_run(text)
    paragraph._p.append(end)
    return run


def docx_figures(doc) -> dict[str, dict]:
    """fig_id -> {hash, rId} for pictures whose alt text is 'fig:<id>'."""
    out = {}
    for inline in doc.element.body.iter(qn("wp:inline")):
        pr = inline.find(qn("wp:docPr"))
        descr = (pr.get("descr") or "") if pr is not None else ""
        if not descr.startswith("fig:"):
            continue
        blip = next(inline.iter(qn("a:blip")), None)
        if blip is None:
            continue
        rid = blip.get(qn("r:embed"))
        part = doc.part.related_parts[rid]
        out[descr[4:]] = {"hash": sha(part.blob), "rId": rid}
    return out


def docx_replace_figure(doc, fig_id: str, png: Path) -> bool:
    figs = docx_figures(doc)
    if fig_id not in figs:
        return False
    doc.part.related_parts[figs[fig_id]["rId"]]._blob = png.read_bytes()
    return True


def docx_sections(doc) -> dict[str, str]:
    """Heading text -> body text under it (for free-text diffs)."""
    from docx.table import Table
    from docx.text.paragraph import Paragraph
    out, cur, buf = {}, "_preamble", []
    for el in doc.element.body.iterchildren():
        if el.tag == qn("w:tbl"):                       # tables count as text of the section they sit in
            t = Table(el, doc)
            buf.extend(" | ".join(c.text for c in row.cells) for row in t.rows)
            continue
        if el.tag != qn("w:p"):
            continue
        p = Paragraph(el, doc)
        if p.style is not None and p.style.name.startswith("Heading"):
            out[cur] = "\n".join(buf).strip()
            cur, buf = p.text.strip(), []
        else:
            buf.append(p.text)
    out[cur] = "\n".join(buf).strip()
    return {k: v for k, v in out.items() if k != "_preamble" or v}


def docx_word_count(doc) -> int:
    return sum(len(p.text.split()) for p in doc.paragraphs)


# ----------------------------------------------------------- PowerPoint ---

def _iter_shapes(shapes):
    for sh in shapes:
        yield sh
        if sh.shape_type == 6:  # group
            yield from _iter_shapes(sh.shapes)


def pptx_slides(prs) -> list[dict]:
    """One dict per slide: title, speaker tag, anchors, figures, notes, clicks."""
    slides = []
    for i, s in enumerate(prs.slides, 1):
        d = {"n": i, "title": "", "speaker": None, "anchors": {}, "figures": {},
             "text": {}, "notes": "", "header": None, "clicks_notes": 0,
             "clicks_anim": s._element.xml.count('nodeType="clickEffect"'),
             "body_words": 0}
        for sh in _iter_shapes(s.shapes):
            name = sh.name or ""
            if name.startswith("fig:") and sh.shape_type == 13:
                d["figures"][name[4:]] = sha(sh.image.blob)
                continue
            if not sh.has_text_frame:
                continue
            txt = sh.text_frame.text
            if name == "tag:speaker":
                d["speaker"] = txt.strip()
            elif name == "title" or (sh.is_placeholder and sh.placeholder_format.type in (1, 3)):
                d["title"] = txt.strip()
            elif name.startswith(("num:", "txt:")):
                d["anchors"][name] = txt
            if name not in ("tag:speaker", "title", "page", "badge", "datanote"):
                d["body_words"] += len(txt.split())
            d["text"][name or f"shape{sh.shape_id}"] = txt
        if s.has_notes_slide:
            notes = s.notes_slide.notes_text_frame.text
            d["notes"] = notes
            m = NOTE_HEADER.match(notes.strip())
            if m:
                d["header"] = {"name": m["name"].strip(), "start": m["start"], "end": m["end"]}
            d["clicks_notes"] = len(CLICK.findall(notes))
        slides.append(d)
    return slides


def pptx_find(prs, name: str):
    for s in prs.slides:
        for sh in _iter_shapes(s.shapes):
            if sh.name == name:
                yield s, sh


def pptx_set_text(shape, text: str):
    """Replace text but keep the first run's formatting."""
    tf = shape.text_frame
    p0 = tf.paragraphs[0]
    if p0.runs:
        p0.runs[0].text = text
        for r in p0.runs[1:]:
            r.text = ""
    else:
        p0.text = text
    for p in tf.paragraphs[1:]:
        for r in p.runs:
            r.text = ""


def pptx_replace_figure(prs, fig_id: str, png: Path) -> int:
    n = 0
    for _, sh in pptx_find(prs, f"fig:{fig_id}"):
        if sh.shape_type == 13:
            rid = sh._element.blipFill.blip.rEmbed
            sh.part.related_part(rid)._blob = png.read_bytes()
            n += 1
    return n


# ------------------------------------------------------------- Script docx ---

SCRIPT_HEAD = re.compile(r"^Slide\s+(\d+)\s*·\s*(.*)$")
SCRIPT_META = re.compile(r"Speaker:\s*(?P<name>.+?)\s*·\s*Start\s*(?P<start>\d+:\d{2})\s*·\s*End\s*(?P<end>\d+:\d{2})")


def script_slides(doc) -> list[dict]:
    """Parse 05 - Presentation Script.docx into one dict per slide."""
    out, cur = [], None
    for p in doc.paragraphs:
        t = p.text.strip()
        m = SCRIPT_HEAD.match(t)
        if p.style.name.startswith("Heading"):
            if m:
                cur = {"n": int(m[1]), "title": m[2].strip(), "speaker": None,
                       "start": None, "end": None, "text": [], "clicks": 0}
                out.append(cur)
            else:
                cur = None          # e.g. a "Presenter 2" group heading: not part of any slide
            continue
        if cur is None:
            continue
        mm = SCRIPT_META.search(t)
        if mm and cur["speaker"] is None:
            cur.update(speaker=mm["name"], start=mm["start"], end=mm["end"])
            continue
        cur["text"].append(t)
        cur["clicks"] += len(CLICK.findall(t))
    for c in out:
        c["text"] = "\n".join(x for x in c["text"] if x)
    return out


def open_docx(path: Path):
    return Document(str(path)) if path.exists() else None


def open_pptx(path: Path):
    return Presentation(str(path)) if path.exists() else None
