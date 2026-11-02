# QF600 Final Project — Set-up Plan

**Scope of this phase:** project set-up only. Build the context files ("RAG"), skills, folder layout and sync mechanism so that anyone who clones the repo can open Claude Code and edit the deliverables consistently. **Do not** generate the deliverables' content in this phase (stubs/templates only).

**Root:** `QF600/Final Assignment/` (all paths below are relative to it, including `.claude/`, the project-scoped Claude folder).

**Key dates (Group 6)**
| Item | Date |
|------|------|
| Presentation | **Wed 04 Nov 2026** (20 min incl. Q&A) |
| Slides submission | **Tue 03 Nov 2026** (one day before slot) |
| Report + code submission | **Tue 03 Nov 2026** |

---

## 0. Files

### Deliverables (submitted)
| # | File | Built with |
|---|------|-----------|
| 01 | `01 - Project Report Group 6.docx` | python-docx (patched in place) |
| 02 | `02 - Dataset Metadata Group 6.md` | `qf600-data-sync` skill |
| 03 | `03 - execution_script_group_6.ipynb` | Jupyter |
| 04 | `04 - Presentation Slides Group 6.pptx` | python-pptx (patched in place, + XML for animations) |

### Non-deliverable (kept in sync, not submitted)
| # | File |
|---|------|
| 05 | `05 - Presentation Script.docx` |

### Source records (read-only inputs)
| Record | Path | In git? | In team bundle? |
|--------|------|---------|-----------------|
| Project guideline | `course_materials/QF600 Group Project Guideline.pdf` | no | yes |
| Lecture notes W1–W9 | `course_materials/lecture_notes/Session *.pdf` | no | yes |
| Execution plan | `QF600_Group_Project_Walkthrough.docx` | yes | — |
| Target paper | `reference_paper/Equity Risk Premium Higher Rate Regime.pdf` | no | yes |
| CVaR paper (Pun, Wang, Yan) | `reference_paper/Data-Driven Distributionally Robust CVaR Portfolio Optimization Under A Regime-Switching Ambiguity Set.pdf` | no | yes |
| Notebook style refs | `reference_style/QF627_PreCourse_0[1-4]_*.ipynb` | no | yes |
| Slide style refs | `reference_style/QF600_*.pptx` | yes | — |
| Datasets | `datasets/*` | no | yes |
| Credentials | `credentials.yaml` | no | **never** |

**Implication:** a clone without the bundle has only the markdown context, so every context file in §2 must be self-contained. The bundle (§4.6) restores the originals.

---

## 1. Housekeeping — ✅ done 01 Nov 2026

Done: notebook renamed; `analysis.ipynb` and root guideline PDF deleted (verified byte-identical); folders + `.gitkeep` created; `credentials.example.yaml`, `requirements.txt` added; `.gitignore` updated. Also fixed: FRED API key was hard-coded in the notebook → now `creds["fred_key"]`. Left as is: GFD login cell uses Finaeon's public trial account (`tryapi@finaeon.com`); decide when GFD is settled.


1. **Rename** `execution_scripts.ipynb` → `03 - execution_script_group_6.ipynb`. Delete `analysis.ipynb` (byte-identical duplicate). Confirm with user before deleting.
2. **Remove duplicate** `QF600 Group Project Guideline.pdf` at the root (canonical copy is in `course_materials/`). Confirm first.
3. **Credentials:** keep `credentials.yaml` gitignored; add committed `credentials.example.yaml` with `fred_key: <your-key>`. Notebook errors with a clear message if `credentials.yaml` is missing.
4. **.gitignore** (repo root):
   - add `QF600/Final Assignment/course_materials/`
   - add `QF600/Final Assignment/datasets/*` and `!QF600/Final Assignment/datasets/.gitkeep`
   - add `QF600/Final Assignment/*.zip` (team bundles)
   - add `QF600/Final Assignment/.sync/backups/`
   - add `~$*` (Office lock files; three currently in the folder)
   - remove stale line `QF600/Final Assignment/QF600 Group Project Guideline.pdf`
5. Add `requirements.txt`: pandas, numpy, statsmodels, scipy, fredapi, pyyaml, requests, openpyxl, xlrd, yfinance, lets-plot, matplotlib, python-docx, python-pptx, nbformat, nbconvert.
6. Create folders: `context/`, `figures/`, `outputs/`, `templates/`, `scripts/`, `.sync/`.

---

## 2. Context files (the "RAG") — ✅ done 01 Nov 2026

Markdown under `context/`, indexed by `context/00_index.md`, which `CLAUDE.md` points to. Each file cites source page/section so claims can be checked.

