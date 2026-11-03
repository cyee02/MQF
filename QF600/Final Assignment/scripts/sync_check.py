"""Detect changes across deliverables 01–05 and check they are aligned.

    python scripts/sync_check.py            # diff vs snapshot + alignment checks (no writes)
    python scripts/sync_check.py --json     # same, machine-readable
    python scripts/sync_check.py --accept   # save the current state as the agreed snapshot
    python scripts/sync_check.py --execute  # also run the notebook top to bottom (check C10)

Exit codes: 0 = no pending changes and no failed checks; 1 = a check failed;
3 = changes since the snapshot are waiting for review (checks may still pass).
Nothing here edits a deliverable. Propagation is done with sync_apply.py
after the user has reviewed the diff (see the qf600-sync-check skill).
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import office_anchors as oa  # noqa: E402

ROOT = oa.ROOT
F = {
    "report": ROOT / "01 - Project Report Group 6.docx",
    "metadata": ROOT / "02 - Dataset Metadata Group 6.md",
    "notebook": ROOT / "03 - execution_script_group_6.ipynb",
    "slides": ROOT / "04 - Presentation Slides Group 6.pptx",
    "script": ROOT / "05 - Presentation Script.docx",
}
RESULTS = ROOT / "outputs" / "results.json"
FIGS = ROOT / "figures"
SNAP = ROOT / ".sync" / "snapshot.json"
DSREG = ROOT / ".sync" / "datasets.json"
README = ROOT / "README.md"
CREDS_EX = ROOT / "credentials.example.yaml"
REQS = ROOT / "requirements.txt"
SKILLS = ROOT / ".claude" / "skills"
TALK_LIMIT = 16 * 60
WORDS_PER_SLIDE = 40
EXEC_SUMMARY_WORDS = 450
PKG = {"yaml": "pyyaml", "docx": "python-docx", "pptx": "python-pptx", "lets_plot": "lets-plot",
       "sklearn": "scikit-learn", "PIL": "pillow", "fredapi": "fredapi", "bs4": "beautifulsoup4",
       "IPython": "ipykernel", "dateutil": "python-dateutil"}


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()[:16]


# ------------------------------------------------------------- collect ----

def notebook_code() -> str:
    if not F["notebook"].exists():
        return ""
    nb = json.loads(F["notebook"].read_text())
    return "\n".join("".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code")


def setup_state() -> dict:
    code = notebook_code()
    scripts = {p.name: p.read_text() for p in (ROOT / "scripts").glob("*.py")}
    all_code = code + "\n" + "\n".join(scripts.values())
    keys = sorted(set(re.findall(r"creds(?:\[\s*|\.get\(\s*)[\"'](\w+)[\"']", all_code)))
    ex_keys = sorted(re.findall(r"^(\w+)\s*:", CREDS_EX.read_text(), re.M)) if CREDS_EX.exists() else []
    readme = README.read_text() if README.exists() else ""
    local = {p.stem for p in (ROOT / "scripts").glob("*.py")}
    imports = set()
    for line in all_code.splitlines():
        m = re.match(r"\s*(?:from\s+(\w+)[\w.]*\s+import|import\s+(\w+))", line)
        if m:
            imports.add(m[1] or m[2])
    third = sorted(i for i in imports if i not in sys.stdlib_module_names and i not in local and i != "__future__")
    reqs = sorted(re.split(r"[<>=\[ ;]", l.strip())[0].lower()
                  for l in REQS.read_text().splitlines() if l.strip() and not l.startswith("#")) if REQS.exists() else []
    skills = sorted(p.name for p in SKILLS.glob("qf600-*") if (p / "SKILL.md").exists())
    secrets = []
    pats = [r"[\"'][0-9a-f]{32}[\"']",
            r"(?i)[\"']?(api_?key|password|passwd|token|secret)[\"']?\s*[:=]\s*[\"'][^\"'{}<>\s]{6,}[\"']"]
    for src, text in [("notebook", code)] + list(scripts.items()):
        for pat in pats:
            for m in re.finditer(pat, text):
                if re.search(r"(?i)example|your|placeholder|xxx|<", m.group(0)):
                    continue
                secrets.append({"where": src, "match": m.group(0)[:40]})
    return {"creds_keys": keys, "example_keys": ex_keys,
            "readme_keys": [k for k in keys if k in readme],
            "imports": third, "requirements": reqs, "skills": skills,
            "readme_skills": [s for s in skills if s in readme], "secrets": secrets}


def collect() -> dict:
    st = {"results": {}, "figures": {}, "report": None, "slides": None, "script": None,
          "datasets": {}, "metadata_files": [], "setup": setup_state()}
    if RESULTS.exists():
        st["results"] = {k: (v.get("display") if isinstance(v, dict) else str(v))
                         for k, v in json.loads(RESULTS.read_text()).items()}
    for p in sorted(FIGS.glob("*")):
        if p.suffix.lower() in (".png", ".svg", ".jpg"):
            st["figures"][p.stem] = h(p.read_bytes())
    doc = oa.open_docx(F["report"])
    if doc is not None:
        st["report"] = {"anchors": oa.docx_anchors(doc),
                        "figures": {k: v["hash"] for k, v in oa.docx_figures(doc).items()},
                        "sections": oa.docx_sections(doc),
                        "headings": [p.text.strip() for p in doc.paragraphs
                                     if p.style is not None and p.style.name.startswith("Heading")],
                        "words": oa.docx_word_count(doc)}
    prs = oa.open_pptx(F["slides"])
    if prs is not None:
        st["slides"] = oa.pptx_slides(prs)
    sdoc = oa.open_docx(F["script"])
    if sdoc is not None:
        st["script"] = {"slides": oa.script_slides(sdoc), "anchors": oa.docx_anchors(sdoc)}
    for p in sorted((ROOT / "datasets").glob("*")):
        if p.is_file() and p.name not in (".gitkeep", ".DS_Store"):
            st["datasets"][p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
    if F["metadata"].exists():
        st["metadata_files"] = sorted(set(re.findall(r"^## \d+\. `([^`]+)`", F["metadata"].read_text(), re.M)))
    return st


# ---------------------------------------------------------------- diff ----

def _txt(a, b, n=3):
    return "\n".join(difflib.unified_diff((a or "").splitlines(), (b or "").splitlines(),
                                          "before", "after", n=0, lineterm=""))[:1500]


def diff(old: dict, new: dict) -> list[dict]:
    ch = []

    def add(file, where, kind, before=None, after=None):
        ch.append({"file": file, "where": where, "kind": kind, "before": before, "after": after})

    def dict_diff(file, label, a, b):
        a, b = a or {}, b or {}
        for k in sorted(set(a) | set(b)):
            if a.get(k) != b.get(k):
                kind = "added" if k not in a else "removed" if k not in b else "changed"
                add(file, f"{label} {k}", kind, a.get(k), b.get(k))

    dict_diff("03 notebook → outputs/results.json", "number", old.get("results"), new.get("results"))
    dict_diff("03 notebook → figures/", "figure", old.get("figures"), new.get("figures"))
    dict_diff("datasets/", "dataset", {k: v[:12] for k, v in old.get("datasets", {}).items()},
              {k: v[:12] for k, v in new.get("datasets", {}).items()})

    o, n = old.get("report") or {}, new.get("report") or {}
    if bool(o) != bool(n):
        add("01 report", "file", "created" if n else "deleted")
    dict_diff("01 report", "anchor", o.get("anchors"), n.get("anchors"))
    dict_diff("01 report", "figure", o.get("figures"), n.get("figures"))
    os_, ns_ = o.get("sections", {}), n.get("sections", {})
    for k in sorted(set(os_) | set(ns_)):
        if os_.get(k) != ns_.get(k):
            add("01 report", f"section '{k}'", "text", None, _txt(os_.get(k), ns_.get(k)))

    osl, nsl = old.get("slides") or [], new.get("slides") or []
    if [s["title"] for s in osl] != [s["title"] for s in nsl]:
        add("04 slides", "slide list", "order/titles", [s["title"] for s in osl], [s["title"] for s in nsl])
    for a, b in zip(osl, nsl):
        for fld in ("speaker", "header", "clicks_anim", "clicks_notes"):
            if a.get(fld) != b.get(fld):
                add("04 slides", f"slide {b['n']} {fld}", "changed", a.get(fld), b.get(fld))
        dict_diff("04 slides", f"slide {b['n']} anchor", a.get("anchors"), b.get("anchors"))
        dict_diff("04 slides", f"slide {b['n']} figure", a.get("figures"), b.get("figures"))
        for k in sorted(set(a["text"]) | set(b["text"])):
            if k.startswith(("num:", "tag:")):
                continue
            if a["text"].get(k) != b["text"].get(k):
                add("04 slides", f"slide {b['n']} text '{k}'", "text", a["text"].get(k), b["text"].get(k))
        if a.get("notes") != b.get("notes"):
            add("04 slides", f"slide {b['n']} notes", "text", None, _txt(a.get("notes"), b.get("notes")))

    osc, nsc = (old.get("script") or {}).get("slides", []), (new.get("script") or {}).get("slides", [])
    if [s["title"] for s in osc] != [s["title"] for s in nsc]:
        add("05 script", "slide list", "order/titles", [s["title"] for s in osc], [s["title"] for s in nsc])
    for a, b in zip(osc, nsc):
        for fld in ("speaker", "start", "end", "clicks"):
            if a.get(fld) != b.get(fld):
                add("05 script", f"slide {b['n']} {fld}", "changed", a.get(fld), b.get(fld))
        if a.get("text") != b.get("text"):
            add("05 script", f"slide {b['n']} script", "text", None, _txt(a.get("text"), b.get("text")))

    for fld in ("creds_keys", "imports", "skills"):
        a, b = old.get("setup", {}).get(fld, []), new["setup"].get(fld, [])
        if a != b:
            add("set-up (README / credentials / requirements)", fld, "changed",
                sorted(set(a) - set(b)) and {"removed": sorted(set(a) - set(b))},
                sorted(set(b) - set(a)) and {"added": sorted(set(b) - set(a))})
    return ch


# -------------------------------------------------------------- checks ----

def presenter_map() -> dict[str, str]:
    p = ROOT / "context" / "09_group.md"
    out = {}
    for m in re.finditer(r"^\|\s*(Presenter \d)\s*\|\s*([^|]+?)\s*\|", p.read_text(), re.M):
        if "TBC" not in m[2]:
            out[m[1]] = m[2]
    return out


def page_estimate(doc_path: Path) -> tuple[int | None, str]:
    soffice = shutil.which("soffice") or "/Applications/LibreOffice.app/Contents/MacOS/soffice"
    if Path(soffice).exists():
        with tempfile.TemporaryDirectory() as td:
            subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", td, str(doc_path)],
                           capture_output=True, timeout=180)
            pdf = next(Path(td).glob("*.pdf"), None)
            if pdf and shutil.which("pdfinfo"):
                out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
                m = re.search(r"Pages:\s+(\d+)", out)
                if m:
                    return int(m[1]), "total pages via LibreOffice (incl. cover, exec summary, annex)"
    return None, "LibreOffice not found: page count not measured"


def checks(st: dict, execute: bool = False) -> list[dict]:
    out = []

    def res(cid, status, detail):
        out.append({"id": cid, "status": status, "detail": detail})

    rep, sl, sc = st["report"], st["slides"], st["script"]
    results = st["results"]

    # C1 numbers
    bad, n = [], 0
    for src, anchors, prefix in [("01", (rep or {}).get("anchors", {}), "num_"),
                                 ("05", (sc or {}).get("anchors", {}), "num_")]:
        for k, v in anchors.items():
            if k.startswith(prefix):
                n += 1
                key = k[len(prefix):]
                if key not in results:
                    bad.append(f"{src}: {k} has no result '{key}'")
                elif v.strip() != results[key]:
                    bad.append(f"{src}: {k} = '{v.strip()}' but results = '{results[key]}'")
    for s in sl or []:
        for k, v in s["anchors"].items():
            if k.startswith("num:"):
                n += 1
                key = k[4:]
                if key not in results:
                    bad.append(f"04 slide {s['n']}: {k} has no result '{key}'")
                elif v.strip() != results[key]:
                    bad.append(f"04 slide {s['n']}: {k} = '{v.strip()}' but results = '{results[key]}'")
    res("C1 numbers match notebook", "fail" if bad else ("pass" if n else "skip"),
        bad or f"{n} number anchors checked")

    # C2 figures
    bad, n = [], 0
    figs = st["figures"]
    for src, fd in [("01", (rep or {}).get("figures", {}))] + \
                   [(f"04 slide {s['n']}", s["figures"]) for s in (sl or [])]:
        for fid, hh in fd.items():
            n += 1
            if fid not in figs:
                bad.append(f"{src}: fig:{fid} not in figures/")
            elif figs[fid] != hh:
                bad.append(f"{src}: fig:{fid} differs from figures/{fid}")
    res("C2 figures match notebook", "fail" if bad else ("pass" if n else "skip"),
        bad or f"{n} figure anchors checked")

    # C3 / C4 / C5 slides vs script
    if sl is None or sc is None:
        for c in ("C3 slides = script (titles, order, speakers)", "C4 timings", "C5 animation clicks"):
            res(c, "skip", "04 and/or 05 not created yet")
    else:
        ss = sc["slides"]
        bad = []
        if len(sl) != len(ss):
            bad.append(f"04 has {len(sl)} slides, 05 has {len(ss)}")
        for a, b in zip(sl, ss):
            if a["title"] != b["title"]:
                bad.append(f"slide {a['n']}: title '{a['title']}' vs script '{b['title']}'")
            if (a["speaker"] or "").lower() != (b["speaker"] or "").lower():
                bad.append(f"slide {a['n']}: tag '{a['speaker']}' vs script '{b['speaker']}'")
            hd = a.get("header") or a.get("header_untimed") or {}
            if hd and hd["name"].lower() != (a["speaker"] or "").lower():
                bad.append(f"slide {a['n']}: notes header '{hd['name']}' vs tag '{a['speaker']}'")
        res("C3 slides = script (titles, order, speakers)", "fail" if bad else "pass", bad or "aligned")

        bad, prev_end, end = [], 0, 0
        for a, b in zip(sl, ss):
            if a.get("untimed"):                         # divider, hidden or backup: no speaking time
                if b.get("start"):
                    bad.append(f"slide {a['n']}: {a['untimed']} slide but script gives times")
                continue
            hd = a.get("header")
            if not hd:
                bad.append(f"slide {a['n']}: notes missing '[NAME · m:ss–m:ss]' header")
                continue
            st_, end = oa.mmss(hd["start"]), oa.mmss(hd["end"])
            if st_ != prev_end:
                bad.append(f"slide {a['n']}: starts {hd['start']} but previous ended {prev_end // 60}:{prev_end % 60:02d}")
            if end <= st_:
                bad.append(f"slide {a['n']}: end {hd['end']} not after start {hd['start']}")
            if (b["start"], b["end"]) != (hd["start"], hd["end"]):
                bad.append(f"slide {a['n']}: notes {hd['start']}–{hd['end']} vs script {b['start']}–{b['end']}")
            prev_end = end
        if end > TALK_LIMIT:
            bad.append(f"talk ends {end // 60}:{end % 60:02d} > 16:00 limit (R4.1)")
        res("C4 timings", "fail" if bad else "pass", bad or f"talk length {end // 60}:{end % 60:02d}")

        bad = []
        for a, b in zip(sl, ss):
            if a["clicks_anim"] != a["clicks_notes"]:
                bad.append(f"slide {a['n']}: {a['clicks_anim']} animations vs {a['clicks_notes']} [CLICK] in notes")
            if a["clicks_notes"] != b["clicks"]:
                bad.append(f"slide {a['n']}: {a['clicks_notes']} [CLICK] in notes vs {b['clicks']} in script")
        res("C5 animation clicks", "fail" if bad else "pass", bad or "aligned")

    # C6 datasets
    ds = set(st["datasets"])
    md = set(st["metadata_files"])
    bad = []
    if ds != md:
        bad.append(f"datasets/ vs 02: missing in 02 {sorted(ds - md)}, extra in 02 {sorted(md - ds)}")
    if rep is not None:
        annex = next((v for k, v in rep["sections"].items() if k.lower().startswith("annex a")), None)
        if annex is None:
            bad.append("01: no 'Annex A' section")
        else:
            miss = [d for d in ds if d not in annex]
            if miss:
                bad.append(f"01 Annex A does not list {miss}")
    reg = json.loads(DSREG.read_text()).get("files", {}) if DSREG.exists() else {}
    stale = [d for d in ds if reg.get(d, {}).get("sha256") != st["datasets"][d]]
    if stale:
        bad.append(f"run qf600-data-sync: registry out of date for {stale}")
    res("C6 datasets = 02 = Annex A", "fail" if bad else ("pass" if ds else "skip"),
        bad or (f"{len(ds)} datasets aligned" if ds else "no datasets yet"))

    # C7 guideline
    bad, warn = [], []
    for k, p in F.items():
        if not p.exists():
            warn.append(f"R1.5 {p.name} not created yet")
    if rep is not None:
        pages, how = page_estimate(F["report"])
        body = sum(len(v.split()) for k, v in rep["sections"].items()
                   if not re.match(r"(?i)(executive summary|annex|appendix|references)", k))
        est = round(body / 450 + len(rep["figures"]) * 0.4)
        line = f"R2.1 body ≈ {est} pages (word/figure estimate)" + (f"; {pages} {how}" if pages else f"; {how}")
        (bad if est > 20 else warn).append(line)
        es = next((v for k, v in rep["sections"].items() if k.lower().startswith("executive summary")), None)
        if es is None:
            bad.append("R2.2 no 'Executive Summary' section")
        elif len(es.split()) > EXEC_SUMMARY_WORDS:
            bad.append(f"R2.2 executive summary {len(es.split())} words > {EXEC_SUMMARY_WORDS} (≈ 1 page)")
    if sl is not None:
        notag = [s["n"] for s in sl if not s["speaker"]]
        if notag:
            bad.append(f"R3.3 slides without speaker tag: {notag}")
        speakers = {(s["speaker"] or "").lower() for s in sl}
        pm = presenter_map()
        expected = [pm.get(f"Presenter {i}", f"Presenter {i}").lower() for i in range(1, 6)]
        missing = [e for e in expected if not any(e in sp or sp in e for sp in speakers if sp)]
        if missing:
            bad.append(f"R3.2 presenters with no slide: {missing}")
        if not any(s["title"].lower().startswith("annex") for s in sl):
            bad.append("R3.4 no Annex slide with key visuals")
        wordy = [f"{s['n']} ({s['body_words']}w)" for s in sl if s["body_words"] > WORDS_PER_SLIDE]
        if wordy:
            warn.append(f"slides over {WORDS_PER_SLIDE} words: {wordy}")
        if pm:
            left = [s["n"] for s in sl if re.search(r"Presenter \d", (s["speaker"] or "") + s["notes"], re.I)]
            if left:
                bad.append(f"presenter mapping confirmed but placeholders remain on slides {left} (run sync_apply.py push-names)")
    res("C7 guideline checklist (context/01)", "fail" if bad else ("warn" if warn else "pass"), bad + warn or "all met")

    # C8 Prof Liu coverage
    if rep is None or sl is None:
        res("C8 Prof Liu points covered (context/10)", "skip", "01 and/or 04 not created yet")
    else:
        bad = []
        cov = (ROOT / "context" / "10_prof_feedback.md").read_text().split("## Coverage map", 1)[-1]
        nums = [h_.split()[0].rstrip(".") for h_ in rep["headings"] if h_[:1].isdigit()]
        for row in re.finditer(r"^\|\s*(\d+)\s[^|]*\|[^|]*\|[^|]*\|\s*([^|]*)\|\s*([^|]*)\|", cov, re.M):
            secs = re.findall(r"\d+", row[2])
            slides_ = [int(x) for x in re.findall(r"\d+", row[3])]
            if not any(s in nums for s in secs):
                bad.append(f"point {row[1]}: report section {row[2].strip()} not found")
            if not any(1 <= x <= len(sl) for x in slides_):
                bad.append(f"point {row[1]}: slide {row[3].strip()} not in deck")
        res("C8 Prof Liu points covered (context/10)", "fail" if bad else "pass", bad or "all 12 mapped")

    # C9 set-up
    su = st["setup"]
    bad = []
    for k in su["creds_keys"]:
        if k not in su["example_keys"]:
            bad.append(f"credential '{k}' used in code but not in credentials.example.yaml")
        if k not in su["readme_keys"]:
            bad.append(f"credential '{k}' used in code but not explained in README step 8")
    for k in su["example_keys"]:
        if k not in su["creds_keys"]:
            bad.append(f"credentials.example.yaml has '{k}' but no code uses it")
    for imp in su["imports"]:
        pkg = PKG.get(imp, imp).lower()
        if pkg not in su["requirements"]:
            bad.append(f"import '{imp}' → add '{pkg}' to requirements.txt")
    for s in su["skills"]:
        if s not in su["readme_skills"]:
            bad.append(f"skill '{s}' not listed in README step 10")
    for s in su["secrets"]:
        bad.append(f"possible hard-coded secret in {s['where']}: {s['match']}…")
    res("C9 set-up in sync (README, credentials, requirements, no secrets)", "fail" if bad else "pass",
        bad or "aligned")

    # C10 notebook runs
    if execute and F["notebook"].exists():
        py = ROOT / ".venv" / "bin" / "python"
        r = subprocess.run([str(py if py.exists() else sys.executable), "-m", "nbconvert", "--to", "notebook",
                            "--execute", "--output", str(Path(tempfile.gettempdir()) / "qf600_exec.ipynb"),
                            str(F["notebook"])], capture_output=True, text=True, cwd=ROOT, timeout=3600)
        res("C10 notebook executes", "pass" if r.returncode == 0 else "fail",
            "ran top to bottom" if r.returncode == 0 else r.stderr[-1500:])
    else:
        res("C10 notebook executes", "skip", "run with --execute")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--accept", action="store_true")
    ap.add_argument("--execute", action="store_true")
    a = ap.parse_args()

    st = collect()
    snap = json.loads(SNAP.read_text()) if SNAP.exists() else None
    changes = diff(snap, st) if snap else []
    cks = checks(st, a.execute)

    if a.accept:
        SNAP.parent.mkdir(exist_ok=True)
        SNAP.write_text(json.dumps(st, indent=1, ensure_ascii=False, default=str))
        print(f"snapshot saved: {SNAP.relative_to(ROOT)}")
        return 0

    if a.json:
        print(json.dumps({"snapshot": bool(snap), "changes": changes, "checks": cks},
                         indent=1, ensure_ascii=False, default=str))
    else:
        print("== Changes since last sync" + ("" if snap else " (no snapshot yet: run --accept once agreed)"))
        if not changes:
            print("  none")
        for c in changes:
            print(f"- [{c['file']}] {c['where']}: {c['kind']}")
            if c["kind"] == "text":
                print("    " + (c["after"] or "").replace("\n", "\n    "))
            elif c["before"] is not None or c["after"] is not None:
                print(f"    {c['before']!r} → {c['after']!r}")
        print("\n== Alignment checks")
        for c in cks:
            mark = {"pass": "✔", "fail": "✘", "warn": "!", "skip": "·"}[c["status"]]
            print(f"{mark} {c['id']}: {c['status']}")
            for d in (c["detail"] if isinstance(c["detail"], list) else [c["detail"]]):
                print(f"    {d}")
    if any(c["status"] == "fail" for c in cks):
        return 1
    return 3 if changes else 0


if __name__ == "__main__":
    sys.exit(main())
