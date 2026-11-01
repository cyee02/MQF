# 04 · Supporting paper: Pun, Wang & Yan, regime-switching robust CVaR

**Citation:** Pun, C. S., Wang, T., & Yan, Z. "Data-Driven Distributionally Robust CVaR Portfolio Optimization under Regime-Switching Ambiguity Set." SSRN 4378930. (NTU / Columbia.)
**File:** `reference_paper/Data-Driven Distributionally Robust CVaR Portfolio Optimization Under A Regime-Switching Ambiguity Set.pdf` (gitignored, in the team bundle). Page numbers are the paper's printed numbers.

**Why we use it:** it gives a principled way to (a) define regimes from an economic variable, (b) estimate regime-switching odds by counting, and (c) use CVaR as the risk measure with **1/N as the benchmark**. Those three pieces feed walkthrough steps 5–6 and Prof Liu's points 4, 9 and 10.

---

## What we borrow

### 1. CVaR, not VaR (p.2, "coherent property")
"CVaR is ... considered a better risk measure than VaR for portfolio optimization due to its **coherent property**", and it can be written as a convex minimisation (Rockafellar & Uryasev 2002).
**Our definition (report it for every strategy, Prof point 10):**
CVaR₅% = − mean of the monthly returns at or below the 5th percentile, i.e. the average loss in the worst 5% of months. Report as a positive loss.

### 2. Regimes from economic variables (p.16, "we can classify the data into four")
The paper's frequency-based approach pre-labels regimes from **covariates**: either bull/bear (sign of the equal-weighted market return), or Bridgewater's four "weathers" from a 2×2 of **inflation (US CPI) and growth (US GDP)** relative to their trailing 1-year moving averages.
→ **Ours:** regimes from the **T-bill rate level** (paper M2 rule) and the **federal deficit** (above/below its median to date), plus the good/middle/bad terciles in step 5.

### 3. Transition probabilities by counting (p.17, Algorithm 2, "by the frequency")
a_{j,k} = #(months in regime j followed by regime k) / #(months in regime j), rows sum to 1.
The next-period regime weights are the row of the **last observed regime**: w_k = a_{j*,k}.
Worked example (p.17): sequence {1,2,1,1,1,2,2,1,2,1} gives A = [[0.4, 0.6], [0.75, 0.25]].
→ **Ours:** estimate a 2×2 (higher/lower) matrix from the history of M2 labels; use it to simulate 10-year paths for "rates stay high" vs "rates fall" (step 6 Monte Carlo).

### 4. Rolling-sample backtest (p.14)
DeMiguel et al. (2009) "rolling-sample" approach: estimate on months t … t+N−1, hold in month t+N, roll forward one month. They use N = 120 months (DeMiguel datasets) and N = 36 months (multi-asset dataset) (p.ec11).
→ **Ours:** train on the previous 10 years, hold 1 year, roll forward (step 6), net of trading costs.

### 5. 1/N as the benchmark; robust optimisation → 1/N (p.14, Proposition 2)
"When Σ_k w_k θ_k → ∞, the solution of the DRO problem ... **converges to the equally weighted portfolio**." Same message as Lecture 5: with no trustworthy return estimates, maximal robustness = 1/N. EW is "a robust choice that is hard to beat" (p.24, citing DeMiguel et al. 2009).
**Headline result (abstract, p.1):** the proposed portfolio "consistently outperforms the equally-weighted portfolio (the 1/N strategy)" and responds promptly to regime change (2008).

### 6. Data facts (for comparison only)
- All data **monthly** (p.24).
- Six DeMiguel et al. (2009) datasets (S&P sectors, industry, international, Mkt/SMB/HML, FF 1-factor, FF 4-factor), extended to **April 2019** from Ken French and MSCI (p.24).
- Multi-asset dataset: equities (10 GICS sectors), 10-yr Treasury, TIPS, commodities (gold, silver, WTI), credit (PIMCO IG fund), **Jan 2004 – Apr 2019** (p.25).
- Risk-free = 90-day T-bill yield (p.24).
- Metrics: Sharpe ratio, certainty equivalent (CEQ), turnover (Tables 2–3).

## What we skip (say so in the report)
- **Wasserstein distributionally robust optimisation** and its LP reformulation (sections 3–4).
- **Hidden Markov model** regime estimation (section 4.1.2).
- Cross-validation of the ambiguity radius θ.
Reason: beyond the course scope (Weeks 1–6), and Prof Liu's questions don't need them (walkthrough, Key terms).

## Quick search phrases
| Topic | Page | Search |
|-------|------|--------|
| Beats 1/N | 1 | "outperforms the equally-weighted" |
| CVaR coherent | 2 | "coherent property" |
| Two regime approaches | 3 | "using frequency to estimate the transition" |
| Prop. 2 → 1/N | 14 | "converges to the equally weighted portfolio" |
| Rolling sample | 14 | "rolling-sample" |
| Bridgewater four regimes | 16 | "classify the data into four" |
| Algorithm 2 / counting | 17 | "by the frequency of occurrence" |
| Datasets, monthly | 24 | "All the data are monthly" |
