---
name: qf600-report
description: QF600 final project only. Create or update 01 - Project Report Group 6.docx (Group 6 project report on Maloney 2024, equity premium in a higher-rate world) from templates/report_template.docx, outputs/results.json and figures/, keeping hand edits and enforcing the guideline (20-page body limit, 1-page executive summary, Annex A datasets). Use for any report writing or editing request in QF600/Final Assignment. Not for QF620.
---

# QF600 report

Scope: `QF600/Final Assignment/01 - Project Report Group 6.docx`. Python: `.venv/bin/python`.

## Read first
- `context/01_requirements.md`: R2.x report rules (cite IDs when you meet them).
- `context/02_execution_plan.md`: section ↔ step skeleton, key terms (use these definitions).
- `context/10_prof_feedback.md`: coverage map; each point must be answered in its section.
- `context/03`, `context/05`: paper facts with page refs; formulas in lecture notation.

## Create (only if the file doesn't exist)
Copy `templates/report_template.docx` to `01 - Project Report Group 6.docx`. Headings are numbered `1 …` to `10 …` plus Executive Summary, References, Annex A, Annex B, AI Assistance Statement. **Keep these heading texts.** `sync_check.py` uses them (C6 Annex A, C7 exec summary, C8 coverage).

## Update (always in place; never regenerate)
1. Back up to `.sync/backups/<timestamp>/` first. Ask the user to close the file in Word.
2. **Numbers:** insert with `office_anchors.docx_add_anchor(paragraph, "num_<key>", display)` using the `display` string from `outputs/results.json`. Never type a result by hand.
3. **Figures:** `doc.add_picture("figures/<fig_id>.png", width=Inches(6))`, then set the picture's alt text: `doc.element.body.xpath('.//wp:docPr')[-1].set('descr', 'fig:<fig_id>')`. Add a caption paragraph "Figure n: … Source: …".
4. **Text:** edit only the paragraphs you were asked to change; leave the rest as the user wrote it.
5. **Annex A** lists every dataset from `02 - Dataset Metadata Group 6.md` (source, description, rows, columns, period).
6. **Citations:** (Maloney 2024, p.6) style; lecture refs as (Lecture 5, slide 14).

## Limits (check before finishing)
- Body (sections 1–10) ≤ **20 pages**. `sync_check.py` estimates it; if LibreOffice is installed, it also measures it.
- Executive summary ≤ **1 page** (≤ 450 words): the question, method, 3 key numbers, central message, recommendation.
- Say plainly that beating benchmarks is not required (R2.7) and report failures honestly.
- Define every metric (R2.6): Sharpe, max drawdown, CVaR 5%, certainty equivalent, t-stat (Newey-West), turnover.

## After editing
Run the `qf600-sync-check` skill. If you changed a claim that slides or the script also make, it will flag the counterpart.
