# Report text: Volatility Surface (sections 2.4 and 3.2)

Paste into `QF620 Project Report Local.docx`, replacing the "[To do]" lines under 2.4 and 3.2. Figures are in `figures/` and come from notebook Section 2 (`analysis.ipynb`). Figure numbers in the report are placeholders (Figure X, Y, Z).

## 2.4 Volatility Surface

**Data constraint.** The data has two option maturities, never quoted at the same time: 16 April 2025 for 1–4 April, then 15 May 2025 from the evening of 6 April. Our analysis therefore focuses on these two quoted expiries, and on the VIX, the market's model-free implied volatility over the next 30 days, computed by CBOE from the same SPX options. At every minute we observe:

- the full smile at the quoted expiry (12–15 days before the roll, 34–39 days after); and
- the 30-day volatility level (the VIX), available in regular hours and 03:15–09:15 ET overnight.

**Strike direction.** Each quoted smile is fitted with Gatheral's raw SVI parameterisation in log-forward-moneyness k = ln(K/F) and total variance w = σ²T. Beyond the quoted strikes the fit is continued linearly in k, as Lee's moment formula allows.

**Maturity direction.** The total model-free variance is pinned at the two market points and is linear in maturity between them (constant forward variance). The fitted smile is scaled to each maturity so that its model-free variance matches this term structure. It reproduces the market smile exactly at the quoted expiry, and the VIX exactly at 30 days.

**Assumptions.**
1. Only one maturity is quoted at each moment; every other maturity is built, not observed.
2. The VIX supplies a 30-day level only, not a smile shape.
3. Outside the two market points, volatility is held flat.
4. The smile has the same shape at every maturity. In practice skew flattens as maturity grows, so the built surface overstates skew beyond the quoted expiry and understates it before it.
5. F = S·e^{rT}, with a constant r = 4.21% and no dividends.

**No-arbitrage checks.** Butterfly: call prices must be convex in strike, checked on market mid prices and with Durrleman's condition g(k) ≥ 0 on the fitted surface. Calendar: total variance must not fall with maturity, which here means the forward variance between the two market points must be non-negative. Where the VIX and the quoted expiry are inconsistent, the quoted expiry (a full observed smile) is kept and the VIX point is adjusted. Every fitted quoted-expiry smile is butterfly-free, and 496 of 499 surfaces pass both checks; the three exceptions are on 4 April, in extrapolated maturities.

**How we present it.** The main evidence is market data: the quoted smile through the event (every 10 minutes in regular hours, 30 minutes overnight) and the term structure between the quoted expiry and the VIX. The full strike × maturity surface is a supporting view: in the figure, the region between the two market points is solid and everything resting on the flat assumption is faded.

## 3.2 Volatility Surface

**The two quoted expiries through the event (Figure X).** Using market quotes only, ATM volatility on the 16 April expiry averaged about 21% in regular hours on 1–2 April, 26% on 3 April and 42% on 4 April. The put premium, measured as the volatility at k = −0.10 minus the at-the-money volatility, widened from about 10 vol points to 15 on 4 April, peaking at 17.7 points at 08:00 ET, 40 minutes after China announced its retaliation. After the roll the 15 May smile sat at 35–37% ATM with a put premium of 9–10 points. Its longer maturity makes it less reactive, so levels are not compared directly across the roll. The 90-day pause cut the 15 May ATM volatility from about 39% at 13:10 ET to about 31% at 13:30 and 25% by 15:30.

**Term structure (Figure Y).** Before the event, the front end was already slightly inverted, with the 16 April expiry about 0.5–1 vol point above the VIX. The inversion deepened to −8.8 vol points on 4 April at 14:40 ET, when the 12-day model-free volatility reached 53.5% against a VIX of 44.8%: options priced an immediate crash risk that was expected to fade within a month. The term structure stayed inverted by 3–5 points from 7 to 10 April. On about a third of the 8–10 April snapshots the VIX even implied more total variance over 30 days than the 15 May expiry did over 35–37 days. The pause flattened the slope from −7.5 to −1.1 points within ten minutes, but it was inverted again by 10 April as US–China escalation continued.

**The full surface (Figure Z, supporting).** Under the assumptions above, the strike × maturity surface shows the same story at every snapshot: near 20% at the money with the usual equity skew on 1 April, an upward shift after the 2 April announcement, the short end and the put side rising most on 4 April, crisis levels of about 40–50% on 7–9 April, and a drop after the 9 April pause.
