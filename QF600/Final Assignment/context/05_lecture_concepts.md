# 05 · Lecture concepts (QF600, Prof Liu Peng)

Source: `course_materials/lecture_notes/Session 1–9.pdf` (gitignored, in the team bundle). Refs are **Lecture n, slide p** (the PDF page). Use the lecture's notation in the report so markers recognise it.

Course arc (L1 p3): W1 Expected utility · W2 Efficient frontier · W3 CAPM · W4 Multi-factor · W5 Portfolio construction · W6 SDF · W7 Multi-period · W8 Behavioural / estimating the SDF · W9 Review (deck titled "Course Review") · W10 Relative valuation. Project presentations in W9–10.

---

## Week 1 · Expected utility (L1)

| Concept | Formula / statement | Ref |
|---------|--------------------|-----|
| Expected utility | E[U(x)] = Σ pᵢ U(xᵢ). Rank options by it, not by E[x] | L1 p19 |
| Concave = risk-averse | U′ > 0, U″ < 0. Jensen: U(E[X]) ≥ E[U(X)] | L1 p26–28 |
| Certainty equivalent / risk premium | U(W − πₐ) = E[U(W + ε̃)]; πₐ ≈ ½ σ² Rₐ(W) | L1 p30–33 |
| Absolute risk aversion | Rₐ(W) = −U″(W)/U′(W) | L1 p33 |
| Relative risk aversion | Rᵣ(W) = −W U″(W)/U′(W); πᵣ ≈ ½ σ² Rᵣ | L1 p34 |
| Utility families | Quadratic (IARA, avoid) · Exponential (CARA) · **Power** W^{1−γ}/(1−γ): CRRA, the workhorse; log = γ→1 | L1 p37–42 |
| Mean-variance from utility | 2nd-order Taylor: E[U(R̃)] ≈ U(μ) + ½ σ² U″(μ) | L1 p44 |
| Skewness | Investors like positive skew, pay to avoid negative skew; MV is blind to both | L1 p51–52 |

