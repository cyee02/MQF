---
name: qf600-sync-check
description: QF600 final project only. Detect every change made to the QF600 Group 6 deliverables (report, dataset metadata, notebook, slides, presenter script) since the last agreed sync, ask the user to review each change, then propagate accepted changes to the other files and re-check alignment. Use after ANY edit to a file in QF600/Final Assignment, when the user says "run the sync check", "sync", "check alignment", or after the notebook is re-run. Not for QF620 or other courses.
---

# QF600 sync check

Scope: `QF600/Final Assignment/` only. All commands run from that folder.
Python: `.venv/bin/python` (Windows: `.venv\Scripts\python`).

The notebook (03) is the **only** source of numbers and figures. 01, 04, 05 are **patched in place at anchors**, never regenerated, so hand edits survive. See `plan.md` §5–6 for the design.

## Steps

1. **Detect.** Run `python scripts/sync_check.py --json` (add `--execute` if the user changed the notebook code and wants it re-run). If `snapshot` is false, this is the first sync. Show the checks, ask the user if the current state is agreed, then `--accept`.
2. **Show the changes**, grouped by file, in plain words: *what changed, where (file · slide/section/anchor), before → after*. Text diffs: show the diff lines, not the whole section.
3. **Ask the user to review each change** (AskUserQuestion, one question per change or per group of related changes): **Accept** (propagate) · **Revert** (restore from the snapshot/backup) · **Edit** (user says what it should be).
4. **Propagate accepted changes.** Back-ups are automatic in `sync_apply.py`; for edits you make yourself, first copy the file to `.sync/backups/<timestamp>/`.

   | Change | Propagate to | How |
   |--------|-------------|-----|
   | Number in `outputs/results.json` | every `num_<key>` (01, 05) / `num:<key>` (04) | `python scripts/sync_apply.py push-numbers --keys <key>` |
   | Figure in `figures/` | `fig:<id>` pictures in 01 and 04 | `python scripts/sync_apply.py push-figures --ids <id>` |
   | Slide title / order / speaker / timing / clicks (04) | matching section in 05 | edit 05 with python-docx (`office_anchors.script_slides` shows its structure) |
   | Script text or timing (05) | notes of the same slide in 04 | edit notes with python-pptx; keep the `[NAME · m:ss–m:ss]` header and `[CLICK n]` markers |
   | Text in 01 that states a result | — | if it no longer matches `results.json`, **ask** whether the notebook or the report is right; never silently overwrite |
   | Free text on a slide (not an anchor) | the script, if the script quotes it | ask the user which counterpart to change |
   | Dataset added/changed/removed | 02 → Annex A in 01 | run the `qf600-data-sync` skill |
   | Presenter mapping filled in `context/09` | tags, notes headers, script | `python scripts/sync_apply.py push-names` |
   | Set-up change (C9: new `creds[...]` key, import, skill) | README, `credentials.example.yaml`, `requirements.txt` | see "Set-up sync" below |

5. **Re-check:** `python scripts/sync_check.py`. Fix anything that still fails, or explain why it can't be fixed yet (e.g. deliverable not created).
6. **Close the loop.** When the user agrees the state is right: `python scripts/sync_check.py --accept` (writes `.sync/snapshot.json`, which is committed so teammates share the baseline).
7. **Summarise** in 3–6 lines: changes accepted / reverted per file, what was propagated, checks still failing.

## Alignment checks (what `sync_check.py` reports)
C1 numbers = results · C2 figures = figures/ · C3 slides = script (titles, order, speakers) · C4 timings contiguous, notes = script, ≤ 16:00 · C5 animation count = `[CLICK n]` count in notes = script · C6 datasets/ = 02 = Annex A · C7 guideline checklist (`context/01`) · C8 Prof Liu's 12 points mapped (`context/10`) · C9 set-up in sync, no hard-coded secrets · C10 notebook runs (`--execute`).

## Set-up sync (README stays true to the code)
When C9 fails or the diff shows `creds_keys` / `imports` / `skills` changed:
- **New credential `creds["<name>"]`:** add `<name>: <your-...>` to `credentials.example.yaml`; add to README step 8 how to get it (sign-up URL, where the key is shown, free/paid) and mention `<name>` literally; add a troubleshooting row. Removed credential → remove both.
- **New third-party import:** add the pip package name to `requirements.txt` (import → package: yaml→pyyaml, docx→python-docx, pptx→python-pptx, lets_plot→lets-plot, sklearn→scikit-learn).
- **New/renamed qf600 skill:** update README step 10 table.
- **Hard-coded secret found:** stop, tell the user where it is, propose moving it to `credentials.yaml` (the repo is public). Never print the full value; never read values from `credentials.yaml`.
- Show the README diff and ask before writing.

## Rules
- Never regenerate 01/04/05 from scratch. Patch anchors or the specific paragraph/shape.
- Never accept the snapshot without the user's agreement.
- If a deliverable is open in Word/PowerPoint, ask the user to close it before writing (lock files `~$*`).
