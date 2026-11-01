"""Keep datasets/, .sync/datasets.json, 02 - Dataset Metadata and context/06 in step.

    python scripts/data_sync.py                 # scan + report (no writes)
    python scripts/data_sync.py --write         # also write registry, 02 and context/06 status
    python scripts/data_sync.py --set FILE --provider P --source S --url U \
        --description D --method script|manual --key fred_key --write

The scan profiles every file in datasets/ (rows, columns, dtypes, date range,
inferred frequency, missing values) and compares it with the last registry.
Source/description come from context/06 when the filename is listed there;
otherwise the file is flagged `needs_meta` and the skill asks the user.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "datasets"
REG = ROOT / ".sync" / "datasets.json"
META_MD = ROOT / "02 - Dataset Metadata Group 6.md"
CTX06 = ROOT / "context" / "06_data_sources.md"
SKIP = {".gitkeep", ".DS_Store"}
META_FIELDS = ("provider", "source", "url", "description", "method", "key")
BEGIN, END = "<!-- AUTO:BEGIN data_sync -->", "<!-- AUTO:END data_sync -->"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def infer_freq(dates: pd.Series) -> str:
    d = pd.to_datetime(dates, errors="coerce").dropna().drop_duplicates().sort_values()
    if len(d) < 3:
        return "unknown"
    gap = d.diff().dt.days.median()
    for lim, name in [(1.5, "daily"), (8, "weekly"), (32, "monthly"), (95, "quarterly"), (370, "annual")]:
        if gap <= lim:
            return name
    return f"~{gap:.0f} days"


def find_date_col(df: pd.DataFrame) -> str | None:
    for c in list(df.columns)[:3]:
        s = df[c]
        if pd.api.types.is_datetime64_any_dtype(s):
            return c
        if s.dtype == object or pd.api.types.is_integer_dtype(s):
            sample = s.dropna().astype(str).head(200)
            if sample.empty:
                continue
            if pd.api.types.is_integer_dtype(s) and not sample.str.fullmatch(r"\d{4}(\d{2})?").all():
                continue
            fmt = "%Y%m" if sample.str.fullmatch(r"\d{6}").all() else ("%Y" if sample.str.fullmatch(r"\d{4}").all() else None)
            parsed = pd.to_datetime(sample, format=fmt, errors="coerce")
            if parsed.notna().mean() > 0.9:
                return c
    return None


def profile(p: Path) -> dict:
    info = {"file": p.name, "sha256": sha256(p), "size": p.stat().st_size,
            "profiled_at": dt.datetime.now().isoformat(timespec="seconds")}
    try:
        if p.suffix.lower() in (".csv", ".txt"):
            df = pd.read_csv(p)
            sheets = {"": df}
        elif p.suffix.lower() in (".xls", ".xlsx"):
            sheets = pd.read_excel(p, sheet_name=None)
        elif p.suffix.lower() == ".parquet":
            sheets = {"": pd.read_parquet(p)}
        else:
            info["note"] = "not profiled (unsupported type)"
            return info
    except Exception as e:  # noqa: BLE001 - report, don't crash the sync
        info["note"] = f"could not read: {e}"
        return info

    info["sheets"] = []
    for name, df in sheets.items():
        df = df.dropna(how="all").dropna(axis=1, how="all")
        sh = {"sheet": name, "rows": int(len(df)), "n_columns": int(df.shape[1]),
              "columns": [{"name": str(c), "dtype": str(df[c].dtype),
                           "missing": int(df[c].isna().sum())} for c in df.columns[:60]]}
        dc = find_date_col(df)
        if dc is not None:
            s = df[dc].dropna().astype(str)
            fmt = "%Y%m" if s.str.fullmatch(r"\d{6}").all() else ("%Y" if s.str.fullmatch(r"\d{4}").all() else None)
            d = pd.to_datetime(s, format=fmt, errors="coerce").dropna()
            if len(d):
                sh.update(date_column=str(dc), start=str(d.min().date()), end=str(d.max().date()),
                          frequency=infer_freq(d))
        info["sheets"].append(sh)
    return info


def ctx06_rows() -> dict[str, dict]:
    """expected filename -> registry row from context/06."""
    rows = {}
    if not CTX06.exists():
        return rows
    for line in CTX06.read_text().splitlines():
        if not re.match(r"\|\s*D\d+", line):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 10:
            continue
        fname = re.findall(r"`([^`]+)`", c[8])
        if fname:
            rows[fname[0]] = {"id": c[0], "description": c[1], "provider": c[2],
                              "url": c[3].replace("`", ""), "frequency_registry": c[4],
                              "period_needed": c[5], "method": c[6],
                              "key": "" if c[7] in ("—", "-") else c[7].replace("`", ""),
                              "source": f"{c[2]}: {c[3].replace('`', '')}"}
    return rows


def update_ctx06_status(files: set[str]):
    if not CTX06.exists():
        return
    out = []
    for line in CTX06.read_text().splitlines():
        if re.match(r"\|\s*D\d+", line):
            c = line.strip().strip("|").split("|")
            fname = re.findall(r"`([^`]+)`", c[8]) if len(c) >= 10 else []
            if fname and fname[0] in files and "downloaded" not in c[9]:
                c[9] = " downloaded "
                line = "|" + "|".join(c) + "|"
        out.append(line)
    CTX06.write_text("\n".join(out) + "\n")


def render_md(reg: dict) -> str:
    files = reg.get("files", {})
    lines = [BEGIN, "", f"_Last synced: {reg.get('synced_at', '—')} · {len(files)} dataset(s)._", ""]
    if not files:
        lines += ["No datasets yet. Add files to `datasets/` and run `qf600-data-sync`.", "", END]
        return "\n".join(lines)
    lines += ["## Summary", "", "| # | File | Description | Source | Frequency | Period | Rows | Columns |",
              "|---|------|-------------|--------|-----------|--------|------|---------|"]
    for i, (fn, f) in enumerate(sorted(files.items()), 1):
        sh = (f.get("sheets") or [{}])[0]
        period = f"{sh.get('start', '—')} → {sh.get('end', '—')}"
        lines.append(f"| {i} | `{fn}` | {f.get('description', '—')} | {f.get('provider', '—')} | "
                     f"{sh.get('frequency', f.get('frequency_registry', '—'))} | {period} | "
                     f"{sh.get('rows', '—')} | {sh.get('n_columns', '—')} |")
    lines.append("")
    for i, (fn, f) in enumerate(sorted(files.items()), 1):
        lines += [f"## {i}. `{fn}`", "",
                  f"- **Description:** {f.get('description', '—')}",
                  f"- **Provider:** {f.get('provider', '—')}",
                  f"- **Source / link:** {f.get('url') or f.get('source', '—')}",
                  f"- **How obtained:** {f.get('method', '—')}"
                  + (f" (API key `{f['key']}` in `credentials.yaml`)" if f.get("key") else ""),
                  f"- **File size:** {f.get('size', 0) / 1e3:,.0f} KB · sha256 `{f.get('sha256', '')[:12]}`"]
        if f.get("note"):
            lines.append(f"- **Note:** {f['note']}")
        for sh in f.get("sheets", []):
            label = f" (sheet `{sh['sheet']}`)" if sh.get("sheet") else ""
            lines += ["", f"**Shape{label}:** {sh['rows']:,} rows × {sh['n_columns']} columns"
                      + (f" · {sh.get('frequency')} · {sh.get('start')} → {sh.get('end')}" if sh.get("start") else ""),
                      "", "| Column | Type | Missing |", "|--------|------|---------|"]
            lines += [f"| {c['name']} | {c['dtype']} | {c['missing']} |" for c in sh["columns"]]
            if sh["n_columns"] > len(sh["columns"]):
                lines.append(f"| … {sh['n_columns'] - len(sh['columns'])} more | | |")
        lines.append("")
    lines.append(END)
    return "\n".join(lines)


HEADER = """# Dataset Metadata · Group 6