| File | Source | Must contain |
|------|--------|-------------|
| `00_index.md` | — | One line per context file + when to read it |
| `01_requirements.md` | Guideline PDF | Each guideline bullet as a checklist item with ID (R1, R2…): deliverables; report max 20 pp excl. cover/appendix/exec summary; 1-page exec summary; define problem & impact; replicate part of paper; explain solution; define metrics; no need to beat benchmark; PPTX; **every member presents**; **speaker name on corner of every slide**; screenshots of key visuals in slide appendix; 20 min incl. Q&A; deadlines (§ Key dates); one member submits; proper file naming. |
| `02_execution_plan.md` | Walkthrough docx | Question; H0–H2; Steps 1–6 with Do / Proves / Conclude / paper page refs; strategies S0–S6; Key terms; lecture concept map; settled questions. |
| `03_paper_erp_higher_rates.md` | Target paper | Authors, title, date; research question; **data: each series with source, frequency, start/end date, transformations**; regime definitions (3 rules, 0.5% floor, 40% cut-off); Exhibit 3, 4, 6, 9 numbers (tables); regressions (t = −2.2, −2.4; CAPE t = −3.2/+3.9); Exhibit 9 weights + assumed inputs; footnote 11 Sharpe ratios; paper's own caveats. "Replication targets" table: exhibit → notebook section → tolerance. |
| `04_paper_cvar_regime.md` | CVaR paper | Only what we borrow: regimes from an economic variable (p.16), switch-counting transition probabilities (p.17), CVaR vs VaR (p.2), 1/N benchmark, Prop. 2. State what we skip (robust optimisation, HMM). |
| `05_lecture_concepts.md` | Lecture notes W1–W6 | Formulas/notation exactly as taught (CE, Sharpe, CAL, w* = (E[R]−rf)/(Aσ²), regression/t-tests, UMD, ridge, 1/N, trading costs, SDF), with session + slide refs. |
| `06_data_sources.md` | Walkthrough Step 1 + paper | Per dataset: provider, URL / FRED series ID, frequency, period, download method (script vs manual), expected filename in `datasets/`, status (pending / downloaded). Ken French (Mkt-RF, RF, UMD), FRED (TB3MS, GS10, BAA/AAA, deficit), Shiller (earnings, CAPE), Damodaran (1928–2025, **pending — user to add**), ETFs (SPY, PSP, IEF, HYG, VNQ, GLD, RSP). GFD/Finaeon status **pending — user to decide**. Kept in sync by `qf600-data-sync`. |
| `07_notebook_style.md` | QF627 notebooks | Distilled style: heading pattern, markdown narration between cells, naming, lets-plot theme, table display, import cell layout, 2–3 verbatim example cells. |
| `08_slide_style.md` | Two QF600 decks | Slide size, layouts, fonts + sizes, palette (hex), title/footer placement, **speaker-name tag position (top corner, as in HW #2)**, section-number badge, chart styling, CONCLUSION slide pattern, "NEXT STEPS" block, Annex A/B pattern, closing disclaimer line ("Prepared with the assistance of Claude… All results were checked by the Group." and "Coursework only… Not investment advice."). |
| `09_group.md` | Reference decks | Members in title-slide order (same in both decks): **Chew Junhong · Marcus Tan Jun Lin · Chia Chong Yee · Abirame d/o Asohan · Ramona Chia Ming Li**. Short names: Junhong, Marcus, Chong Yee, Abirame, Ramona. **Presenters are placeholders `Presenter 1`…`Presenter 5`** until the user confirms the mapping; speaker tags, script sections and ownership use the placeholder. A single mapping table (Presenter n → name) lives here, and `qf600-sync-check` replaces placeholders in 04/05 once it is filled in. Time budget ≈3 min each, ≈15–16 min total, ≥4 min Q&A. |
| `10_prof_feedback.md` | User (pasted 1 Nov 2026) | Prof Liu's 12 points **verbatim** with our "next step" for each, plus a map point → walkthrough step → report section → slide. Note on point 6: feedback note read "i is shrinking" as ERP shrinking; walkthrough (settled) reads it as **rates falling**. Plan covers both (falling-rate comparison in Step 5; w* sensitivity to shrinking ERP in point 7). Confirm with Prof. |

**Acceptance:** every number in 03/04 has a page reference; 01 has a checklist ID for every guideline bullet; 10 maps all 12 points to at least one section.

---

## 3. Templates — ✅ done 01 Nov 2026 (`scripts/build_templates.py`)

1. `templates/slides_template.pptx` — from the HW #2 deck: keep masters/layouts, delete content slides. Speaker-tag text box in top corner.
2. `templates/report_template.docx` — cover, exec summary, numbered headings, caption styles, Annex A "Datasets", References, AI-assistance statement.
3. `templates/script_template.docx` — one section per member; per slide: slide no., title, speaker, start time, duration, script text, `[CLICK n]` markers.

**Anchors (needed for in-place sync):** every synced element carries a stable ID.
- pptx: shape name `num:<key>`, `fig:<fig_id>`, `txt:<slide_key>.<n>`; notes start with `slide_key:`.
- docx: bookmarks / content controls named `num_<key>`, `fig_<fig_id>`; script headings carry `slide_key`.

---

## 4. Skills and CLAUDE.md — ✅ done 01 Nov 2026

Scoped to this project: `QF600/Final Assignment/.claude/skills/qf600-*` and `QF600/Final Assignment/CLAUDE.md`, so they apply only to QF600 and never to QF620 or other courses. They ship with the clone. The repo-wide `pr-readme` skill stays in `MQF/.claude/skills/`. Each skill: trigger description, inputs, steps, done-criteria; points to `context/` rather than duplicating it.

1. **`QF600/Final Assignment/CLAUDE.md`** — scope, file table (§0), key dates, "read `context/00_index.md` first", the sync rules (§5), "run `qf600-sync-check` after any edit".
2. **`qf600-notebook`** — edit/run 03 in the style of `context/07`; every figure saved to `figures/<fig_id>.png` (high DPI, slide-readable fonts); every reported number written to `outputs/results.json` (key, value, display format, source cell).
3. **`qf600-report`** — create/update 01 from template + `results.json` + `figures/`; enforce page limit and 1-page exec summary; Annex A from 02.
4. **`qf600-slides`** — create/update 04 and 05 together: speaker tag on every slide, readable figures (min font sizes from `context/08`), word budget per slide, speaker notes = script + start time + duration + `[CLICK n]`, appendix with key screenshots, timing within budget.
5. **`qf600-data-sync`** — run whenever a file is added/changed/removed in `datasets/`:
   1. Scan `datasets/`, compare with `.sync/datasets.json` (filename, sha256, size).
   2. For each new/changed file: profile it (row count, columns + dtypes, date range, inferred frequency, missing values).
   3. Look up source/description in `context/06`; if unknown, ask the user (provider, URL, how downloaded).
   4. Ask/record how the dataset is obtained: script (which API, needs key?), manual download, or team bundle only.
   5. Update `02 - Dataset Metadata Group 6.md` (source, description, rows, columns, period, frequency, link), `context/06` status, and `.sync/datasets.json`.
   6. If the dataset needs a new API key or package, apply the set-up updates in §5.1 (README, `credentials.example.yaml`, `requirements.txt`).
   7. Hand off to `qf600-sync-check` so Annex A in 01 is updated.
6. **`qf600-bundle`** — share gitignored materials with teammates.
   - **Pack:** zip `course_materials/`, `reference_paper/`, `reference_style/QF627_*.ipynb`, `datasets/` into `QF600_Final_Group6_bundle_<YYYYMMDD>.zip` at the root, with `bundle_manifest.json` (path, sha256, size, created by/at). **Never** include `credentials.yaml`, `.sync/backups/`, lock files. Report file count + size.
   - **Unpack:** when a `QF600_Final_Group6_bundle_*.zip` is in the root: verify manifest hashes; reject absolute paths / `..` (zip-slip); list files that would overwrite a local file with different content and ask before overwriting; extract; then run `qf600-data-sync`. Ask whether to delete the zip afterwards.
7. **`qf600-sync-check`** — detect and propagate changes (§5–6).

---

## 5. Sync mechanism (hand edits preserved)

Notebook 03 is the only producer of numbers and figures. Docs 01/04/05 are **patched in place at their anchors**, never regenerated, so any text outside anchors (and hand edits inside them) survive.

```
datasets/ ──► 03 notebook ──► outputs/results.json, figures/
   │                                   │
   └─► qf600-data-sync ──► 02 .md      ▼
                       01 Report ◄──► 04 Slides ◄──► 05 Script
                              (patched at anchors)
```

**Snapshot:** `.sync/snapshot.json` stores, per file, what was last agreed: anchor → text/value, figure hashes, slide list (key, title, speaker, timing, click count), script sections, notebook `results.json` copy, dataset hashes. Committed to git so all teammates share the same baseline.

**Workflow of `qf600-sync-check`:**
1. Extract current state of 01–05 (+ `results.json`, `figures/`).
2. Diff against the snapshot. Report each change grouped by file: *what changed, where (anchor / slide / paragraph), old → new*.
3. **Prompt the user** to review each change: accept / reject (revert) / edit.
4. For accepted changes, propagate to the dependent files:
   - number/figure change in 03 → 01, 04, 05
   - slide text/order/speaker/timing/click change in 04 → 05 (and vice versa)
   - text change in 01 that states a result → flag if it no longer matches `results.json`; ask whether the notebook or the report is right
   - dataset change → 02 → Annex A in 01
   - code change in 03 (or `scripts/`) that changes set-up → README, `credentials.example.yaml`, `requirements.txt` (§5.1)
5. Before writing, back up each file to `.sync/backups/<timestamp>/`.
6. Run the alignment checks (§6); on pass, update the snapshot.
7. Close with a short summary of changes made per file.

Unanchored hand edits (free text) are shown in the diff but only propagated when the user says which counterpart to change.

### 5.1 Set-up sync (README stays true to the code)

`README.md` is the teammates' set-up guide, so it must match what the code needs. `qf600-sync-check` and `qf600-data-sync` scan the notebook and `scripts/` and compare against the snapshot:

| Detected in code | Update |
|------------------|--------|
| New `creds["<name>"]` key (e.g. a new data API) | README step 8: how to get the key (sign-up URL, where the key is in the account page, free/paid); new placeholder in `credentials.example.yaml`; troubleshooting row for a missing key |
| Removed credential | Remove it from README step 8 and `credentials.example.yaml` |
| New `import` of a third-party package | Add to `requirements.txt`; README step 6 unchanged unless extra install steps are needed (e.g. system libraries) |
| New download URL / API host | `context/06` + README "What's in this folder" note if a dataset is script-only vs bundle-only |
| New manual dataset (not script-downloadable) | README step 7: say it comes in the bundle; remind owner to re-pack (`qf600-bundle`) |
| New/renamed deliverable or folder | README "What's in this folder" table |
| New/renamed skill in `.claude/skills/qf600-*` | README step 10 table |
| Python version requirement change | README step 3 |

Rules:
- Show the proposed README diff and ask before writing, like any other change.
- Credentials are detected by name only. Never read or copy values from `credentials.yaml` into any file.
- Hard-coded secrets in code (API-key-like strings, passwords) → stop, flag to the user, and propose moving them to `credentials.yaml`. The repo is public.

---

## 6. Alignment checks (`scripts/sync_check.py`) — ✅ built 01 Nov 2026 (checks C1–C10)

1. Every `num:` anchor in 01/04/05 equals the formatted value in `results.json`.
2. Every `fig:` image in 01/04 has the same hash as `figures/`.
3. Slide keys, titles, order and speakers in 04 == 05.
4. Timings in 04 notes == 05; cumulative start times consistent; total ≤ budget.
5. `[CLICK n]` count in script == animation count on that slide.
6. Datasets in `datasets/` == 02 == Annex A in 01 (rows, columns, sources).
7. Guideline checklist R1…Rn (page count, exec summary ≤ 1 page, speaker tag on every slide, appendix screenshots, filenames, every member has ≥ 1 slide).
8. Every Prof Liu point (`context/10`) is addressed in ≥ 1 report section and slide.
9. Set-up is in sync (§5.1): every `creds[...]` key in code is in `credentials.example.yaml` and README step 8; every third-party import is in `requirements.txt`; every `qf600-*` skill is in README step 10; no hard-coded secrets in 03 or `scripts/`.
10. Notebook executes top-to-bottom (`nbconvert --execute`) — run on request, as it needs datasets.

---

## 7. Data reproducibility

- Notebook section 1 (or `scripts/download_data.py`) downloads every script-accessible dataset to `datasets/`.
- Manually obtained files (Damodaran, any GFD extract) — download steps + expected filename in `context/06`; shared via `qf600-bundle`.
- 02 lists source + link for each (guideline deliverable #2).

---

## 8. Execution order

1. §1 housekeeping (confirm deletions with user)
2. §2 context files 00–10
3. §3 templates with anchors
4. §5/§6 scripts: `sync_check.py`, `data_sync.py`, `bundle.py` (work on empty outputs)
5. §4 CLAUDE.md + skills
6. Dry run in a scratch dir: clone → install → unpack a test bundle → `qf600-data-sync` → `qf600-sync-check` passes on stubs; make a hand edit in 04 and confirm it is detected and offered for propagation to 05
7. Commit on a new branch; PR via `pr-readme`

**Timeline note:** report, code and slides are all due Tue 03 Nov — finish set-up 01 Nov, leaving 02 Nov for content.

---

## 9. Open questions

1. Presenter n → member mapping (user will confirm; placeholders until then).
2. "i is shrinking": confirm with Prof whether it means rates falling (walkthrough) or ERP shrinking (feedback note).
3. Damodaran data and GFD decision — pending, user will add later (`qf600-data-sync` handles it).
