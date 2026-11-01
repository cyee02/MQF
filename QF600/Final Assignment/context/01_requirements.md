# 01 · Project requirements (QF600 Group Project Guideline)

Source: `course_materials/QF600 Group Project Guideline.pdf` (2 pages, SMU Classification: Restricted). Every bullet in the guideline is listed below as a checklist item with an ID. `scripts/sync_check.py` and the `qf600-sync-check` skill test these IDs; cite the ID when you say a requirement is met.

## Key dates (Group 6)

| Item | Date | Source |
|------|------|--------|
| Report + code submission | **Tue 03 Nov 2026** | Guideline: "End of Week 10"; date confirmed by group |
| Slides submission | **Tue 03 Nov 2026** | Guideline: "one day before the selected presentation slot" |
| Presentation | **Wed 04 Nov 2026** | Group 6 slot |
| Presentation length | **20 min including Q&A** | Guideline p.2 |

## Project objective (p.2)

> Able to conduct analysis and research on a real-world application of asset pricing and related topics based on recent literature. Provide explanation and seek insight from data understanding, modeling and optimization exercise. Move beyond single-shot application via iterative trial-and-error to seek potential improvement.

| ID | Requirement | How we meet it |
|----|-------------|----------------|
| R0.1 | Real-world asset-pricing application based on recent literature | Maloney (2024, JPM) "Honey, the Fed Shrunk the Equity Premium" → `context/03` |
| R0.2 | Insight from data understanding, modelling and optimisation | Walkthrough steps 2–5 → `context/02` |
| R0.3 | Iterative trial-and-error, not single-shot | Walk-forward backtests and strategy variants S0–S6 (step 6); show what changed between iterations |

## Deliverables (p.2)

| ID | Requirement | Our file |
|----|-------------|----------|
| R1.1 | Project report in Word / PDF / Markdown / web app | `01 - Project Report Group 6.docx` |
| R1.2 | Datasets, preferably CSV, or a link if too big; cite the source if downloaded by script | `datasets/*.csv` + `02 - Dataset Metadata Group 6.md` |
| R1.3 | Execution scripts for data analysis, model development, validation (backtesting) and monitoring (R/Python/open source) | `03 - execution_script_group_6.ipynb` |
| R1.4 | Presentation slides in PowerPoint; **presenter's name on each slide** | `04 - Presentation Slides Group 6.pptx` |
| R1.5 | Only one member submits; **files properly named** | Filenames above. Check none were renamed |

## Report requirements (p.2)

| ID | Requirement | Check |
|----|-------------|-------|
| R2.1 | **Max 20 pages**, excluding cover page, appendix and executive summary | Count body pages in the docx |
| R2.2 | **One-page executive summary** of the most important findings | Exec summary section ≤ 1 page |
| R2.3 | Clearly define the research problem and its impact | Section 1 |
| R2.4 | **Replicate some portion of the target reference paper** | Exhibit 3 + regression + Exhibit 9 replication (`context/03` replication targets) |
| R2.5 | Explain the solution and how it solves the business problem / opportunity | Strategy section + central message |
| R2.6 | Define and explain model performance measures and evaluation metrics | Metrics section (Sharpe, max drawdown, CVaR 5%, CE, t-stats, turnover) |
| R2.7 | No need to beat benchmark methods or show superior performance | State this. An honest "no" is a valid result |

## Slide requirements (p.2)

| ID | Requirement | Check |
|----|-------------|-------|
| R3.1 | PPTX deck summarising important findings and recommendations | Deck ends with conclusion + recommendation slide |
| R3.2 | **All students must speak and present** | Each of Presenter 1–5 owns ≥ 1 slide |
| R3.3 | **Speaker name at the corner of every slide** (marks attributed to that speaker) | Speaker tag top-right on every slide, including title and annex |
| R3.4 | **Screenshots of the most important visualisations in the slides appendix** | Annex section with the key figures |

## Presentation (p.2)

| ID | Requirement | Check |
|----|-------------|-------|
| R4.1 | 20 minutes per group, including Q&A | Talk ≤ 16 min (leave ≥ 4 min Q&A). Timings in speaker notes sum ≤ 16:00 |
| R4.2 | Slides due one day before the slot | 03 Nov 2026 |
| R4.3 | Report + code due end of Week 10 | 03 Nov 2026 |

## Course grading context (Lecture 1 p.5)

Group assignment = **40%** of the course grade, assessed on teamwork, problem solving and **oral communication**. Class participation 20%, final exam 40%.
