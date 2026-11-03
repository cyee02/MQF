# 07 · Changes Trail

How the project developed: the questions we asked at each stage, the choices we made and why, and what changed as a result. It is a record of our reasoning as much as of our edits.

## Stages at a glance

| # | Stage | Main question | Outcome |
|---|-------|---------------|---------|
| 1 | Groundwork | What does the paper claim, what data can we get, and how do we keep five deliverables consistent? | Context notes, data plan, one source of numbers, sync checks |
| 2 | First full analysis | Does the paper's result hold on free data, and does it survive our two challenges? | Replication works; both challenges rejected |
| 3 | Revisions after feedback | Is the evidence fair to a real investor, and is it presented clearly? | Out-of-sample test, walk-forward tuning, alpha/beta, clearer tables |
| 4 | Presentation restructure | Does the talk follow a clear argument? | Deck reorganised into five sections |
| 5 | Deficit test rethink | Was our deficit test measuring the right thing? | Annual test: H2 supported but fragile; Sharpe test removed |
| 6 | Clarity of the H0 tests | Can a reader see exactly what is tested, and why 3.3 and 3.4 differ? | Rules moved to §1.1; equations and one-sided cut-off stated; all 12 split tests shown |

## How our hypotheses evolved

| Stage | Part A (replicate the paper) | Part B (challenge it) |
|-------|------------------------------|------------------------|
| 1–4 | H0: the rate level makes no difference · H1: stocks earn less after high rates | H2: the Sharpe ratio holds up · H3: a big deficit offsets high rates |
| 5 | unchanged | **H2: a big deficit offsets high rates.** The Sharpe test was dropped once the deficit test gave a sharper answer to the same question. |

---

## 1 · Groundwork

**Questions:** What exactly does Maloney (2024) claim, what data did it use, and what can we reproduce without paid sources?

**What we did and why:**
- **Summarised every source before writing code:** the guideline, the walkthrough, the base paper, the CVaR paper, the lecture notes and the feedback received. Each summary lists page references, so every claim in the report can be traced to its source.
- **Chose free proxies for the paper's Global Financial Data series:** Ken French, FRED, Shiller, Damodaran, World Bank and Yahoo Finance. We documented each proxy and where it differs from the original, rather than hiding the gap.
- **Wrote the hypotheses down before seeing any results,** in two parts: replicate the paper (H0 vs H1), then try to prove it wrong (H2, H3). Fixing them first keeps the tests honest.
- **Made the notebook the only source of numbers and figures.** The report, slides and script read from `outputs/results.json` and `figures/` through anchors. Automated alignment checks (C1–C10) catch any number, figure, timing or dataset that drifts out of step.

## 2 · First full analysis

**Questions:** Does the paper's result reproduce on free data? If so, can it be explained away by risk (H2) or by the government deficit (H3)?

**What we did and why:**
- **Rebuilt the paper's three regime rules (M1–M3).** Only the trailing rule M2 uses information available at the time, so only M2 may drive strategies; M1 and M3 are for replication.
- **Replicated Exhibits 3 and 9.** The premium roughly halves after high-rate months (11.1% vs 5.4% a year; paper 10.3% vs 5.8%), and our Exhibit 9 weights match the paper's.
- **Used Newey-West t-statistics throughout.** Rate regimes are persistent (a high-rate month is followed by another about 97% of the time), so ordinary standard errors would overstate significance.
- **Tested H2** (Sharpe ratio) with a 12-month block bootstrap, and **H3** (deficit) with a monthly split by the primary deficit. Both were rejected.
- **Turned the findings into strategies (B, S1–S4)** and backtested them on investable ETFs, with a regime-switching Monte Carlo for the next ten years.

## 3 · Revisions after feedback

**Questions:** Would an investor living through these periods have seen the same thing? Are our strategy comparisons fair?

**What we changed and why:**

