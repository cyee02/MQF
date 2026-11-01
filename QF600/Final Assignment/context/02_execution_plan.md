# 02 · Execution plan (from `QF600_Group_Project_Walkthrough.docx`)

Source: `QF600_Group_Project_Walkthrough.docx` (dated 1 Nov 2026). This file restates it in a form the notebook, report and slides can follow section by section. **If the walkthrough and this file disagree, the walkthrough wins: update this file.**

**The question:** *Do equities do poorly when risk-free rates are high, and what should an investor hold now?*
Steps 1–4 test whether the paper is right and why. Steps 5–6 turn that into an allocation. Steps 5–6 use whatever steps 2–4 find: if the paper holds, try to improve its strategy; if it fails, use what broke it to set better rules.

**Vocabulary.** "Return above cash" = return − 3-month T-bill. "Ours" = not in the paper. Paper page refs are printed page numbers (see `context/03` §8).

---

## Hypotheses (fixed before seeing results)

| ID | Hypothesis | Source |
|----|-----------|--------|
| **H1** | When rates are high, stocks earn less above cash, and less per unit of risk (lower Sharpe). | Paper, Key Findings p.1 |
| **H2** | Strategies that keep their money in T-bills while trading (**momentum, UMD**) earn about the same above cash whether rates are high or low. | Paper, Key Findings p.1 |
| **H3** | When the government runs a big deficit, company profits keep growing even with high rates, so stocks suffer less. | **Ours** (Kalecki profits identity) |

---

## Step 1 · Collect the data and register predictions
**Do:** collect Ken French (market, RF, UMD), FRED (T-bill, 10-yr, corporate yields, deficit), Shiller (earnings, CAPE), Damodaran annual returns 1928–2025, ETF prices from 2005. Record H1–H3.
**Proves:** our data matches the paper's sources (e.g. our computed bond returns line up with Damodaran's published ones).
**Conclude:** the tests are fair because predictions were fixed first.
**Paper:** data p.4–5 "Long Dataset"; H1/H2 p.1. H3 is ours.
**Notebook section:** §1 Data. **Datasets:** `context/06`.

## Step 2 · Replicate the paper's main results
**Do:**
1. Label each month higher/lower-rate with the three rules (M1 full-sample median; M2 trailing 5-yr at 40th pct; M3 centred 5-yr). Rates < 0.5% always lower. **Only M2 may be used by strategies** (no look-ahead).
2. For stocks, Treasuries, corporate bonds and momentum: average return above cash and Sharpe ratio over the next 1, 12, 36 months, higher vs lower regime → **Exhibit 3**.
3. Regression: excess return_{t+1} on T-bill_t (paper t = −2.2 equities, −2.4 credit).
4. Recompute **Exhibit 9** portfolios from the stated assumptions.
**Proves:** H1, H2, and that our method reproduces the paper.
**First pass (Damodaran):** stocks 9.1%/yr above cash after low-rate years vs 6.7% after high (paper 10.3% vs 5.8%). Same direction, smaller gap.
**Answers Prof Liu:** point 1.
**Paper:** p.4 rules; fn 4 p.4; p.5 Dec 2023; p.6 Exhibit 3; p.5 t-stats; p.12–13 Exhibit 9.

## Step 3 · Test why: profits and the deficit
**Do:**
1. Check the paper's channel: real EPS growth after low rates **11%/yr** vs **1%** after high (p.6).
2. Split higher/lower months again by **deficit** (big = above its median *to date*). Compare next-12-month earnings growth and stock returns in the 4 groups.
**Proves:** H3.
**Conclude:** if yes, high rates alone aren't a reason to sell stocks; may explain 2024–25 (high rates, deficit ≈ 6% of GDP) → strategy **S3**. If no, the paper's channel stands.
**Paper:** p.6 "blistering 11%"; p.7 "Intuitively, it is low". Deficit split and Kalecki are ours.

