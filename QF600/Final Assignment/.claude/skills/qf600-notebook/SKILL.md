---
name: qf600-notebook
description: QF600 final project only. Edit, extend or run 03 - execution_script_group_6.ipynb (the Group 6 execution script: data download, replication of Maloney 2024, out-of-sample tests, allocation, backtests) in the QF627 house style. Every figure goes to figures/ and every reported number to outputs/results.json, so the report and slides can be synced. Use for any notebook/analysis/code request in QF600/Final Assignment. Not for QF620.
---

# QF600 notebook

Scope: `QF600/Final Assignment/03 - execution_script_group_6.ipynb`. Kernel: `.venv`.

## Read first (only what the task needs)
- `context/02_execution_plan.md`: which step/section the work belongs to, hypotheses, strategies S0–S6.
- `context/03_paper_erp_higher_rates.md`: regime rules, replication targets and tolerances.
- `context/06_data_sources.md`: dataset IDs, series, filenames, API keys.
- `context/07_notebook_style.md`: **house style (must follow)** and the results registry.
- `context/05_lecture_concepts.md`: formulas in course notation.

## Rules
1. **Section order** = walkthrough steps: §0 Setup · §1 Data & hypotheses · §2 Replication · §3 Profits & deficit · §4 Out-of-sample · §5 Allocation · §6 Backtest & simulation · §7 Results export. Section headers use the anchor pattern from `context/07`.
2. **Style:** parenthesised method chains with `=\`, `keyword = value` spacing, lets-plot with `labs(title, subtitle, caption = "Source: …")`, markdown narration before and after each key result.
3. **Data:** load from `datasets/<expected file>`; download code in §1 saves there. New dataset → add its row to `context/06` first, then run `qf600-data-sync` after downloading.
4. **Credentials:** `creds = yaml.safe_load(open("credentials.yaml"))`, then `creds["<name>"]`. **Never hard-code a key.** A new key name triggers the set-up sync (README, `credentials.example.yaml`): `qf600-sync-check` C9 will flag it.
5. **No look-ahead in strategies:** only the trailing rule M2 (`context/03` §3) may drive S2–S6. M1/M3 are for replication only. Walk-forward: train 10 yrs, hold 1 yr, roll; subtract trading costs (state the bps).
6. **Results registry:** every number that will appear in the report/slides/script goes through `record(key, value, fmt)`; §7 writes `outputs/results.json`. Keys are stable `snake_case` (`ex3_eq_lower_12m`, `s0_cvar5`). Don't rename a key once used, because the docs reference it.
7. **Figures:** every figure used outside the notebook is saved as `figures/<fig_id>.png` (`ggsave(p, "figures/<fig_id>.png", scale = 2)` or matplotlib `dpi=200`), base text ≥ 14 pt, colours from `context/08` §2 (teal `#5CC6A7`, blue `#5B8DEF`, orange `#E2692F`, gold `#F0B64A`). Stable IDs `figNN_<slug>`.
8. **Metrics** (report for every strategy): annualised return, volatility, Sharpe, max drawdown, **CVaR 5%** (avg loss in worst 5% of months), turnover; t-stats with Newey-West next to OLS.
9. **Replication:** compare each result to the target table in `context/03` §4 and print ours vs paper side by side.

## After editing
1. Run the notebook top to bottom (`python -m nbconvert --to notebook --execute --inplace "03 - execution_script_group_6.ipynb"`) or the changed sections, and fix errors.
2. Run the `qf600-sync-check` skill: changed numbers/figures are then pushed to 01/04/05 after the user reviews them.
