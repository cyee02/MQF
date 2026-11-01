# 02 · Execution plan (from `QF600_Group_Project_Walkthrough.docx`)

Source: `QF600_Group_Project_Walkthrough.docx` (dated 1 Nov 2026). This file restates it in a form the notebook, report and slides can follow section by section. **If the walkthrough and this file disagree, the walkthrough wins: update this file.**

**The question:** *Do equities do poorly when risk-free rates are high, and what should an investor hold now?*
Steps 1–4 test whether the paper is right and why. Steps 5–6 turn that into an allocation. Steps 5–6 use whatever steps 2–4 find: if the paper holds, try to improve its strategy; if it fails, use what broke it to set better rules.

**Vocabulary.** "Return above cash" = return − 3-month T-bill. "Ours" = not in the paper. Paper page refs are printed page numbers (see `context/03` §8).

---

## Hypotheses (fixed before seeing results)

**Part A · Replicate the paper** on the paper's sample (monthly, Jan 1926 – Dec 2023). The paper's main source, Global Financial Data (Finaeon), isn't available: SMU has no subscription, so we use free proxies (`context/06`).

| ID | Hypothesis | Source |
|----|-----------|--------|
| **H0** | The level of the T-bill rate makes no difference: stocks earn the same above cash after high-rate months as after low-rate months. | Null hypothesis (ours) |
| **H1** | After high-rate months, stocks earn less above cash (the paper's claim). | Paper, Key Findings p.1 |

**Part B · Test whether the paper's conclusion holds up**, using the Sharpe ratio and the fiscal deficit.

| ID | Hypothesis | Source |
|----|-----------|--------|
| **H2** | Sharpe ratio: once risk is counted, high rates don't hurt stocks much. The equity Sharpe ratio after high-rate months is not materially lower than after low-rate months (paper: 0.57 vs 0.31). Tested on 1926–2023 and on the extension to 2026. | Ours, challenging paper p.6 "Economic drivers" |
| **H3** | Fiscal-deficit offset: when the government runs a big deficit, company profits keep growing even with high rates, so stocks' return above cash after high-rate months is not lower when the deficit is big. | Ours (Kalecki profits identity) |

The paper's momentum claim (momentum / cash-plus earns about the same above cash in both regimes, Key Findings p.1) is **not a separate hypothesis**: it is a replication check in step 2 and feeds the cash-plus discussion in steps 5–6 (momentum is one of the four benchmark assets).

---

## Step 1 · Collect the data and register the hypotheses
**Do:** collect Ken French (market, RF, UMD), FRED (T-bill, 10-yr, corporate yields, deficit), Shiller (earnings, CAPE), Damodaran annual returns 1928–2025, ETF prices from 2005. GFD isn't available (no SMU subscription), so these are proxies over the paper's period. Record H0–H3 in two parts (A: H0/H1, B: H2/H3).
**Proves:** our proxy data matches the paper's sources closely enough (e.g. our computed bond returns line up with Damodaran's published ones). State where proxies differ from GFD.
**Conclude:** the tests are fair because the hypotheses were fixed first. Part A says whether the paper's result is real; Part B says whether it should change what an investor holds.
**Paper:** data p.4–5 "Long Dataset"; H1 p.1; Sharpe 0.57 vs 0.31 p.6 "Economic drivers". H0 (null), H2 (as a challenge) and H3 are ours.
**Notebook section:** §1 Data. **Datasets:** `context/06`.