## Step 4 · Out-of-sample and robustness
**Do:**
1. Fit the regression on **1926–1995**, test on **1996–2026**.
2. Check **2024–2026** on its own.
3. Robustness: (a) simpler rule: rate > own 5-yr average; (b) add **CAPE** (paper: t = −3.2 rate, +3.9 1/CAPE; rates and CAPE both high in early 2024).
**Conclude:** rate the claim **true / partly true / false**. If it failed recently, explain with evidence: CAPE rising; concentration (cap-weight SPY vs equal-weight RSP); the deficit (step 3).
**First pass:** stocks beat cash by **19.7% (2024)** and **13.5% (2025)** vs a 6.7% high-rate average. Two years can't overturn a century → likely "inconclusive" for the recent period.
**Answers Prof Liu:** points 2, 3, 5.
**Paper:** p.7 two-factor + "early 2024"; p.8 Exhibit 4; p.5 "not serially independent"; p.14 "market timing is difficult". OOS split and 2024–26 check are ours.

## Step 5 · What should an investor hold
**Do:**
1. Which assets still diversify stocks when rates are high, rising, falling: **Treasuries, gold, momentum**.
2. Mean-variance stock share by regime: **w\* = (E[R] − r_f) / (A · σ²)** (Lecture 2).
3. Compare **100% stocks, 70/30, 60/40, 50/50 (stocks/bonds), 1/N** in **rising, high-and-steady, falling** rate periods. Metrics: return, volatility, Sharpe, max drawdown, **CVaR 5%**.
4. Sort history into **good / middle / bad** thirds by T-bill rate, a CAPE-based valuation gap, and the deficit. Find the best stock share (0–100% in 10% steps) in each; locate **today** using the latest FRED data.
5. Falling rates get their own comparison: 3-month rate **5.6% (Oct 2023) → 3.7% (early 2026) → 4.2% (Oct 2026)**.
**Proves:** how much a smaller equity reward should cut the stock share; which assets still protect.
**Conclude:** recommended stock share today (the **X** in the central message); whether **50/50 beats 60/40** when rates are high.
**Answers Prof Liu:** points 4, 6, 7, 8, 9, 10, 11.
**Paper:** p.7 rising rates; p.1 + Exhibit 6 p.10 cash-plus; p.9 mechanisms. Gold, 60/40 vs 50/50, terciles are ours / Prof's.

## Step 6 · Backtest strategies and give the verdict
**Do:**
1. **Walk-forward:** choose weights from the previous 10 years, hold 1 year, roll forward; subtract trading costs.
2. **Monte Carlo** 10-year paths under "rates stay high" vs "rates fall", with high↔low switching odds counted from history (CVaR paper Algorithm 2, `context/04`).

