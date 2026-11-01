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

## Step 2 · Replicate the paper (H0 vs H1, in and out of sample) and test the Sharpe ratio (H2)
**Do:**
1. Label each month higher/lower-rate with the three rules (M1 full-sample median; M2 trailing 5-yr at 40th pct; M3 centred 5-yr). Rates < 0.5% always lower. **Only M2 may be used by strategies** (no look-ahead).
2. For stocks, Treasuries, corporate bonds and momentum: average return above cash over the next 1, 12, 36 months, higher vs lower regime → **Exhibit 3**. **Test H0 vs H1** with a difference-in-means regression, Newey-West t (rate levels persist, p.5). **Momentum check.**
3. Regression: excess return_{t+1} on T-bill_t (paper t = −2.2 equities, −2.4 credit).
4. **H0 vs H1 in-sample (1926–1995) vs out-of-sample (1996–today)** (feedback 1 Nov 2026: belongs in step 2): same regime-gap test in each period (M1 cut-off = in-sample median), plus the regression fitted on 1926–1995 and tested on 1996–2026 (out-of-sample R²).
5. **H2:** equity Sharpe ratio after high- vs low-rate months on 1926–2023 and 1926–2026; block-bootstrap interval.
6. Recompute **Exhibit 9** from the stated assumptions.
**Answers Prof Liu:** points 1, 2, 5 (do not cite Prof Liu in the deliverables; present as our own analysis).
**Paper:** p.4 rules; p.5 Dec 2023; p.6 Exhibit 3; p.6 Sharpe 0.57 vs 0.31; p.5 t-stats; p.12–13 Exhibit 9.

## Step 3 · Test the fiscal-deficit offset (H3)
**Do:**
1. Check the paper's channel: real EPS growth after low rates **11%/yr** vs **1%** after high (p.6).
2. Split higher/lower months again by the **primary deficit** (deficit minus interest, % of GDP, FRED; big = above its median *to date*). Compare next-12-month earnings growth and stock returns in the 4 groups. **H3 holds** if, after high-rate months, stocks' return above cash and earnings growth are higher when the deficit is big than when small, and close to the low-rate level.
**Proves:** H3: whether a big deficit offsets high rates, keeping profits and stock returns up.
**Conclude:** if yes, high rates alone aren't a reason to sell stocks; may explain 2024–25 (high rates, deficit ≈ 6% of GDP) → strategy **S3**. If no, the paper's explanation stands (H1 with no offset).
**Paper:** p.6 "blistering 11%"; p.7 "Intuitively, it is low". Deficit split and Kalecki are ours.

## Step 4 · Recent years and robustness
**Do:** 2024–2026 on their own; concentration (SPY vs RSP); robustness (simpler rule; CAPE two-factor regression). The in/out-of-sample split moved to step 2.
**Conclude:** rate the claim **true / partly true / false** and explain recent failures with evidence.
**Answers Prof Liu:** points 2, 3.

## Step 5 · What should an investor hold: from findings to backtested strategies (old steps 5 and 6, merged)
**Evidence (long sample, Feb 1960 → latest):** diversifiers by rate state; w\* = (E[R] − r_f)/(Aσ²); 60/40 vs 50/50 vs 1/N by rate state; good/middle/bad thirds → recommended stock share X.
**Strategies (ETFs, May 2007 → latest, 70/30 chronological split, monthly rebalance, 10 bps costs).** Report the paper's strategies on their own first, then all strategies together. Metrics for every strategy: alpha, alpha t (NW), beta vs B, annual return, volatility, variance, Sharpe, CVaR 5%, max drawdown, turnover.

| Code | Strategy | Rule |
|------|----------|------|
| **B** | Benchmark | SPY, IEF, GLD, PDP equal, bought once, never rebalanced; restarted each period |
| **S1** | Paper (Exhibit 9) | Column 2 when low, column 4 when high |
| **S2** | Rate rule | 70/30 SPY/IEF low, 50/50 high |
| **100/0, 70/30, 60/40, 50/50, 1/N** | Fixed mixes | Rebalanced monthly |
| **S3** | Rate + deficit | As S2, 60/40 when high and deficit big |
| **S4** | Ridge MV by regime | η chosen by walk-forward validation inside the in-sample period (10-yr expanding train, 12-month validation windows), refit on full in-sample |

**Monte Carlo:** 10-year paths, rates stay high / fall / always high; B, S2, S3, S4, 60/40, 50/50.
**Answers Prof Liu:** points 4, 6–12.

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
| 1 | §1 Data & hypotheses | 1 Paper; 2 Data; Annex A | 2–4 |
| 2 | §2 Replication, in/out of sample (H0 vs H1, H2) | 3 Replication | 5–7 |
| 3 | §3 Deficit offset (H3) | 4 Mechanism | 8 |
| 4 | §4 Recent years & robustness | 5 Does it still hold? | 9 |
| 5 | §5 What to hold: evidence, strategies, backtests | 6 What to hold; 7 Verdict | 10–16 |
| — | §6 Results export | Exec summary; 1 Problem, paper & impact; 8 Metrics; 9 Limitations; References; Annexes | 1, 16 (conclusion), Annex A–C |
