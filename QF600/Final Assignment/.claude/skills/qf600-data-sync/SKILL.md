---
name: qf600-data-sync
description: QF600 final project only. Sync dataset metadata whenever a file is added, changed or removed in QF600/Final Assignment/datasets/. Profiles each file (rows, columns, types, date range, frequency), asks the user for any missing source details, and updates 02 - Dataset Metadata Group 6.md, the report's Annex A, context/06 and, when a new API key or package is needed, the README set-up guide. Use when the user says "I added a dataset", "sync the metadata", after a bundle unpack, or after notebook §1 downloads data. Not for QF620.
---

# QF600 data sync

Scope: `QF600/Final Assignment/`. Python: `.venv/bin/python` (Windows `.venv\Scripts\python`).

## Steps

1. **Scan:** `python scripts/data_sync.py`. It prints `new`, `changed`, `removed`, `needs_meta`. Nothing is written yet.
2. **Fill missing metadata.** For each `needs_meta` file, first look for a matching row in `context/06_data_sources.md` (by expected filename). If none, ask the user (AskUserQuestion, one question per file is fine):
   - provider and link (URL, FRED series ID, or "manual download from …")
   - one-line description
   - how it is obtained: `script` (which API? needs a key?) or `manual` (bundle only)
   Then record it: `python scripts/data_sync.py --set <file> --provider "…" --url "…" --description "…" --method script|manual [--key <cred_name>]`
3. **Register in context/06.** If the file had no row, add one (next free `D` ID; columns as in the table; status `downloaded`).
4. **Write:** `python scripts/data_sync.py --write` → updates `.sync/datasets.json`, regenerates the `AUTO` block in `02 - Dataset Metadata Group 6.md` (text outside the block is preserved), and sets status `downloaded` in context/06.
5. **Annex A in the report (01).** If `01 - Project Report Group 6.docx` exists, update the "Annex A Datasets" section so it lists every dataset with source, description, rows and columns (same facts as 02). Edit only that section; back up first to `.sync/backups/<timestamp>/`.
6. **Set-up impact** (`plan.md` §5.1):
   - Needs a **new API key** → add `<key>: <your-…>` to `credentials.example.yaml`; add to README step 8 how to get the key (sign-up URL, where it is shown, free/paid) and name `<key>` literally; tell the teammate to add it to their own `credentials.yaml`. Never read or copy values from `credentials.yaml`.
   - Needs a **new package** → add it to `requirements.txt`.
   - **Manual** dataset → README step 7 already says it comes in the bundle; remind the user to re-pack (`qf600-bundle`) and share the new zip.
   - Show README/credentials diffs and ask before writing.
7. **Hand off:** run the `qf600-sync-check` skill (C6 checks datasets/ = 02 = Annex A).
8. **Summarise:** files added/changed/removed, rows × columns for each new file, anything the user still has to do.

## Notes
- `datasets/` is gitignored. The metadata (02, `.sync/datasets.json`) is committed.
- Excel files (Shiller, Damodaran) are profiled sheet by sheet; their headers are messy, so check the column list and write a better description by hand if needed.
- Removed files: confirm with the user that the removal is intended before writing.
