---
name: qf600-bundle
description: QF600 final project only. Pack or unpack the Group 6 team bundle, a zip of the gitignored files teammates need (course_materials/, reference_paper/, reference_style/QF627 notebooks, datasets/). Use when the user says "pack the team bundle", "make a zip for my teammates", "unpack the team bundle", or a QF600_Final_Group6_bundle_*.zip appears in QF600/Final Assignment. Never includes credentials. Not for QF620.
---

# QF600 team bundle

Scope: `QF600/Final Assignment/`. Python: `.venv/bin/python` (Windows `.venv\Scripts\python`).

## Pack
1. Check that no Word/PowerPoint lock files (`~$*`) are inside the bundled folders, and that `datasets/` has what teammates need (`python scripts/data_sync.py` shows the list).
2. `python scripts/bundle.py pack` → `QF600_Final_Group6_bundle_<YYYYMMDD>.zip` in the project folder, with `bundle_manifest.json` (path, sha256, size, creator).
3. Report the file count per folder and the zip size. Remind the user:
   - share it via the group drive/chat, **not** git (zips are gitignored; the repo is public and the course materials are SMU-restricted)
   - `credentials.yaml` is never included. Each teammate uses their own FRED key (README step 8).

## Unpack
1. The zip must be directly inside `QF600/Final Assignment/`. `python scripts/bundle.py unpack` picks the newest `QF600_Final_Group6_bundle_*.zip` (or pass a path).
2. The script refuses the zip if the manifest is missing, a hash doesn't match, or a path is absolute / contains `..`. Report this and stop.
3. **Exit code 2 = conflicts:** local files that differ from the bundle were skipped. List them and ask the user per file (AskUserQuestion): keep local, or take the bundle's copy. Re-run with `--overwrite <path> …` (or `--overwrite-all` if the user says replace everything).
4. Run the `qf600-data-sync` skill (datasets may have changed).
5. Ask whether to delete the zip now.
6. Summarise: written / unchanged / conflicts and how each was resolved.