QF600 Asset Pricing · Group Project · Deliverable 02

Datasets used by `03 - execution_script_group_6.ipynb`. Script-downloaded files are rebuilt by notebook §1; manually obtained files are listed with their download link. The same information appears in Annex A of the Project Report.

"""


def write_md(reg: dict):
    block = render_md(reg)
    if META_MD.exists():
        text = META_MD.read_text()
        if BEGIN in text and END in text:
            pre, rest = text.split(BEGIN, 1)
            post = rest.split(END, 1)[1]
            META_MD.write_text(pre + block + post)
            return
        META_MD.write_text(text.rstrip() + "\n\n" + block + "\n")
    else:
        META_MD.write_text(HEADER + block + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--set", metavar="FILE")
    for f in META_FIELDS:
        ap.add_argument(f"--{f}")
    a = ap.parse_args()

    reg = json.loads(REG.read_text()) if REG.exists() else {"files": {}}
    old = reg.get("files", {})
    ctx = ctx06_rows()
    current = {p.name: p for p in sorted(DATA.glob("*")) if p.is_file() and p.name not in SKIP}

    report = {"new": [], "changed": [], "removed": [], "unchanged": [], "needs_meta": []}
    files = {}
    for name, p in current.items():
        prev = old.get(name)
        h = sha256(p)
        if prev and prev.get("sha256") == h:
            entry = prev
            report["unchanged"].append(name)
        else:
            entry = {**{k: v for k, v in (prev or {}).items() if k in META_FIELDS}, **profile(p)}
            report["changed" if prev else "new"].append(name)
        for k, v in ctx.get(name, {}).items():
            entry.setdefault(k, v)
        files[name] = entry
    report["removed"] = sorted(set(old) - set(current))

    if a.set:
        if a.set not in files:
            print(f"no such dataset: {a.set}")
            return 1
        files[a.set].update({f: getattr(a, f) for f in META_FIELDS if getattr(a, f)})

    for name, e in files.items():
        missing = [f for f in ("provider", "description", "method") if not e.get(f)]
        if missing:
            report["needs_meta"].append({"file": name, "missing": missing})
        if e.get("key"):
            report.setdefault("keys", sorted(set(report.get("keys", [])) | {e["key"]}))

    print(json.dumps(report, indent=2))
    if a.write:
        reg = {"synced_at": dt.datetime.now().isoformat(timespec="seconds"), "files": files}
        REG.parent.mkdir(exist_ok=True)
        REG.write_text(json.dumps(reg, indent=2))
        write_md(reg)
        update_ctx06_status(set(files))
        print(f"wrote {REG.relative_to(ROOT)}, {META_MD.name}, context/06 status")
    return 0


if __name__ == "__main__":
    sys.exit(main())
