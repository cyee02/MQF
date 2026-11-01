# 03 · Target paper: Maloney (2024), "Honey, the Fed Shrunk the Equity Premium"

**Citation:** Maloney, T. (2024). "Honey, the Fed Shrunk the Equity Premium: Asset Allocation in a Higher-Rate World." *The Journal of Portfolio Management*, 50(6), April 2024. AQR Capital Management, London.
**File:** `reference_paper/Equity Risk Premium Higher Rate Regime.pdf` (18 PDF pages, journal pages 1–16; gitignored, in the team bundle).
**Page references** below use the page number **printed on the paper** (as the walkthrough does), plus a search phrase.

---

## 1. Research question and claims

*Should the level of the risk-free rate change asset allocation?* (p.1–2). Two channels:
1. Excess-of-cash returns depend on the cash rate in a systematic way → optimal allocations change (**the paper's focus**).
2. Even with constant excess returns, constrained investors face different trade-offs (e.g. a return target is easier to hit when cash pays more) → covered in the Exhibit 9 case study.

**Key findings box (p.1, "Equity markets have historically delivered"):**
- Equities earned **smaller excess returns when cash rates were higher**, consistent with yield-based forecasts that the ERP shrank in 2021–2024.
- Private assets behave like equities. **Liquid alternatives** (large cash holdings) earned **similar excess returns in both regimes**.
- If every asset's expected return moved in parallel with cash, higher rates would make investing easier. History says they don't. **Cash-plus liquid alternatives gain a relative advantage.**

**Conclusion (p.13–14, "more—not less—attractive"):** equities and illiquid alternatives underperformed when cash rates were higher; bonds passed the cash rate through better; liquid alternatives did best. **Caveat: "Market timing is difficult"**: scale tactical tilts by conviction; strategic diversification is the best defence.

**Rates outlook (p.2–4, Exhibit 1):** the average of forecasts puts the fed funds rate **+320 bps** higher over the 10 years after 2022–23 than the 12 years before (eurozone +300 bps, UK +380 bps). The forecast average gives a random walk ¼ weight (fn 3).

---

## 2. Data used by the paper (what we must source or proxy)

### 2a. Long dataset: Jan 1926 – Dec 2023, monthly (p.4–5, "Long Dataset")

**GFD is not available to us:** SMU has no subscription to Finaeon / Global Financial Data, and the free trial covers only US stocks from 2019. Every GFD series below uses the listed proxy, over the paper's sample (monthly, Jan 1926 – Dec 2023).

| Series | Paper's source | Frequency | Period | Our source (see `context/06`) |
|--------|---------------|-----------|--------|-------------------------------|
| 3-month T-bill rate | Federal Reserve from 1934; Global Financial Data (GFD) short rates 1926–1933 | Monthly | 1926–2023 | FRED `TB3MS` (from 1934) + Ken French `RF` (1-month T-bill, from Jul 1926) to back-fill 1926–33 |
| US equity returns | GFD | Monthly | 1926–2023 | Ken French `Mkt-RF` + `RF` (CRSP value-weighted, from Jul 1926) |
| US Treasury bond returns | GFD | Monthly | 1926–2023 | Damodaran annual T-bond returns (1928–2025) for the long check; FRED `GS10` yield → approximate monthly bond return (duration approximation); IEF ETF from 2002 |
| US IG corporate credit excess returns (over duration-matched Treasuries) | Asvanunt & Richardson (2017) | Monthly | 1926–2023 | Damodaran annual Baa corporate returns (1928–2025) minus T-bond; FRED `BAA`/`AAA` yields for a monthly approximation |
| Real EPS, CAPE | Robert Shiller data library | Monthly | 1926–2023 | Shiller `ie_data.xls` |
| S&P 500 (Exhibit 4) | GFD | Monthly | 1926–2023 | Shiller price series / Ken French market |

### 2b. Broad dataset: Jan 1990 – Dec 2023, monthly (p.7, "Broad Dataset")

| Asset | Paper's source | Our proxy |
|-------|---------------|-----------|
| US equities, Treasuries, IG credit | as above / Bloomberg | as above |
| Private equity | hedge fund / PE index (Bloomberg) | PSP ETF (listed private equity, from 2006) |
| Real estate | Bloomberg index | VNQ ETF (from 2004) |
| Equity market neutral | hedge fund index | not available free. Momentum UMD (Ken French) is our cash-plus stand-in |
| Trend following | hedge fund index | not available free. Momentum UMD stand-in (DBMF from 2019 as a sanity check only) |

Rolling-regime threshold drops from the **40th to the 30th percentile** for this shorter sample (fn 7). Commodities were tested with mixed results (fn 7). Broad hedge-fund indices inherit equity's preference for low rates (fn 8).

### 2c. Exhibit 9 inputs
Volatilities and correlations from **monthly historical proxy data, Jan 1990 – Jun 2023**. Sharpe ratios assumed (0.3 for major asset classes, adjusted for breadth). See §5.

---

## 3. Regime definitions (p.4, "Rolling categorization"; fn 4)

Three rules label each month **higher-rate** or **lower-rate** using the 3-month T-bill rate:

| Rule | Definition | Look-ahead? | Use |
|------|-----------|-------------|-----|
| **M1 Full-sample** | Higher if rate > **median of the full 1926–2023 sample** | Yes (full sample) | Replication only |
| **M2 Rolling trailing** | Compare the rate to the **trailing 5-year window** (60 months) | **No** | Replication **and the only rule our strategies may use** |
| **M3 Rolling centred** | Compare to the **5-year window centred** on the month (±30 months) | Yes (needs future data) | Replication only. Not biased toward rising-rate periods |

**Footnote 4 adjustments (rolling rules M2, M3):**
- Any rate **< 0.5% is always "lower"**.
- Because of that floor, the threshold moves from the median to the **40th percentile** of the window (≈ equal counts of higher/lower months). The long dataset uses 40%; the broad (1990+) dataset uses **30%** (fn 7).
- "The main patterns are not sensitive to these choices."

**Check:** **December 2023 is "higher" under all three rules** (p.5, "classified as higher rates by all three").

Exhibits 3 and 6 report the **average across the three rules** (and Exhibit A1 breaks them out).

**Horizons:** returns are measured **starting in** each regime over the next **1, 12 and 36 months**, annualised (p.5, Exhibit 3).

---

## 4. Results to replicate (replication targets)

Notebook section numbers are placeholders until the notebook is built. **Tolerance** is how close our number needs to be to count as "replicated" given different data sources.

### 4a. Exhibit 3: excess-of-cash returns by regime, 1926–2023 (p.6)

Panel A, annualised average excess-of-cash return, **average of the three rules**. Values are read from the bar chart and cross-checked against the Exhibit A1 differences (p.15):

| Asset | Horizon | Lower rates | Higher rates | Diff (A1) |
|-------|---------|-------------|--------------|-----------|
| US equities | 1M | 11.4% | 4.9% | −6.5% |
| US equities | 12M | 10.3% | 5.8% | −4.5% |
| US equities | 36M | 10.4% | 5.5% | −4.8% |
| US Treasuries | 1M | 2.2% | 0.6% | −1.6% |
| US Treasuries | 12M | 1.5% | 1.2% | −0.4% |
| US Treasuries | 36M | 1.7% | 1.2% | −0.5% |
| US IG credit (excess of Treasuries) | 1M | 3.0% | 0.7% | −2.3% |
| US IG credit | 12M | 2.6% | 1.1% | −1.5% |
| US IG credit | 36M | 2.3% | 1.3% | −1.0% |

Panel B (averaged over 1M/12M/36M): cash **1.8% → 5.2%** nominal (lower → higher regime); cash real **−0.6% → 1.7%**. Inflation ≈ 1 pp higher after high rates. Equity total nominal *and* real returns are **lower** after high rates; bond total returns are slightly higher.

**Tolerance:** sign of every difference must match; equity gap within ±2 pp. (Our Damodaran first pass: 9.1% vs 6.7% annual; paper 10.3% vs 5.8% → same direction, smaller gap.)

### 4b. Risk and fundamentals (p.6–7, "blistering 11%")

| Statistic | After lower rates | After higher rates |
|-----------|------------------|--------------------|
| Equity volatility | 19.4% | 17.4% |
| Equity Sharpe ratio | **0.57** | **0.31** |
| Real EPS growth, arithmetic (Shiller) | **11%** | **1%** |
| Real EPS growth, geometric | 5.8% | −1.1% |
| T-bill change next 12M | +29 bps | −27 bps |
| T-bill change next 36M | +63 bps | −73 bps |

Averaged over 1/12/36-month horizons (fn 5).

### 4c. Regressions (p.5 "statistically significant negative"; p.7 "two-factor regression")

| Regression (monthly) | Result |
|---------------------|--------|
| Excess return on starting T-bill rate: **equities** | t = **−2.2** |
| Same: **IG credit** | t = **−2.4** |
| Same: Treasuries | not significant |
| Equities on T-bill rate **and 1/CAPE** | t = **−3.2** (rate), **+3.9** (1/CAPE) |

Correlation between T-bill rate and 1/CAPE: **+0.3** (Exhibit 4, Panel A). Controlling for subsequent rate *changes* makes the level effect stronger (p.7, "Another interacting factor").
**Paper's own caveat:** t-stats are questionable because rate levels are persistent, so observations are "not serially independent" (p.5). → We report Newey-West t-stats alongside OLS.
Fitted premium in Exhibit 4 Panel B is **in-sample** and "probably exaggerated" at end-2023 (fn 6, "market timing is difficult").

### 4d. Exhibit 6: broad dataset 1990–2023 (p.10)

Average excess-of-cash return (avg of 3 rules × 3 horizons), lower → higher:

| Asset | Lower | Higher | Diff (A1 Panel B) |
|-------|-------|--------|-------------------|
| US equities | 11.3% | 5.5% | −5.8% |
| US Treasuries | 2.3% | 3.3% | +1.0% |
| US IG credit | 2.0% | −0.4% | −2.4% |
| Private equity | 14.4% | 7.0% | −7.4% |
| Real estate | 9.4% | 3.2% | −6.2% |
| Equity market neutral | 2.6% | 2.9% | +0.3% |
| Trend following | 4.4% | 6.4% | +2.0% |

Panel B total returns: cash 1.2% → 4.0%; trend 5.7% → 10.5%; EMN 3.8% → 7.0%.
**Tolerance:** we replicate only the equity / Treasury rows and the **momentum-as-cash-plus** analogue (sign: momentum's excess return roughly equal across regimes).

### 4e. Yield-based expected returns (p.11–12, Exhibit 8; fn 9)
1926–2023 yield-based ERP: **4.2%** (lower) vs **2.3%** (higher); Treasuries 0.7% vs 0.3%. Alt risk premia assumed SR 0.36, vol 7.3%. *Context only. Not replicated.*

---

## 5. Exhibit 9: asset allocation case study (p.12–13, "We start with a theoretical")

Max-Sharpe portfolios under four assumption sets. Weights read from the stacked bars (columns may not sum to exactly 100% because of rounding in the chart):

| Asset | (1) Theoretical unconstrained max SR | (2) Lower-rate world: 3% real target, real cash −0.5% | (3) Higher-rate S1: 3% real target, real cash +0.5%, same SRs | (4) Higher-rate S2: 3% real target, real cash +0.5%, adjusted SRs |
|-------|------|------|------|------|
| Public equity | 13% | **37%** | 24% | **26%** |
| Private equity | — | **17%** | 1% | **10%** |
| Treasuries | 55% | **18%** | 45% | **33%** |
| HY bonds | 9% | — | 2% | **3%** |
| Real estate | 5% | **10%** | 9% | — |
| Liquid alts | 17% | **19%** | 18% | **28%** |
| Implied Sharpe (fn 11) | **0.45** | **0.36** | **0.44** | **0.35** |

Walkthrough mapping: **"low-rate portfolio" = column 2; "high-rate portfolio" = column 4** (strategy S6).

**Assumptions table (p.13):**

| Asset | Volatility | Normal SR | Higher-rate SR adj. |
|-------|-----------|-----------|---------------------|
| Public equity | 15% | 0.30 | −0.06 |
| Private equity | 20% | 0.275 | −0.06 |
| Treasuries | 5% | 0.30 | — |
| HY bonds | 10% | 0.275 | −0.03 |
| Real estate | 10% | 0.275 | −0.06 |
| Liquid alts | 8% | 0.25 | — |

**Correlations:**

|  | Pub Eq | Priv Eq | Treas | HY | RE |
|--|--------|---------|-------|----|----|
| Private equity | 0.9 | | | | |
| Treasuries | 0.0 | 0.0 | | | |
| HY bonds | 0.7 | 0.7 | 0.0 | | |
| Real estate | 0.5 | 0.6 | 0.2 | 0.6 | |
| Liquid alts | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 |

Column 2 puts > 50% of capital (≈ 75% of risk) in public + private equity to hit the 3% real target ("reach for yield", Hau & Lai 2016). Scenario 1 = "a higher-cash-rate tide lifts all boats" (+1% real return for all assets). Scenario 2 = SR penalties → more liquid alts.
**Important:** Exhibit 9 is built from **assumed** inputs and **never backtested** in the paper. Our step 6 tests it on ETF data (SPY, PSP, IEF, HYG, VNQ, momentum for liquid alts).

---

## 6. Cash-plus mechanism (p.9, "two different mechanisms")
Liquid alts keep large T-bill holdings: (1) **long/short financing**: short proceeds fund longs, so the portfolio earns cash + (longs − shorts) − financing spread; (2) **derivatives**: exposure via futures, collateral sits in cash. So return ≈ cash rate + active premium. **Fees:** performance fees on total return (0% hurdle) take ~40% of excess return when cash = 5% (Exhibit 7: 5% gross excess, 20% fee). Fees should be charged above a cash hurdle.
→ **UMD momentum** is self-financing (long winners, short losers), so `RF + UMD` is our cash-plus proxy.

---

## 7. What is ours, not the paper's (from the walkthrough)
- H3 deficit / Kalecki profits channel; deficit split of regimes.
- 1926–1995 / 1996–2026 out-of-sample split; 2024–26 check; simpler "rate > 5-yr average" rule.
- Gold; 60/40 vs 50/50 vs 70/30; good/middle/bad terciles; strategies S0–S5; Monte Carlo of "rates stay high" vs "rates fall".
- Equal-weight vs cap-weight S&P (RSP vs SPY) for the concentration explanation.

## 8. Quick search phrases (for checking the PDF)
| Topic | Page | Search |
|-------|------|--------|
| Key findings | 1 | "Equity markets have historically delivered" |
| Three regime rules | 4 | "Rolling categorization" |
| 0.5% floor, 40th percentile | 4 fn 4 | "less than 0.5%" |
| Data sources | 4–5 | "Long Dataset" |
| Dec 2023 all-three higher | 5 | "classified as higher rates by all three" |
| Regression t-stats | 5 | "statistically significant negative" |
| Serial dependence caveat | 5 | "not serially independent" |
| Exhibit 3 | 6 | "Leaner Compensation for Risk" |
| EPS 11% vs 1% | 6 | "blistering 11%" |
| Why low rates help profits | 7 | "Intuitively, it is low" |
| CAPE two-factor | 7 | "two-factor regression" |
| Rising rates interaction | 7 | "Another interacting factor" |
| Broad dataset | 7 | "Broad Dataset" |
| Exhibit 4 | 8 | "Toxic Combination" |
| Cash-plus mechanisms | 9 | "two different mechanisms" |
| Exhibit 6 | 10 | "Maintained Their Edge" |
| Exhibit 9 description | 12 | "We start with a theoretical" |
| Sharpe 0.45/0.36/0.44/0.35 | 12 fn 11 | "implied Sharpe ratio" |
| Exhibit 9 + assumptions | 13 | "Optimal Capital Allocations" |
| Market timing caveat | 14 | "Market timing is difficult" |
| Exhibit A1 | 15 | "Excess-of-Cash Return Difference" |