| Change | Reason |
|--------|--------|
| Added an in-sample (1926–95) vs out-of-sample (1996 onward) test of H0 vs H1 | A pattern can describe history without forecasting the future. It did keep its direction, but became too weak to trade. |
| Tuned S4's ridge penalty by walk-forward validation inside the in-sample period | Choosing it on the full in-sample period let the same months both fit and judge the weights: in-sample Sharpe 1.17 fell to 0.47 out of sample. |
| Added alpha and beta against the benchmark, with Newey-West t | Sharpe ratios alone don't show whether a strategy adds anything beyond the benchmark. |
| Added fixed stock/bond mixes and 1/N rebalanced; merged the allocation and backtest steps | To compare our rules with what investors actually hold, on the same sample and costs. |
| Moved results into tables; defined M1–M3 and the strategy codes; explained the paper's method in section 1 | So a reader can follow the argument without the notebook. |

## 4 · Presentation restructure

**Question:** Does the talk follow one clear line of argument?

**What we changed:**
- Organised the deck into five sections: summary of the paper, hypotheses, testing, findings and conclusion, and annex.
- Added slides on what the paper found and how it tests its claim, so the audience knows the method before seeing our replication.
- Gave the 2024–25 episode its own slide, because it is the strongest evidence against the paper.
- Reworded titles so each one states its finding.

## 5 · Rethinking the deficit test

**Question:** Our monthly test said a big deficit does not offset high rates (−4.7%, t −1.30). A separate annual test based on Kalecki's profits equation said it does. Which is right, and why do they disagree?

**What we found when we took the monthly test apart:**
- **The deficit measure mattered most.** The monthly test used the *primary* deficit, which excludes interest. In Kalecki's identity, interest paid by the government is income for bondholders, so excluding it removes part of the channel being tested.
- **The horizon was too short.** The deficit is published once a year, and the channel (deficit → income → profits → prices) takes years to reach stock returns. A 12-month horizon is too short for that.
- **Monthly data adds no new information.** It repeats each annual deficit value twelve times, which overstates how many independent observations we have.

**How we redesigned it:**
- **Annual data, 1929–2025.** The cut-offs are the sample medians from our own data (T-bill 3.07%, deficit 2.58% of GDP), not figures picked by hand.
- **Horizons of 1, 3 and 5 years.** One and three years match the paper's 12- and 36-month horizons; five years matches the 60-month window of the M2 rule.
- **Overlapping windows.** They use every year as a starting point. Because neighbouring windows share years, we judge significance with Newey-West t (lags = horizon) and a circular-shift p-value that keeps the deficit's persistence.
- **A decision rule set before running:** the hypothesis counts as supported only if the gap is positive with t > 1.96 at both 3 and 5 years.

**Result:**

| After high-rate years | 1 year | 3 years | 5 years |
|---|---|---|---|
| Big deficit | 9.4% | 8.5% | 9.2% |
| Small deficit | 0.5% | 1.6% | 3.0% |
| Gap (Newey-West t) | +8.8% (1.90) | +6.9% (2.82) | +6.2% (3.48) |
| Low-rate years, for reference | 12.7% | 13.1% | 12.5% |

The rule is met. A big deficit offsets about 60–65% of the high-rate penalty, so most of it, but not all.

**How far we trust it.** We tested the result against the obvious objections and report them all:

| Variant | 3-year gap (t) | 5-year gap (t) |
|---|---|---|
| Primary deficit, excluding interest | −1.7% (−0.61) | 2.2% (1.81) |
| Cut-off known at the time | 0.2% (0.07) | 4.2% (2.36) |
| Without 1980–1989 | 5.9% (1.55) | 6.3% (1.54) |
| Non-overlapping windows | 6.9% (1.60) | 6.2% (2.00) |

The effect depends on counting interest in the deficit and on the 1980s, when rates were falling. We therefore present H2 as supported but fragile: it helps explain 2024–25, but it is not a reliable trading signal on its own.

**Why the Sharpe test was removed.** The Sharpe test and the deficit test both asked whether an investor should cut stocks when rates are high. Once the deficit test gave a sharper and more relevant answer, keeping both added length without adding insight.

**What changed in each file:**