**Project use:** certainty equivalent picks the stock share (Sharpe can't, because a stock/cash mix has the same Sharpe at any weight). CE of portfolio p ≈ μ_p − ½ A σ_p².

## Week 2 · Efficient frontier (L2)

| Concept | Formula | Ref |
|---------|---------|-----|
| MV utility | **U = E(r) − ½ A σ²** | L2 p21 |
| Portfolio mean / variance | μₚ = wᵀμ; σₚ² = wᵀΣw | L2 p8, p29 |
| Estimators | μ̂ = (1/T) Σ rₜ; σ̂² = (1/(T−1)) Σ (rₜ − μ̂)² | L2 p5 |
| Rolling window | Short N responsive/noisy; long N smooth/laggy | L2 p6 |
| μ is hard to forecast, σ is easy | Vol clusters and persists; mean return is mostly noise | L2 p13 |
| Cash + one risky asset | μₚ = w μ + (1 − w) r_f; σₚ = w σ (straight line) | L2 p27 |
| Min-variance portfolio | w\* = Σ⁻¹1 / (1ᵀΣ⁻¹1) | L2 p36 |
| Sharpe ratio | (μₚ − r_f)/σₚ = slope of the line from cash | L2 p35 |
| With a riskless asset | μₚ = R_f + wᵀ(μ − R_f e). "Only the excess over cash matters" | L2 p52 |
| CML | μₚ = R_f + σₚ √H_S, H_S = (μ − R_f e)ᵀ Σ⁻¹ (μ − R_f e) = tangency Sharpe² | L2 p53–54 |
| Two-fund separation | Any frontier portfolio = mix of two frontier portfolios | L2 p45–47 |

**Optimal risky share** (MV investor, one risky asset + cash): **w\* = (E[R] − r_f) / (A σ²)**. Used in step 5; Prof point 7. If the premium shrinks, w\* falls in proportion; if σ also falls, less so.

## Week 3 · CAPM (L3)

| Concept | Formula | Ref |
|---------|---------|-----|
| CAPM | μᵢ = R_f + βᵢ(μ_M − R_f) | L3 p3 |
| Regression form | R̃ᵢ − R_f = αᵢ + βᵢ(R̃_M − R_f) + ε̃ᵢ; CAPM predicts α = 0 | L3 p6, p11 |
| Beta | βᵢ = Cov(R̃ᵢ, R̃_M)/Var(R̃_M); portfolio β = Σ wᵢ βᵢ | L3 p19, p40 |
| Which R_f? | **Match the horizon**: 3-month T-bill for short-term decisions; 10-yr for 10-yr valuations | L3 p15 |
| Variance split | σᵢ² = βᵢ² σ_M² + σ²_ε; R² = systematic share | L3 p50–51 |
| Estimation caveats | α not in theory, estimating it is the test; M is proxied; α, β have standard errors | L3 p53 |
| Negative β assets | Expected return below R_f; rational as insurance (e.g. gold in some regimes) | L3 p42 |
| HW1 recipe | Pick universe → strategy → rolling backtest → return, vol, Sharpe, MDD vs buy-and-hold → regress on market, is α significant? | L3 p55 |

## Week 4 · Factor models (L4)

| Concept | Formula / statement | Ref |
|---------|--------------------|-----|
| K-factor model | R̃ᵢ − R_f = αᵢ + Σ βᵢₖ F̃ₖ + ε̃ᵢ | L4 p5, p7 |
| Traded factor premium | λₖ = E[F̃ₖ] (its own average return) | L4 p9, p11 |
| Fama–MacBeth | Time-series βs → cross-sectional slopes each period → average | L4 p12 |
| FF3, Carhart 4 | + SMB, HML; + **UMD** (long winners, short losers, rebalanced monthly) | L4 p18, p25, p29 |
| Ken French Data Library | Mkt−RF, SMB, HML, RMW, CMA, Mom; daily/weekly/monthly/annual; **US from July 1926**; CSV in zip; values in % | L4 p19–20 |
| Momentum pattern | Winners keep winning ~1 year, then reverse (3–5 yr) | L4 p28 |
| **Four tests for any new signal** | (1) Out of sample? (2) Why should it pay (risk or bias story)? (3) Already known / spanned by existing factors? (4) Survives costs? Demand **t > 3.0** (Harvey–Liu–Zhu 2016) | L4 p32–36 |
| Net alpha | Net α = gross α − turnover × cost | L4 p36 |

**Project use:** apply the four tests to the rate signal and the deficit signal (step 4); momentum as cash-plus (H2).

## Week 5 · Advanced portfolio construction (L5)

| Concept | Formula | Ref |
|---------|---------|-----|
| Error maximiser | w\* = (1/λ) Σ⁻¹μ ⇒ Δw = (1/λ) Σ⁻¹Δμ; 1 pp change in μ moved a weight 64 pp (ρ = 0.95 example) | L5 p8–9 |
| **Ridge** | max μ̂ᵀw − (λ/2) wᵀΣ̂w − (η/2)‖w‖² ⇒ **w\* = (λΣ̂ + ηI)⁻¹ μ̂** | L5 p14–15 |
| No signal ⇒ 1/N | min ‖w‖² s.t. 1ᵀw = 1 ⇒ wᵢ = 1/N | L5 p17 |
| Robust optimisation | Ellipsoidal uncertainty on μ ⇒ shrink the tilt: w = w₀ · max(0, 1 − κ/t) | L5 p20–21 |
| **Trading costs** | max μ̂ᵀw − (λ/2)wᵀΣ̂w − τ‖w − w⁻‖₁ (no-trade region); backtest net = gross − turnover × bps/1e4 | L5 p23–24 |
| Factor-neutral | max αᵀw − (λ/2) wᵀDw s.t. Bᵀw = 0; Σ = BΩBᵀ + D | L5 p29–35 |
| Long-only can't be factor-neutral | Use relative neutrality Bᵀ(w − b) = 0 | L5 p37 |
| Tracking error | TE² = aᵀΣa = (Bᵀa)ᵀΩ(Bᵀa) + aᵀDa, a = w − b | L5 p41–44 |

**Project use:** S1 (1/N), S4 (ridge MVO by regime), Exhibit 9 sensitivity, all backtests net of costs (state the bps assumption).

## Week 6 · Stochastic discount factor (optional, L6)

| Concept | Formula | Ref |
|---------|---------|-----|
| Problem | max U(C₀) + δ E[U(C̃₁)] | L6 p9–11 |
| Euler equation | E[ δ U′(C̃₁)/U′(C₀) · R̃ᵢ ] = 1 | L6 p14 |
| SDF | M̃ = δ U′(C̃₁)/U′(C₀); large in bad states | L6 p15–16 |
| Pricing | Pᵢ = E[M̃ X̃ᵢ]; for the riskless asset **E[M] = 1/R_f** | L6 p16; L9 p26–28 |
| Risk premium | Set by covariance with M: E[Rᵢ] − R_f = −R_f Cov(M, Rᵢ) | L9 p28 |

**Project use:** one paragraph of intuition. A higher R_f means a lower E[M]. The ERP depends on Cov(M, R), not on R_f, so nothing forces the ERP to stay constant when R_f rises.

## Weeks 7–9 (context only)
- L7 multi-period: value function, backward induction, multi-period SDF M_{t,t+i} = Π M (L7 p8–13).
- L8 estimating the SDF from data (ML/network approach) (L9 p33–35).
- L9 course review: one-slide summaries of W1–W8. Use it as a quick reference for notation.