## Step 2 · Replicate the paper (H0 vs H1) and test the Sharpe ratio (H2)
**Do:**
1. Label each month higher/lower-rate with the three rules (M1 full-sample median; M2 trailing 5-yr at 40th pct; M3 centred 5-yr). Rates < 0.5% always lower. **Only M2 may be used by strategies** (no look-ahead).
2. For stocks, Treasuries, corporate bonds and momentum: average return above cash and Sharpe ratio over the next 1, 12, 36 months, higher vs lower regime → **Exhibit 3**. **Test H0 vs H1** with a difference-in-means t-test, Newey-West standard errors (rate levels persist, p.5). **Momentum check:** momentum's return above cash should be about the same in both groups (backs cash-plus, steps 5–6).
3. Regression: excess return_{t+1} on T-bill_t (paper t = −2.2 equities, −2.4 credit).
4. **H2:** equity Sharpe ratio after high- vs low-rate months (paper 0.57 vs 0.31) on 1926–2023, then 1926–2026; significance of the gap by bootstrap.
5. Recompute **Exhibit 9** portfolios from the stated assumptions.
**Proves:** H0 vs H1 (does the paper's result hold on its sample?), H2 (is the gap still there once risk is counted?), and that our method reproduces the paper.
**Conclude:** if H0 is rejected, the pattern really existed in 1926–2023. First pass (Damodaran): stocks 9.1%/yr above cash after low-rate years vs 6.7% after high (paper 10.3% vs 5.8%); same direction, smaller gap. If the Sharpe gap is small (H2 holds), the paper overstates the case for cutting stocks.
**Answers Prof Liu:** point 1.
**Paper:** p.4 rules; fn 4 p.4; p.5 Dec 2023; p.6 Exhibit 3; p.6 Sharpe 0.57 vs 0.31, vol 19.4% vs 17.4%; p.5 t-stats; p.12–13 Exhibit 9.

## Step 3 · Test the fiscal-deficit offset (H3)
**Do:**
1. Check the paper's channel: real EPS growth after low rates **11%/yr** vs **1%** after high (p.6).
2. Split higher/lower months again by the **primary deficit** (deficit minus interest, % of GDP, FRED; big = above its median *to date*). Compare next-12-month earnings growth and stock returns in the 4 groups. **H3 holds** if, after high-rate months, stocks' return above cash and earnings growth are higher when the deficit is big than when small, and close to the low-rate level.
**Proves:** H3: whether a big deficit offsets high rates, keeping profits and stock returns up.
**Conclude:** if yes, high rates alone aren't a reason to sell stocks; may explain 2024–25 (high rates, deficit ≈ 6% of GDP) → strategy **S3**. If no, the paper's explanation stands (H1 with no offset).
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
0. **Data:** longest sample available, monthly Feb 1960 → latest (World Bank gold starts Jan 1960). Equity = Ken French market; bonds = 10Y Treasury return built from the yield (annual corr with Damodaran 0.99); gold = World Bank monthly price; momentum = RF + UMD. Gold fixed at $35 until Aug 1971; kept and disclosed. Notebook §5.
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
1. **Investable ETF backtest, 70/30 chronological split:** SPY, IEF, GLD, PDP (+ PSP, HYG, VNQ for S1), monthly May 2007 → latest. Fit/choose on the first 70% (May 2007 – Nov 2020), judge only on the last 30% (Dec 2020 – Sep 2026, includes the 2022–26 high-rate period). Monthly rebalance, 10 bps costs. Notebook §6.
2. **Monte Carlo** 10-year paths under "rates stay high" vs "rates fall", with high↔low switching odds counted from history (CVaR paper Algorithm 2, `context/04`).

| Code | Strategy | Rule |
|------|----------|------|
| **B** | Benchmark | Equal amounts in SPY, IEF, GLD, PDP, bought once and **never rebalanced**; restarted at equal weights at the start of each period (in-sample, out-of-sample) |
| **S1** | The paper's portfolios (reference) | Exhibit 9 column 2 when rates are low, column 4 when high (SPY, PSP, IEF, HYG, VNQ, PDP for cash-plus) |
| **S2** | Rate rule | 70% SPY / 30% IEF when rates are low (M2), 50/50 when high (the paper's direction) |
| **S3** | Rate + deficit | Like S2, but 60/40 when rates are high **and** the primary deficit is big (H3) |
| **S4** | Optimised by period | Ridge mean-variance weights on SPY, IEF, GLD, PDP from each regime's **in-sample** history (Week 5) |

Summary table per period (in-sample / out-of-sample), as in Assignment 1: **alpha and beta vs the benchmark** (Newey-West t), annual return, annual variance, Sharpe ratio, CVaR 5% (monthly), max drawdown. Dropped: 60/40 (S0), rebalanced 1/N, cash-plus (old S5) and SPY-only. Prof Liu's 60/40 vs 50/50 question is answered in step 5 instead.

**Conclude:** final verdict on the paper and one **central message**: *"Being in the middle doesn't mean retreating to risk-free … the best stock share is around X%."* Rewrite if the evidence says otherwise. **Beating 60/40 is not required**: an honest "no" is valid.
**Answers Prof Liu:** points 2, 4, 10, 12. Beating the benchmark is not required.
**Paper:** p.13 Exhibit 9; p.12 four scenarios; fn 11 Sharpe 0.45/0.36/0.44/0.35; p.14 "more—not less—attractive". CVaR paper: p.17 counting; p.1 1/N benchmark. B, S2–S4 and the simulation are ours; S1 is the paper's Exhibit 9.

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
| Exhibit 9 portfolios | Low-rate: 37% stocks, 17% PE, 18% Treasuries, 10% RE, 19% cash-plus. High-rate: 26% stocks, 10% PE, 33% Treasuries, 3% HY, 28% cash-plus. ETFs from 2007: SPY, PSP, IEF, HYG, VNQ, PDP (momentum) |
| Gold | Low correlation with stocks; held up in 2022. Pays no interest, so looks worse when cash pays well |
| CAPE | S&P 500 price / 10-yr average real earnings. 15–20 typical; > 30 expensive |
| Sharpe vs certainty equivalent | Any stock/cash mix has the same Sharpe, so Sharpe can't size the stock share. CE (Week 1) can |
| Ridge and 1/N | Ridge shrinks MVO weights toward equal; with no return signal it gives exactly 1/N (Week 5) |

## Lecture concept map

| Week | Concept | Used in |
|------|---------|---------|
| W1 | Risk aversion, certainty equivalent | Step 5 stock share |
| W2 | Sharpe, CAL/CML, tangency, w\* = (E[R] − r_f)/(Aσ²) | H2, Exhibit 9, steps 2 and 5 |
| W3 | Regression, t-tests, beta, alpha | H0 vs H1 test, paper regressions, H3, strategy alphas (steps 2–4, 6) |
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
| 2 | §2 Replication (H0 vs H1, H2) | 3 Replication | 3–4 |
| 3 | §3 Deficit offset (H3) | 4 Mechanism | 5 |
| 4 | §4 Out-of-sample | 5 Does it still hold? | 6–7 |
| 5 | §5 Allocation | 6 What to hold | 8–9 |
| 6 | §6 Backtest & simulation | 7 Strategies; 8 Verdict | 10–11 |
| — | — | Exec summary; 1 Problem & impact; 9 Limitations; References; Annexes | 1, 12 (conclusion), Annex |
