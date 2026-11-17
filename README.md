# MQF

Coursework, notebooks, and notes for the MQF programme.

## QF600 — Asset Pricing

| Work | Notes |
|---|---|
| [Assignment 1 — Compute Alpha](QF600/Assignment%201%20-%20Compute%20Alpha/) | Alpha/beta decomposition of an investor portfolio (QQQ/DBMF/GLD) against a benchmark (SPY), backtested both rebalanced and buy-and-held so every metric carries the cost of the schedule, with drawdown and CVaR tail risk, optional Markowitz max-Sharpe re-weighting at each rebalance, and a choice of risk-free convention (10-year, 5-year, or none) compared side by side. Live companion: [Alpha Bench](https://claude.ai/code/artifact/2492151c-5692-4cad-9ea6-f6f1f5f09c46) |
| [Final Project — Equity Premium in a Higher-Rate World](QF600/Final%20Assignment/) | Group 6 project replicating and stress-testing Maloney (2024), "Honey, the Fed Shrunk the Equity Premium", then recommending an allocation for a higher-rate world. Set-up: context summaries of the guideline, papers, lectures and Prof Liu's feedback; project-scoped Claude skills for the notebook, report, slides, data and sync checks; teammate set-up guide in the folder's README. |

## QF620 — Stochastic Modelling in Finance

| Work | Notes |
|---|---|
| [Final Project — SPX Options During the 2025 Liberation Day Tariff Shock](QF620/Final%20Assignment/) | Group project on how SPX options priced the April 2025 tariff shock. `analysis.ipynb` covers data prep, the implied volatility smile, and the volatility surface and term structure (Section 2: the two quoted expiries through the event and their term structure against the VIX, a supporting SVI surface with its flat-vol assumptions marked, no-arbitrage checks, and the `iv_surface(timestamp)` function, with charts in [figures/](QF620/Final%20Assignment/figures/) and report text in [Vol surface report sections (2.4 and 3.2).md](QF620/Final%20Assignment/Vol%20surface%20report%20sections%20%282.4%20and%203.2%29.md)); [`analysis_glen.ipynb`](QF620/Final%20Assignment/analysis_glen.ipynb) is a copy that adds the SABR calibration (Section 3); report text for the SABR sections is in [SABR report sections (2.5 and 3.3).md](QF620/Final%20Assignment/SABR%20report%20sections%20%282.5%20and%203.3%29.md). |

---

The `pr-readme` skill in [.claude/skills/pr-readme/](.claude/skills/pr-readme/SKILL.md) keeps this
index in sync whenever a pull request is opened.
