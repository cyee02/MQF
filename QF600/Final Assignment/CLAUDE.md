# QF600 Final Project · Group 6

Group project for QF600 Asset Pricing (SMU MQF): replicate and stress-test Maloney (2024), "Honey, the Fed Shrunk the Equity Premium", then recommend an allocation for a higher-rate world. This file and the `qf600-*` skills in `.claude/skills/` apply **only to this folder**, not to QF620 or other courses in the repo.

**Due: report + code + slides Tue 03 Nov 2026 · presentation Wed 04 Nov 2026 (20 min incl. Q&A).**

## Start here
Read `context/00_index.md`, then only the context file the task needs. Context files are self-contained; the source PDFs/notebooks are gitignored (team bundle only).

## Files
| # | File | Submitted | Skill |
|---|------|-----------|-------|
| 01 | `01 - Project Report Group 6.docx` | yes | `qf600-report` |
| 02 | `02 - Dataset Metadata Group 6.md` | yes | `qf600-data-sync` |
| 03 | `03 - execution_script_group_6.ipynb` | yes | `qf600-notebook` |
| 04 | `04 - Presentation Slides Group 6.pptx` | yes | `qf600-slides` |
| 05 | `05 - Presentation Script.docx` | no | `qf600-slides` |

Other skills: `qf600-sync-check` (after any edit), `qf600-bundle` (share gitignored files).

## Rules
1. **The notebook is the only source of numbers and figures.** It writes `outputs/results.json` and `figures/`; 01/04/05 reference them through anchors (`num_<key>`, `num:<key>`, `fig:<id>`).
2. **Patch, don't regenerate.** Edit 01/04/05 in place so hand edits survive. Back up to `.sync/backups/` first.
3. **After any edit, run `qf600-sync-check`.** It shows what changed since the last agreed snapshot, asks the user to review, propagates accepted changes, and re-runs the alignment checks.
4. **Presenters are `Presenter 1`–`5`** until the mapping is confirmed in `context/09_group.md`.
5. **Never hard-code credentials.** Keys live in `credentials.yaml` (gitignored); names in `credentials.example.yaml`; how-to in README step 8. The repo is public.
6. **Keep README.md true to the code.** New key, package, dataset or skill → update README (see `plan.md` §5.1).
7. Strategies may only use information available at the time (trailing regime rule M2; walk-forward).

## Commands (run from this folder)
```bash
.venv/bin/python scripts/sync_check.py            # diff + alignment checks
.venv/bin/python scripts/sync_check.py --accept   # save agreed snapshot (after user agrees)
.venv/bin/python scripts/sync_apply.py push-numbers | push-figures | push-names
.venv/bin/python scripts/data_sync.py [--write]
.venv/bin/python scripts/bundle.py pack | unpack
.venv/bin/python scripts/build_templates.py       # rebuild templates/ (needs the bundle)
```
Windows: `.venv\Scripts\python` instead of `.venv/bin/python`.
