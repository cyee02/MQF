# 10 · Prof Liu's feedback and our next steps

Source: user-supplied note "Prof Liu's Feedback + Next Steps" (pasted 1 Nov 2026). Prof's words are quoted verbatim. "Next step" is the group's plan. The coverage map at the bottom is what `qf600-sync-check` tests (check 8): every point must appear in ≥ 1 report section and ≥ 1 slide.

---

**1. On the paper**
> Prof: "this paper is ok, direction is ok"

Next step: keep the current paper and direction.

**2. If thesis holds**
> Prof: "if the thesis recent years stay true, can try to optimise the paper's strategy to get even more returns"

Next step: test the thesis on recent years' data. If it holds, tweak the strategy to improve returns. Example: adjust the equity % based on the rate environment instead of keeping it fixed.

**3. If thesis fails**
> Prof: "if its false, explain"

Next step: explain what changed in the data or market that broke the thesis.

**4. Future rate increases**
> Prof: "what can we do in future if we expect interest rate to increase? (E.g. if now we use 60/40, can we improve by using 50/50 in future? Will the expected return increase)"

Next step: compare 60/40, 50/50 and 70/30 in high-rate vs low-rate periods (return, volatility, Sharpe, drawdown). Portfolio return = w × stock return + (1 − w) × r_f. Higher r_f means the bond/cash portion earns more, so 50/50 may cost little return but cut risk. Example: Monte Carlo of "rates stay high" vs "rates fall", comparing 60/40 vs 50/50 (our idea, not Prof's).

**5. Out-of-sample**
> Prof: "out of sample test"

Next step: chronological split (e.g. 70/30), no shuffling. Better: walk-forward (train 10 yrs, test the next yr, roll forward). This also covers the "iterative trial-and-error" objective (guideline R0.3).

**6. Shrinking + portfolio impact**
> Prof: "what can we do that i is shrinking now, how does it impact our portfolio, their investment strategies"

Feedback note's reading: "i is shrinking" = the equity risk premium shrinking. **Walkthrough (settled question) reads it as interest rates falling.** We cover both: falling-rate periods get their own comparison (step 5), and w\* sensitivity to a shrinking ERP is shown under point 7. **To confirm with Prof.**
Core question: if bonds and cash now pay more, how much should we still put in stocks?
Next step: show how the shrinking affects our portfolio and typical strategies.

**7. Mean-variance + central message**
> Prof: "mean variance impact is what on the suggestions, central message"

Optimal risky weight w\* = (E[R] − r_f) / (A × σ²). If the premium shrinks, w\* falls, but only slightly if the Sharpe ratio holds up (Jim's deficit point). This links to our view that we shouldn't underweight equities just because rates are high.
Next step: state what mean-variance says about our suggested allocation and give one clear central message.

**8. Risk-free or risky? How to change %?**
> Prof: "shall we just do investment in the risk free or choose risky? how should I change my % now that it is no longer 50-50, real investment perspective what can we do?"

Next step: recommend a specific risky % from a practical investor's view. Example: test risky weights from 0% to 100% in 10% steps and see which gives the best Sharpe. *(Note: for a stock/cash mix Sharpe is flat in w. Use certainty equivalent or a stock/bond mix. See `context/02` Key terms.)*

**9. Good market vs middle**
> Prof: "most likely when the market is good, invest in risky, now it is in the middle, everyone knows, 100% risky, we can do some analysis on this etc"

Good market: 100% risky. Bad market: risk-free. Middle (now): needs analysis.
Next step: split history into good / middle / bad regimes using the equity risk premium, the r_f level or the deficit variable, in thirds. For each regime, test risky weights 0–100% and report return, volatility, Sharpe, max drawdown and CVaR. Where the Sharpe peaks in the middle regime is our answer to "how should I change my %". Then check which regime today falls in, using the latest FRED data.

**10. CVaR**
> Prof: "cvar is only a number that can calculate, based on the strategy we propose we can do corresponding cvar, its just a number to report"

Next step: calculate CVaR (average loss in the worst 5% of months) for each strategy and report it. No need to optimise with it.

**11. Typical strategies under rising r_f**
> Prof: "given that the risk free is rising, what is the implication of typical strategy? equal weighted? what is the impact on it"

Equal-weighted 1/N: weights don't adjust. Cash earns more; bonds lose value during hikes then earn more; the equity premium shrinks. Equal-weighted stocks: mixed. Small caps hurt, value tilt helps; in 2022 the equal-weighted S&P fell less than cap-weighted. Need to test. 60/40: the bond cushion can fail when rates rise fast (2022: stocks and bonds fell together).
Next step: backtest 100% equity, 60/40, 50/50, 1/N and our strategy across rising, high-stable and falling rate periods.

**12. What can be done better**
> Prof: "what can be done to better"

Next step: propose improvements to the paper's strategy, e.g. adjusting allocation by rate regime, and show whether it beats the original.

---

## Coverage map

Report sections and slides are indicative. `qf600-report` / `qf600-slides` update the last two columns as the files take shape.

| Point | Walkthrough step | Notebook § | Report section | Slide(s) |
|-------|-----------------|-----------|----------------|----------|
| 1 Paper direction ok | 2 | §2 | 3 Replication | 4–5 |
| 2 If holds → optimise | 4, 6 | §4, §6 | 5, 7 | 7, 10 |
| 3 If fails → explain | 4 | §4 | 5 | 7 |
| 4 Rate increases: 60/40 vs 50/50 | 5, 6 | §5, §6 | 6, 7 | 8, 11 |
| 5 Out-of-sample | 4, 6 | §4, §6 | 5, 7 | 7, 10 |
| 6 "i is shrinking" | 5 | §5 | 6 | 8 |
| 7 MV + central message | 5 | §5 | 6, 8 | 9, 12 |
| 8 Risky % | 5 | §5 | 6 | 9 |
| 9 Good / middle / bad | 5 | §5 | 6 | 9 |
| 10 CVaR | 5, 6 | §5, §6 | 6, 7 (all tables) | 8, 10 |
| 11 Typical strategies, rising r_f | 5 | §5 | 6 | 8 |
| 12 Do better | 6 | §6 | 7, 8 | 10–12 |
