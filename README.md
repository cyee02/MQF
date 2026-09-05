# MQF

Coursework notebooks and notes.

## Contents

| Course | Work | What it does |
|---|---|---|
| QF600 — Asset Pricing | [Assignment 1 — Compute Alpha](QF600/Assignment%201%20-%20Compute%20Alpha/) | Backtests an investor portfolio (SOXX 70 / GLD 30) against a benchmark (IVV 60 / AGG 40) with periodic rebalancing, then decomposes the result into beta and alpha via OLS on daily excess returns. |

Each assignment folder carries its own `README.md` with the methodology; the notebooks sit alongside
them and run unchanged locally (VSCode + Data Wrangler) or in Google Colab.

## Conventions

- One folder per course (`QF600`, `QF627`, …), one subfolder per assignment.
- An assignment's write-up lives in that folder's `README.md`, so GitHub renders it when the folder
  is opened.
- This index is refreshed whenever a pull request is opened — see
  [`.claude/skills/update-readme-on-pr`](.claude/skills/update-readme-on-pr/SKILL.md).
