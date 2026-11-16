# Report text for the SABR sections

Paste into `QF620 Project Report Local.docx`, replacing the "[To do]" lines under 2.5 and 3.3. The figures come from notebook Sections 3.4 and 3.5; the table comes from Section 3.3.

---

## 2.5 Stochastic Volatility Model (SABR)

The SABR model (Hagan et al., 2002) lets volatility itself follow a random process that is correlated with the forward price:

dF = α F^β dW^F,  dα = ν α dW^α,  dW^F dW^α = ρ dt

Each parameter controls one feature of the smile. α sets the overall level of volatility, close to the at-the-money vol once scaled by F^(1−β). ρ is the correlation between price and volatility: a negative ρ means volatility rises when the market falls, which makes low-strike puts dearer and produces the skew. ν, the volatility of volatility, lifts both wings and controls the curvature. β sets how volatility scales with the price level.

We use Hagan's closed-form approximation for the SABR implied Black volatility (Session 6), implemented as in the course reference `calibration (full).ipynb`. Since F = S e^(rT), this Black volatility is directly comparable with the Black-Scholes implied vols from Section 2.3.

**Calibration.** For each snapshot we take the market smile, forward F and time to expiry T from Section 2.3. We then choose α, ρ and ν to minimise the sum of squared differences between market and SABR implied vols across strikes, using `scipy.optimize.least_squares`. β is fixed at 0.7, as in the course reference. β and ρ both tilt the smile, so fitting both at once is unstable, and a check with β = 0.5 and β = 1 changed the fit error by less than 0.1 vol points at every snapshot. Options with a mid price below $0.50 are left out of the fit, because at a few ticks their price reflects the minimum price step and bid-ask spread rather than volatility. Fit quality is the root-mean-square error (RMSE) across strikes, in vol points.

**Snapshots.** We calibrate at the ten daily snapshots used for the smile (minute closest to 16:00 ET), plus six event moments:
- 20:20 on 2 April, the first overnight minute after the announcement
- 10:05, 10:18 and 10:30 on 7 April: before the false 90-day pause report, at the peak of the rally on it, and after the White House denial
- 13:15 and 13:30 on 9 April: before and after the real pause at 13:18

---

## 3.3 SABR Calibration

**Table X. Calibrated SABR parameters (β = 0.7)**

| Snapshot (ET) | Moment | Expiry | ATM vol | ρ | ν | RMSE (vol pts) |
|---|---|---|---|---|---|---|
| Tue 01 Apr 16:00 | Daily close | 16 Apr | 19.3% | −0.67 | 3.56 | 1.04 |
| Wed 02 Apr 16:00 | Daily close | 16 Apr | 19.1% | −0.68 | 3.85 | 1.02 |
| Wed 02 Apr 20:20 | After announcement | 16 Apr | 25.1% | −0.74 | 3.35 | 1.02 |
| Thu 03 Apr 16:00 | Daily close | 16 Apr | 27.6% | −0.75 | 3.37 | 0.73 |
| Fri 04 Apr 16:00 | Daily close | 16 Apr | 45.3% | −0.76 | 4.02 | 0.61 |
| Sun 06 Apr 20:15 | Overnight open | 15 May | 45.9% | −0.78 | 2.78 | 0.52 |
| Mon 07 Apr 10:05 | Before false report | 15 May | 38.5% | −0.79 | 2.44 | 0.12 |
| Mon 07 Apr 10:18 | Peak of false rally | 15 May | 29.5% | −0.75 | 2.53 | 0.49 |
| Mon 07 Apr 10:30 | After denial | 15 May | 38.1% | −0.77 | 2.63 | 0.42 |
| Mon 07 Apr 16:00 | Daily close | 15 May | 36.7% | −0.75 | 2.55 | 0.59 |
| Tue 08 Apr 16:00 | Daily close | 15 May | 39.9% | −0.79 | 2.62 | 0.37 |
| Wed 09 Apr 13:15 | Before pause | 15 May | 38.9% | −0.85 | 2.34 | 0.30 |
| Wed 09 Apr 13:30 | After pause | 15 May | 30.8% | −0.76 | 2.62 | 0.99 |
| Wed 09 Apr 16:00 | Daily close | 15 May | 25.1% | −0.73 | 2.89 | 0.60 |
| Thu 10 Apr 16:00 | Daily close | 15 May | 33.0% | −0.79 | 2.76 | 0.65 |
| Fri 11 Apr 09:15 | Overnight close | 15 May | 35.8% | −0.83 | 2.76 | 0.49 |

ATM vol is the SABR vol at K = F, shown in place of α because it is easier to read.

SABR fits the smiles closely (Figure X). The RMSE is 0.1–0.6 vol points on most 15 May snapshots and 0.6–1.0 points on the shorter 16 April options. Figure Y shows how the parameters moved:

- **Level.** ATM vol rose from 19% before the announcement to 25% overnight, 28% on 3 April and 45% on 4 April. It fell from 39% to 31% within 12 minutes of the 9 April pause, and to 25% by the close.
- **Skew.** ρ became more negative as the shock spread: −0.67 before the announcement, −0.74 about four hours after it, and −0.76 by 4 April. It reached its most negative value, −0.85, three minutes before the pause. The market was paying the most for crash protection just before the relief arrived. ρ then flattened to −0.73 by the 9 April close, and steepened again on 10–11 April as the China escalation remained.
- **Vol of vol.** ν is mainly driven by maturity: 3.3–4.0 on the two-week 16 April options against 2.3–2.9 on the five-week 15 May options. Within the May expiry, ν rose from 2.34 before the pause to 2.89 at the close: after the pause, the market paid more for large moves in both directions.
- **False report.** On 7 April, ATM vol fell from 38.5% to 29.5% at the peak of the rally on the false pause report, and was back at 38.1% by 10:30, after the White House denial. Option prices treated the rumour as real and then fully reversed. The real pause produced a similar first move but kept going.

**Verdict.** With three parameters, SABR describes each snapshot's smile to within about one vol point, and its parameters separate the phases of the event clearly. Its weaknesses:
- The two-week smiles on 1–2 April bend more sharply near the money than SABR allows, and SABR's ATM vol is 1.1–1.3 points too low there.
- The fit is worst in the minutes after the pause (max error 3.9 points), when quotes were repricing quickly.
- SABR assumes ρ and ν are constant, yet here they had to be recalibrated at every snapshot and sometimes moved sharply within 15 minutes.

So SABR is a good description of each smile, but not of how the smile moved through the event.

**Limitations to add to Section 5:** comparisons across the change of expiry (4 April → 6 April) mix the event with the change of maturity; F assumes no dividends, which leaves a small step between put and call vols at K = F on some May snapshots.
