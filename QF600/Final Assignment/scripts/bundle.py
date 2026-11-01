"""Pack / unpack the team bundle: the gitignored files teammates need.

    python scripts/bundle.py pack
    python scripts/bundle.py unpack [ZIP] [--overwrite PATH ...] [--overwrite-all]

pack    zips course_materials/, reference_paper/, reference_style/QF627_*.ipynb
        and datasets/ into QF600_Final_Group6_bundle_<YYYYMMDD>.zip, with
        bundle_manifest.json (path, sha256, size). Never includes credentials.
unpack  verifies the manifest, refuses unsafe paths, and lists conflicts
        (local files that differ). Conflicting files are only overwritten when
        named with --overwrite or with --overwrite-all. Exit code 2 = conflicts
        were skipped and need a decision.
"""
from __future__ import annotations

import argparse
import datetime as dt
import getpass
import hashlib
import json
import sys
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PREFIX = "QF600_Final_Group6_bundle_"
MANIFEST = "bundle_manifest.json"
INCLUDE = [
    ("course_materials", "**/*"),
    ("reference_paper", "**/*"),
    ("reference_style", "QF627_*.ipynb"),
    ("datasets", "**/*"),
]
NEVER = {"credentials.yaml", ".gitkeep", ".DS_Store"}


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def collect() -> list[Path]:
    files = []
    for folder, pattern in INCLUDE:
        base = ROOT / folder
        if base.exists():
            files += [p for p in base.glob(pattern)
                      if p.is_file() and p.name not in NEVER and not p.name.startswith("~$")]
    return sorted(set(files))


def pack() -> int:
    files = collect()
    out = ROOT / f"{PREFIX}{dt.date.today():%Y%m%d}.zip"
    manifest = {
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "created_by": getpass.getuser(),
        "files": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p),
                   "size": p.stat().st_size} for p in files],
    }
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            z.write(p, p.relative_to(ROOT).as_posix())
        z.writestr(MANIFEST, json.dumps(manifest, indent=2))
    total = sum(f["size"] for f in manifest["files"])
    print(f"packed {len(files)} files ({total / 1e6:.1f} MB raw) -> {out.name} "
          f"({out.stat().st_size / 1e6:.1f} MB)")
    for folder, _ in INCLUDE:
        n = sum(1 for f in manifest["files"] if f["path"].startswith(folder + "/"))
        print(f"  {folder:<18} {n} files")
    return 0


def safe(name: str) -> bool:
    p = PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts and not name.startswith(("/", "\\")) \
        and ":" not in p.parts[0] and p.name not in NEVER


def unpack(zip_path: Path | None, overwrite: set[str], overwrite_all: bool) -> int:
    if zip_path is None:
        found = sorted(ROOT.glob(f"{PREFIX}*.zip"))
        if not found:
            print(f"no {PREFIX}*.zip in {ROOT}")
            return 1
        zip_path = found[-1]
    print(f"unpacking {zip_path.name}")
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        if MANIFEST not in names:
            print("refused: no bundle_manifest.json in zip")
            return 1
        manifest = json.loads(z.read(MANIFEST))
        listed = {f["path"]: f for f in manifest["files"]}
        bad = [n for n in names if n != MANIFEST and (not safe(n) or n not in listed)]
        if bad:
            print("refused: unsafe or unlisted paths:", *bad[:10], sep="\n  ")
            return 1
        new, same, conflicts, written = [], [], [], []
        for path, meta in listed.items():
            data = z.read(path)
            if hashlib.sha256(data).hexdigest() != meta["sha256"]:
                print(f"refused: hash mismatch for {path}")
                return 1
            dest = ROOT / path
            if dest.exists():
                if sha256(dest) == meta["sha256"]:
                    same.append(path)
                    continue
                if not (overwrite_all or path in overwrite):
                    conflicts.append(path)
                    continue
            else:
                new.append(path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            written.append(path)
    print(f"  written {len(written)} (new {len(new)}), unchanged {len(same)}, "
          f"conflicts skipped {len(conflicts)}")
    for c in conflicts:
        print(f"  CONFLICT {c}")
    if conflicts:
        print("re-run with --overwrite <path> ... or --overwrite-all to replace local copies")
        return 2
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pack")
    u = sub.add_parser("unpack")
    u.add_argument("zip", nargs="?", type=Path)
    u.add_argument("--overwrite", nargs="*", default=[])
    u.add_argument("--overwrite-all", action="store_true")
    a = ap.parse_args()
    if a.cmd == "pack":
        return pack()
    return unpack(a.zip, set(a.overwrite), a.overwrite_all)


if __name__ == "__main__":
    sys.exit(main())