| File | Change |
|------|--------|
| 03 notebook | §3 is the annual test, with a method note, decision line, robustness table and figure `fig04_h2_deficit`. The Sharpe test and its figure are removed. S3 and the good/middle/bad thirds use the full deficit, for consistency. |
| outputs, figures | `results.json` regenerated; new deficit figure; the Sharpe figure and old deficit figure removed. |
| 01 report | Executive summary, hypotheses (now three), §4 rebuilt (tables, rationale, verdict), §5 ("a big deficit is one reason"), verdict and limitations updated; Sharpe section removed and figures renumbered. |
| 04 slides, 05 script | Hypothesis slides, the significance slide (Sharpe content replaced by rate persistence), the deficit slide, the 2024–25 and conclusion slides, and the annex, with matching script text. |
| 02 metadata, context/, scripts/ | Hypothesis lists, step 3 method and dataset descriptions updated; build scripts use the new keys. |

**Knock-on effects we checked:**
- S3 in-sample Sharpe 0.78 → 0.79.
- Deficit third's best stock share 60% → 50%.
- Unchanged: the recommended 60% stock share, all out-of-sample results and the Monte Carlo.

---

## 6 · Making the H0 tests readable

**Question:** A group review of the report found §3.3–3.4 hard to follow: the rules were defined after they were first used, the regression had no equation, "6 tests" did not match "3 rules", our rule-by-rule results seemed to be compared with the paper's asset-by-asset ones, and the §3.4 table showed only one t below −1.96 yet claimed 2 of 6 rejections.

**What we changed in the report and why (no numbers changed):**

| Change | Reason |
|--------|--------|
| Moved the M1–M3 table to §1.1, next to the paper's step 1; §3.1 now only covers how we apply it | Figure 1 and §1.1 already used the rule names before §3.1 defined them. |
| §3.3 split into Test 1 (our gap regression, by rule) and Test 2 (the paper's regression, by asset), each with its equation and variable definitions | Makes clear that only Test 2 is compared with the paper, asset for asset; the paper reports no t-statistics by rule. |
| Explained the overlapping 12-month windows and what Newey-West corrects | Each month is one observation, so neighbouring 12-month averages share 11 months; OLS would overstate t. |
| Stated "six tests = 2 horizons × 3 rules" and the one-sided cut-off (t < −1.645, not ±1.96) | The −1.96 reading made the rejection counts look wrong. |
| §3.4 table now shows both horizons for both periods, marks each rejection, and the one-month table left Annex B | The four rejections (all M3) were split between §3.4 and Annex B, so the table could not be checked on its own. Text explains why 3.4 is weaker than 3.3 (shorter periods; smaller gaps out of sample). |

**Then synchronised the slides and script with the report:**

| Change | Reason |
|--------|--------|
| Deck reordered to follow the report: data now opens Testing; 2024–25, what to hold (gold and momentum, 60% stocks) come before the strategies and backtests | The slides had moved these after the Monte Carlo, so the talk and the report told the story in different orders. |
| M1–M3 definitions moved from the data slide to the method slide | Same move as in the report (§1.1). |
| Presenters re-split into five contiguous blocks; hand-overs, page numbers and timings recomputed; speaker tag added to section dividers and annex slides (R3.3) | Reordering broke the old blocks; several pages were numbered twice. |
| Script rebuilt from the slide notes: one heading per slide, grouped by presenter, with section dividers, the hidden slide and backups marked as untimed | It still followed the old 19-slide deck. The sync check now accepts untimed slides. |
| Slide 9 notes: bars are the paper, diamonds are ours; slide 11 notes state the one-sided cut-off (t < −1.645); slide 3 given a script | The notes had bars and diamonds the wrong way round; slide 3 had no notes. |
| Titles of slides 3 and 20 shortened to one line | Both wrapped into the line below; slide 3's title also sat above the slide edge and under the speaker tag. |
| 5-year circular-shift p written as "p < 0.001" (notebook, results, report) | No rotation out of 5,000 beat the actual gap, so "0.000" overstated the precision. |

---

## Still to do
- Agree the current state as a group and save it as the sync snapshot (`scripts/sync_check.py --accept`).
- Trim the talk to 16:00 (R4.1); it now runs 18:54 (check C4).
- Check the layout of slides 3, 4, 6, 11, 13 and 16 in PowerPoint (6, 11 and 13 were slides 7, 11 and 13 before the reorder; 3, 4 and 16 changed today).