| Code | Strategy | Rule |
|------|----------|------|
| **S0** | 60/40 | 60% stocks / 40% Treasuries always. Benchmark (Prof's example) |
| **S1** | Equal weights | 1/N across all assets |
| **S2** | Rate rule | 70% stocks when M2 = lower; 50% when higher (paper's direction) |
| **S3** | Rate + deficit | Like S2, but stay at 60% when rates high **and** deficit big (H3) |
| **S4** | Optimised by period | Mean-variance weights from each regime's history, **ridge** shrinkage (Week 5) |
| **S5** | Cash-plus | Like S2, but stocks sold in high-rate periods go to **momentum** (RF + UMD) instead of bonds |
| **S6** | Paper's portfolios | Exhibit 9 column 2 when rates low, column 4 when high (ETF proxies) |

**Conclude:** final verdict on the paper and one **central message**: *"Being in the middle doesn't mean retreating to risk-free … the best stock share is around X%."* Rewrite if the evidence says otherwise. **Beating 60/40 is not required**: an honest "no" is valid.
**Answers Prof Liu:** points 2, 4, 10, 12.
**Paper:** p.13 Exhibit 9; p.12 four scenarios; fn 11 Sharpe 0.45/0.36/0.44/0.35; p.14 "more—not less—attractive". CVaR paper: p.17 counting; p.1 beats 1/N. S1–S5 and the simulation are ours.

---

## Key terms (use these definitions in the report and slides)

| Term | Definition |
|------|-----------|
| Sharpe ratio | (return − cash) / volatility. Extra return per unit of risk |
| Max drawdown | Largest peak-to-trough fall (≈ −50% for US stocks 2007–09) |
| CVaR 5% | Average loss in the worst 5% of months. Report for **every** strategy |
| Momentum (UMD) | Long past-year winners, short losers. Self-financing, so collateral earns T-bills: return = RF + UMD |
| Cash-plus / liquid alts | Daily-traded hedge-fund-style funds (trend, market-neutral) holding mostly T-bills. Momentum is our stand-in |
| Kalecki identity | Profits = Investment − Household saving + Government deficit + Net exports + Dividends |
| Primary deficit | Deficit excluding interest. Used because high rates mechanically raise interest costs |
| Exhibit 9 portfolios | Low-rate: 37% stocks, 17% PE, 18% Treasuries, 10% RE, 19% cash-plus. High-rate: 26% stocks, 10% PE, 33% Treasuries, 3% HY, 28% cash-plus. ETFs from 2007: SPY, PSP, IEF, HYG, VNQ, momentum |
| Gold | Low correlation with stocks; held up in 2022. Pays no interest, so looks worse when cash pays well |
| CAPE | S&P 500 price / 10-yr average real earnings. 15–20 typical; > 30 expensive |
| Sharpe vs certainty equivalent | Any stock/cash mix has the same Sharpe, so Sharpe can't size the stock share. CE (Week 1) can |
| Ridge and 1/N | Ridge shrinks MVO weights toward equal; with no return signal it gives exactly 1/N (Week 5) |

## Lecture concept map

| Week | Concept | Used in |
|------|---------|---------|
| W1 | Risk aversion, certainty equivalent | Step 5 stock share |
| W2 | Sharpe, CAL/CML, tangency, w\* = (E[R] − r_f)/(Aσ²) | H1, H2, Exhibit 9, steps 2 and 5 |
| W3 | Regression, t-tests, beta, alpha | Paper regressions, H3, strategy alphas (steps 2–4, 6) |
| W4 | Momentum (UMD); four tests for a new signal | Cash-plus; are the rate/deficit signals real (steps 2, 4, 6) |
| W5 | Ridge, 1/N, estimation error, trading costs | S1, S4, Exhibit 9 sensitivity, after-cost backtests (steps 2, 6) |
| W6 (optional) | SDF, E[M] = 1/R_f | One paragraph on why the premium can move with rates |

Details and slide refs: `context/05`.

## Settled questions
- Momentum = **UMD** (Ken French).
- CVaR paper = **Pun, Wang & Yan** regime-switching robust CVaR.
- "i is shrinking" = **interest rates falling** (covered in step 5). *Note:* the Prof feedback note read it as the ERP shrinking. We cover both (see `context/10`). Confirm with Prof.

## Notebook ↔ report ↔ slides skeleton

| Step | Notebook § | Report section | Slides (indicative) |
|------|-----------|----------------|---------------------|
| — | §0 Setup | — | — |
| 1 | §1 Data & hypotheses | 2 Data; Annex A | 2 |
| 2 | §2 Replication | 3 Replication | 3–4 |
| 3 | §3 Profits & deficit | 4 Mechanism | 5 |
| 4 | §4 Out-of-sample | 5 Does it still hold? | 6–7 |
| 5 | §5 Allocation | 6 What to hold | 8–9 |
| 6 | §6 Backtest & simulation | 7 Strategies; 8 Verdict | 10–11 |
| — | — | Exec summary; 1 Problem & impact; 9 Limitations; References; Annexes | 1, 12 (conclusion), Annex |
