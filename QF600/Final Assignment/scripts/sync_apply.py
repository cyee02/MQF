"""Propagate reviewed changes into 01 / 04 / 05 at their anchors (hand edits elsewhere survive).

    python scripts/sync_apply.py push-numbers [--keys K ...]   # results.json -> num anchors
    python scripts/sync_apply.py push-figures [--ids ID ...]   # figures/ -> fig anchors
    python scripts/sync_apply.py push-names                    # context/09 mapping -> tags, notes, script
    python scripts/sync_apply.py set-text FILE ANCHOR "text"   # one txt:/num: anchor in one file

Every write first copies the target files to .sync/backups/<timestamp>/.
Run sync_check.py afterwards, then sync_check.py --accept once the user agrees.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import office_anchors as oa  # noqa: E402
from sync_check import F, FIGS, RESULTS, presenter_map  # noqa: E402

ROOT = oa.ROOT


def backup(paths):
    dest = ROOT / ".sync" / "backups" / dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    dest.mkdir(parents=True, exist_ok=True)
    for p in paths:
        if p.exists():
            shutil.copy2(p, dest / p.name)
    print(f"backup → {dest.relative_to(ROOT)}")


def results():
    return {k: (v["display"] if isinstance(v, dict) else str(v))
            for k, v in json.loads(RESULTS.read_text()).items()}


def push_numbers(keys):
    res = results()
    keys = keys or list(res)
    backup([F["report"], F["slides"], F["script"]])
    log = []
    for name in ("report", "script"):
        doc = oa.open_docx(F[name])
        if doc is None:
            continue
        for k in keys:
            if f"num_{k}" in oa.docx_anchors(doc) and oa.docx_set_anchor(doc, f"num_{k}", res[k]):
                log.append(f"{F[name].name}: num_{k} = {res[k]}")
        doc.save(F[name])
    prs = oa.open_pptx(F["slides"])
    if prs is not None:
        for k in keys:
            for s, sh in oa.pptx_find(prs, f"num:{k}"):
                oa.pptx_set_text(sh, res[k])
                log.append(f"{F['slides'].name}: num:{k} = {res[k]}")
        prs.save(F["slides"])
    print("\n".join(log) or "no number anchors found")


def push_figures(ids):
    figs = {p.stem: p for p in FIGS.glob("*.png")}
    ids = ids or list(figs)
    backup([F["report"], F["slides"]])
    log = []
    doc = oa.open_docx(F["report"])
    if doc is not None:
        for i in ids:
            if i in figs and oa.docx_replace_figure(doc, i, figs[i]):
                log.append(f"01: fig:{i}")
        doc.save(F["report"])
    prs = oa.open_pptx(F["slides"])
    if prs is not None:
        for i in ids:
            if i in figs and oa.pptx_replace_figure(prs, i, figs[i]):
                log.append(f"04: fig:{i}")
        prs.save(F["slides"])
    print("\n".join(log) or "no figure anchors found")


def short(name: str) -> str:
    """Speaker-tag name: the known short name if listed in context/09, else the full name."""
    shorts = {"Chew Junhong": "Junhong", "Marcus Tan Jun Lin": "Marcus", "Chia Chong Yee": "Chong Yee",
              "Abirame d/o Asohan": "Abirame", "Ramona Chia Ming Li": "Ramona"}
    return shorts.get(name, name)


def push_names():
    pm = presenter_map()
    if not pm:
        print("context/09 still has no confirmed presenter mapping")
        return
    backup([F["slides"], F["script"]])
    prs = oa.open_pptx(F["slides"])
    if prs is not None:
        for s in prs.slides:
            for _, sh in [(s, x) for x in s.shapes if x.name == "tag:speaker"]:
                t = sh.text_frame.text.strip()
                if t in pm:
                    oa.pptx_set_text(sh, short(pm[t]))
            if s.has_notes_slide:
                tf = s.notes_slide.notes_text_frame
                for p in tf.paragraphs:
                    for r in p.runs:
                        for ph, name in pm.items():
                            r.text = re.sub(rf"\b{ph}\b", short(name).upper() if r.text.startswith("[") else short(name),
                                            r.text, flags=re.I)
        prs.save(F["slides"])
    doc = oa.open_docx(F["script"])
    if doc is not None:
        for p in doc.paragraphs:
            for r in p.runs:
                for ph, name in pm.items():
                    if ph in r.text:
                        r.text = r.text.replace(ph, short(name))
        doc.save(F["script"])
    print("presenter names applied:", ", ".join(f"{k} → {short(v)}" for k, v in pm.items()))


def set_text(file_key: str, anchor: str, text: str):
    p = F[file_key]
    backup([p])
    if p.suffix == ".pptx":
        prs = oa.open_pptx(p)
        hits = list(oa.pptx_find(prs, anchor))
        for _, sh in hits:
            oa.pptx_set_text(sh, text)
        prs.save(p)
        print(f"{len(hits)} shape(s) updated")
    else:
        doc = oa.open_docx(p)
        ok = oa.docx_set_anchor(doc, anchor, text)
        doc.save(p)
        print("updated" if ok else f"anchor {anchor} not found")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    n = sub.add_parser("push-numbers")
    n.add_argument("--keys", nargs="*")
    f = sub.add_parser("push-figures")
    f.add_argument("--ids", nargs="*")
    sub.add_parser("push-names")
    t = sub.add_parser("set-text")
    t.add_argument("file", choices=["report", "slides", "script"])
    t.add_argument("anchor")
    t.add_argument("text")
    a = ap.parse_args()
    {"push-numbers": lambda: push_numbers(a.keys), "push-figures": lambda: push_figures(a.ids),
     "push-names": push_names, "set-text": lambda: set_text(a.file, a.anchor, a.text)}[a.cmd]()


if __name__ == "__main__":
    main()
