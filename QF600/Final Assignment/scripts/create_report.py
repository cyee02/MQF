"""Create the first version of 01 - Project Report Group 6.docx from the template and the notebook's outputs.

    python scripts/create_report.py            # refuses to overwrite an existing report

Every number is written as a `num_<key>` bookmark holding results.json's display string,
and every figure carries alt text `fig:<id>`, so qf600-sync-check can keep them in step.
After the first version exists, edit the report in place (qf600-report skill); never re-run this.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.shared import Inches, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).parent))
import office_anchors as oa  # noqa: E402

ROOT = oa.ROOT
OUT = ROOT / "01 - Project Report Group 6.docx"
R = {k: v["display"] for k, v in json.loads((ROOT / "outputs" / "results.json").read_text()).items()}
META = json.loads((ROOT / ".sync" / "datasets.json").read_text())["files"]
TOKEN = re.compile(r"\{(\w+)\}|\*\*(.+?)\*\*")


def para(doc, text, style=None, after=None):
    """Paragraph with {key} → num_<key> anchors and **bold** spans."""
    p = doc.add_paragraph(style=style) if style else doc.add_paragraph()
    pos = 0
    for m in TOKEN.finditer(text):
        if m.start() > pos:
            p.add_run(text[pos:m.start()])
        if m.group(1):
            key = m.group(1)
            if key not in R:
                raise KeyError(f"no result '{key}' in outputs/results.json")
            oa.docx_add_anchor(p, f"num_{key}", R[key])
        else:
            p.add_run(m.group(2)).bold = True
        pos = m.end()
    if pos < len(text):
        p.add_run(text[pos:])
    if after is not None:
        p.paragraph_format.space_after = Pt(after)
    return p


def bullets(doc, items):
    for t in items:
        para(doc, t, style="List Bullet", after=2)


def table(doc, header, rows, widths=None, note=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Light Grid Accent 1"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for c, h in zip(t.rows[0].cells, header):
        c.text = ""
        c.paragraphs[0].add_run(h).bold = True
    for r in rows:
        cells = t.add_row().cells
        for c, v in zip(cells, r):
            c.text = ""
            p = c.paragraphs[0]
            pos = 0
            for m in TOKEN.finditer(v):
                if m.start() > pos:
                    p.add_run(v[pos:m.start()])
                if m.group(1):
                    oa.docx_add_anchor(p, f"num_{m.group(1)}", R[m.group(1)])
                else:
                    p.add_run(m.group(2)).bold = True
                pos = m.end()
            if pos < len(v):
                p.add_run(v[pos:])
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(9)
    if widths:
        for row in t.rows:
            for c, w in zip(row.cells, widths):
                c.width = Inches(w)
    if note:
        n = doc.add_paragraph()
        n.add_run(note).italic = True
        n.runs[0].font.size = Pt(8.5)
    doc.add_paragraph()
    return t


FIG_N = [0]


def figure(doc, fig_id, caption, width=6.3):
    doc.add_picture(str(ROOT / "figures" / f"{fig_id}.png"), width=Inches(width))
    doc.element.body.xpath(".//wp:docPr")[-1].set("descr", f"fig:{fig_id}")
    FIG_N[0] += 1
    c = doc.add_paragraph()
    r = c.add_run(f"Figure {FIG_N[0]}: {caption}")
    r.italic, r.font.size = True, Pt(9)
    c.paragraph_format.space_after = Pt(10)


def clear_body_after(doc, heading_text):
    """Remove the template's placeholder paragraph under a heading, return the heading paragraph."""
    for p in doc.paragraphs:
        if p.text.strip() == heading_text:
            nxt = p._p.getnext()
            if nxt is not None and nxt.tag.endswith("}p") and "".join(nxt.itertext()).startswith("["):
                nxt.getparent().remove(nxt)
            return p
    raise KeyError(heading_text)


def build():
    if OUT.exists():
        sys.exit(f"{OUT.name} already exists: edit it in place (qf600-report), don't regenerate.")
    tpl = Document(str(ROOT / "templates" / "report_template.docx"))
    # Keep the cover page (everything before "Executive Summary"); rebuild the rest in order.
    body = tpl.element.body
    start = next(p for p in tpl.paragraphs if p.text.strip() == "Executive Summary")._p
    node = start
    while node is not None:
        nxt = node.getnext()
        if not node.tag.endswith("sectPr"):
            body.remove(node)
        node = nxt
    doc = tpl
    for p in doc.paragraphs:
        if p.text.startswith("Honey, the Fed"):
            for r in p.runs:
                r.font.color.rgb = RGBColor(0x1F, 0x3A, 0x34)

    # ------------------------------------------------------------ exec summary
    doc.add_heading("Executive Summary", 1)
    para(doc, "**Question.** Do stocks earn less when the risk-free rate is high, and what should an investor hold now that "
              "the 3-month T-bill pays {today_tbill}? We replicate Maloney (2024), \"Honey, the Fed Shrunk the Equity Premium\", "
              "test whether its conclusion survives, and turn the evidence into an allocation.")
    para(doc, "**The paper's result is real on its own sample.** Using free proxies for its data (1926–2023), stocks earned "
              "{ex3_equities_lower_12m} a year above cash in the 12 months after lower-rate months but only {ex3_equities_higher_12m} "
              "after higher-rate months (paper: 10.3% vs 5.8%). Four of six tests reject \"rates make no difference\" (H0), the "
              "paper's regression gives t = {reg_t_ols_eq} (paper −2.2), and we reproduce its Exhibit 9 portfolios exactly "
              "(implied Sharpe ratios {ex9_sr_1}, {ex9_sr_2}, {ex9_sr_3}, {ex9_sr_4}).")
    para(doc, "**A big deficit offsets most of the high-rate penalty (H2), but the evidence is fragile.** In years when the "
              "T-bill rate was above its median, stocks earned {h2_ret_high_big_5y} a year above cash over the next five years when "
              "the deficit was big, against {h2_ret_high_small_5y} when it was small (Newey-West t = {h2_t_5y}).")
    para(doc, "**But the pattern is too weak to trade.** Fitted on 1926–1995, the rate signal has an out-of-sample R² of only "
              "{oos_r2} on 1996–2026, and in 2024–25 stocks beat cash by {recent_eq_2024} and {recent_eq_2025} despite high rates, "
              "driven by a few very large companies. On investable ETFs (Dec 2020 – Sep 2026, out of sample) no strategy beats an "
              "equal-weight, never-rebalanced mix of stocks, Treasuries, gold and momentum (Sharpe {s6_oos_b_sharpe}); the paper's "
              "own portfolios score {s6_oos_s1_sharpe} and our rate rule {s6_oos_s2_sharpe}.")
    para(doc, "**Recommendation.** Being in the middle doesn't mean retreating to risk-free. The best stock share today is around "
              "{x_stock_share}, held alongside bonds, gold and momentum rather than switched in and out by the level of rates. "
              "When rates are high or rising, gold and momentum diversify stocks better than bonds: an equal-weight mix of all four "
              "had a Sharpe ratio of {s5_sharpe_1n_high} in higher-rate months since 1960, against {s5_sharpe_6040_high} for 60/40.")
    doc.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)

    # -------------------------------------------------------------- 1 problem
    doc.add_heading("1 Research Problem and Impact", 1)
    para(doc, "From 2010 to 2021 the federal funds rate averaged about 0.5%; in 2022–23 it rose above 5%. Most forecasts put "
              "rates over the next decade about 3.2 percentage points higher than in the decade before (Maloney 2024, p.3). An "
              "investor who held 60% stocks and 40% bonds through the low-rate years now faces a simple question with a large impact "
              "on a portfolio: if cash and bonds pay more, should the stock share fall, and by how much?")
    para(doc, "Maloney (2024) argues that the equity premium (stocks' return above cash) has been smaller when cash rates were high, "
              "that bonds pass higher rates on to investors, and that \"cash-plus\" strategies, which keep their money in T-bills "
              "while they trade, gain a relative advantage. We test that claim, ask whether it still holds after 2023, and translate "
              "the answer into an allocation that an investor could actually run. Beating a benchmark is not the goal; an honest "
              "\"no\" is a valid result (guideline R2.7).")
    para(doc, "We fixed three hypotheses before looking at results, in two parts:")
    table(doc, ["", "Hypothesis", "Tested in"], [
        ["H0", "The T-bill rate level makes no difference: stocks earn the same above cash after higher- and lower-rate months.", "§3"],
        ["H1", "The paper's claim: after higher-rate months, stocks earn less above cash.", "§3"],
        ["H2", "Ours: a big government deficit keeps profits growing when rates are high, offsetting the penalty (Kalecki).", "§4"],
    ], widths=[0.4, 5.0, 0.8], note="Part A (H0 vs H1) replicates the paper on its sample; Part B (H2) looks for evidence against its conclusion.")

    # ----------------------------------------------------------------- 2 data
    doc.add_heading("2 Data", 1)
    para(doc, "The paper's main source, Global Financial Data (Finaeon), is not available to us: SMU has no subscription and the "
              "free trial covers only US stocks from 2019. We use free proxies over the paper's sample (monthly, July 1926 – "
              "December 2023) and extend them to September 2026. All series are downloaded by the notebook (§1); Annex A lists "
              "every file with its source, size and columns.")
    table(doc, ["Paper's series", "Our proxy", "Period"], [
        ["3-month T-bill rate (GFD before 1934)", "FRED TB3MS from 1934; Ken French 1-month bill ×12 before", "Jul 1926 – Sep 2026"],
        ["US equity returns (GFD)", "Ken French market return (CRSP, all US stocks)", "Jul 1926 – Sep 2026"],
        ["US Treasury returns (GFD)", "10-year bond return built from the 10-year yield (FRED GS10, Shiller before 1953)", "Jul 1926 – Sep 2026"],
        ["IG credit excess return", "Baa bond return (Moody's Baa yield) minus the 10-year Treasury return", "Jul 1926 – Sep 2026"],
        ["Real earnings, CAPE", "Robert Shiller's data library", "1871 – Oct 2026"],
        ["Cash-plus / liquid alternatives", "Momentum: T-bill + UMD (Ken French); PDP ETF in the backtest", "1927 – Sep 2026"],
        ["(not in paper) gold", "World Bank monthly gold price", "Jan 1960 – Sep 2026"],
        ["(not in paper) deficit", "FRED federal surplus and interest outlays, % of GDP", "1929 / 1940 – 2025"],
        ["Investable assets", "SPY, IEF, GLD, PDP, PSP, HYG, VNQ, RSP (Yahoo Finance)", "2002 – Oct 2026"],
    ], widths=[1.8, 3.2, 1.3])
    para(doc, "Our 10-year bond return, compounded to calendar years, has a correlation of {bond_check_corr} with Damodaran's "
              "published annual T-bond returns, so the proxy is close to a standard series. Each month is labelled higher- or "
              "lower-rate with the paper's three rules (p.4): above the 1926–2023 median (M1); above the 40th percentile of the "
              "previous 5 years (M2); or of the 5 years centred on the month (M3). Rates below 0.5% always count as lower. Only M2 "
              "uses information available at the time, so it is the only rule our strategies use. December 2023 is higher-rate under "
              "all three rules, as in the paper (p.5).")
    figure(doc, "fig01_regimes", "The 3-month T-bill rate and higher-rate months under the trailing 5-year rule (M2).")

    # ----------------------------------------------------------- 3 replication
    doc.add_heading("3 Replication of the Paper", 1)
    doc.add_heading("3.1 Exhibit 3: smaller premiums after higher rates", 2)
    para(doc, "For every month we average the return above cash over the next 1, 12 and 36 months, then average across months and "
              "across the three rules, as the paper does. Our proxies reproduce the paper's equity pattern closely; credit shows an "
              "even larger gap. Treasuries differ: we find almost no penalty at 12 and 36 months, consistent with the paper's broad "
              "1990–2023 sample, where Treasuries did slightly better after higher rates (p.7).")
    table(doc, ["Asset · horizon", "After lower (ours)", "After higher (ours)", "Paper lower / higher"], [
        ["Equities · 1M", "{ex3_equities_lower_1m}", "{ex3_equities_higher_1m}", "11.4% / 4.9%"],
        ["Equities · 12M", "{ex3_equities_lower_12m}", "{ex3_equities_higher_12m}", "10.3% / 5.8%"],
        ["Equities · 36M", "{ex3_equities_lower_36m}", "{ex3_equities_higher_36m}", "10.4% / 5.5%"],
        ["Treasuries · 12M", "{ex3_treasuries_lower_12m}", "{ex3_treasuries_higher_12m}", "1.5% / 1.2%"],
        ["IG credit · 12M", "{ex3_credit_lower_12m}", "{ex3_credit_higher_12m}", "2.6% / 1.1%"],
        ["Momentum (UMD) · 12M", "{ex3_momentum_lower_12m}", "{ex3_momentum_higher_12m}", "not reported"],
    ], widths=[1.8, 1.4, 1.4, 1.7], note="Annualised return above cash, Jul 1926 – Dec 2023, average of the three regime rules.")
    figure(doc, "fig02_exhibit3_replication", "Our replication of Exhibit 3 (bars) against the paper's values (diamonds).")
    doc.add_heading("3.2 H0 against H1", 2)
    para(doc, "We regress the next-month and next-12-month equity return above cash on a higher-rate dummy for each rule. Because "
              "rate levels persist, ordinary standard errors overstate significance (the paper's own caveat, p.5), so we use "
              "Newey-West t-statistics and a one-sided 5% test. **{h0_rejections} of the 6 tests reject H0** in favour of H1: the "
              "12-month gap is {h0_gap_12m_m1} under M1 (t = {h0_t_12m_m1}) and {h0_gap_12m_m3} under M3 (t = {h0_t_12m_m3}); under "
              "the trailing rule M2 it is {h0_gap_12m_m2} (t = {h0_t_12m_m2}). The paper's continuous regression of next month's "
              "return on today's T-bill rate gives t = {reg_t_ols_eq} for equities (paper −2.2, Newey-West {reg_t_nw_eq}), "
              "t = {reg_t_ols_credit} for credit (paper −2.4) and t = {reg_t_ols_tsy} for Treasuries (not significant in either).")
    doc.add_heading("3.3 Momentum and Exhibit 9", 2)
    para(doc, "The paper says strategies that hold T-bills while trading earn about the same above cash in either regime. Momentum "
              "(UMD) did better than that: it earned {mom_gap_avg} a year more after higher-rate months (Newey-West t = {mom_t_m2} "
              "under M2), which supports the paper's cash-plus argument more strongly than the paper itself claims.")
    para(doc, "Finally we recompute Exhibit 9, the paper's only allocation advice, from its stated volatilities, Sharpe ratios and "
              "correlations: maximum-Sharpe long-only portfolios, with a 3% real return target and real cash at −0.5% (lower-rate "
              "world) or +0.5% (higher-rate world). Our weights are within {ex9_mae} of the paper's on average, and the implied "
              "Sharpe ratios match exactly. In the higher-rate world with penalised Sharpe ratios (column 4), the portfolio holds 26% "
              "public equity, 33% Treasuries and 28% liquid alternatives; this is strategy S1 in §7.")

    # ------------------------------------------------------------ 4 mechanism
    doc.add_heading("4 Why: Profits and the Deficit", 1)
    para(doc, "The paper's explanation is fundamental: low rates stimulate demand and borrowing, so company earnings grow faster "
              "(p.7). We confirm it with Shiller's data. Real earnings per share grew {eps_growth_lower} a year after lower-rate "
              "months and {eps_growth_higher} after higher-rate months (12- and 36-month horizons, paper: 11% vs 1%).")
    para(doc, "H2 asks whether a big government deficit breaks this link. Under the Kalecki profits identity, a deficit is income "
              "for households and firms, so it should support profits even when rates are high. We use annual data, {h2_first_year}–"
              "{h2_last_year}: a year is high-rate when the 3-month T-bill is above its median ({h2_rate_cut}) and has a big deficit "
              "when the federal deficit, including interest, is above its median ({h2_def_cut} of GDP).")
    para(doc, "**Why annual data, 1-, 3- and 5-year horizons and overlapping windows.** The deficit is published once a year, and "
              "Kalecki's channel takes years to work. One and three years match the paper's 12- and 36-month horizons; five years "
              "matches the 60-month M2 window. Every year starts a window, so we use Newey-West t-statistics (lags = horizon) and a "
              "circular-shift p-value.")
    table(doc, ["Return above cash, % a year", "Next 1 year", "Next 3 years", "Next 5 years"], [
        ["Low-rate years", "{h2_ret_low_1y}", "{h2_ret_low_3y}", "{h2_ret_low_5y}"],
        ["High rate, small deficit", "{h2_ret_high_small_1y}", "{h2_ret_high_small_3y}", "{h2_ret_high_small_5y}"],
        ["High rate, big deficit", "{h2_ret_high_big_1y}", "{h2_ret_high_big_3y}", "{h2_ret_high_big_5y}"],
        ["Big minus small deficit", "{h2_gap_1y}", "{h2_gap_3y}", "{h2_gap_5y}"],
        ["Newey-West t", "{h2_t_1y}", "{h2_t_3y}", "{h2_t_5y}"],
        ["Circular-shift p (one-sided)", "{h2_p_1y}", "{h2_p_3y}", "{h2_p_5y}"],
    ], widths=[2.4, 1.2, 1.2, 1.2], note="Annual. S&P 500 minus 3-month T-bill (Damodaran); federal deficit, % of GDP (FRED).")
    para(doc, "**H2 is supported, with caveats.** A big deficit offsets about {h2_offset_5y} of the high-rate penalty at five years, "
              "but with the primary deficit or a cut-off known at the time the three-year gap disappears, and most of the evidence "
              "comes from 1982–1994.")
    figure(doc, "fig04_h2_deficit", "Stocks' average annual return above cash over the next 1, 3 and 5 years, by rate and deficit.", width=5.6)

    # ------------------------------------------------------------------- 5 OOS
    doc.add_heading("5 Does It Still Hold? Out-of-Sample Tests", 1)
    para(doc, "A pattern can describe the past without helping to forecast. We fit the paper's regression on 1926–1995 only "
              "(slope t = {oos_slope_train_t}) and use it to forecast 1996 – September 2026. The forecasts are barely better than "
              "the 1926–95 average return: out-of-sample R² is {oos_r2} (Campbell and Thompson 2008). In the later period the slope "
              "is {oos_slope_test} per percentage point of T-bill rate (t = {oos_slope_test_t}). The direction survives: after "
              "higher-rate months stocks still earned {late_eq_higher_12m} a year above cash against {late_eq_lower_12m} after "
              "lower-rate months (1996–2026, M2), but the gap is smaller and not reliable.")
    para(doc, "The recent years break the pattern outright. Stocks beat cash by {recent_eq_2024} in 2024, {recent_eq_2025} in 2025 "
              "and {recent_eq_2026} in January–September 2026, against a {recent_hi_avg} average after higher-rate months in the "
              "paper's sample. A big deficit is one reason (§4); concentration is another: the cap-weighted S&P 500 beat its equal-weight "
              "version by {conc_gap_2023} in 2023, {conc_gap_2024} in 2024 and {conc_gap_2025} in 2025, so the gains came from a few "
              "very large companies. Valuation also rose: the CAPE ratio is now {cape_latest}, near its historical high.")
    para(doc, "Robustness. A simpler rule (rate above its own 5-year average) gives {simple_eq_lower_12m} vs {simple_eq_higher_12m}, "
              "the same direction. Adding valuation strengthens the rate effect, as the paper found: in the two-factor regression "
              "the T-bill rate has t = {cape_t_tbill} and 1/CAPE t = {cape_t_ey} (paper −3.2 and +3.9). With CAPE above 40 and "
              "rates high, the regression predicts a low premium today, which is exactly what 2024–25 contradicted.")
    para(doc, "**Verdict on the paper: partly true.** The relationship is real in a century of data and reproduces closely, but it "
              "is weak as a forecast, and it failed in the most recent high-rate episode (Prof Liu points 2, 3 and 5).")

    # ------------------------------------------------------------- 6 allocation
    doc.add_heading("6 What Should an Investor Hold?", 1)
    para(doc, "We use the longest sample the data allows, monthly from February 1960 (when the World Bank's gold series starts) to "
              "September 2026, with four assets: stocks, 10-year Treasuries, gold and momentum (cash-plus). Gold was fixed at $35 "
              "until August 1971, so it barely moves in the first decade; we keep those years and note it.")
    doc.add_heading("6.1 Which assets still protect a portfolio?", 2)
    para(doc, "Bonds are a weaker cushion when rates are high or rising: their correlation with stocks is {s5_corr_bonds_high} in "
              "higher-rate months and {s5_corr_bonds_rising} while rates rise (as in 2022, when stocks and bonds fell together). Gold "
              "({s5_corr_gold_high} and {s5_corr_gold_rising}) and momentum ({s5_corr_momentum_high} and {s5_corr_momentum_rising}) "
              "stay close to uncorrelated in both (Prof Liu point 11).")
    doc.add_heading("6.2 What mean-variance says (Prof Liu point 7)", 2)
    para(doc, "For one risky asset plus cash, the optimal stock share is w* = (E[R] − r_f) / (A σ²) (Lecture 2). With risk "
              "aversion A = 3, the historical premium and volatility give w* = {s5_wstar_low_A3} after lower-rate months (i.e. "
              "leverage) but {s5_wstar_high_A3} after higher-rate months. The premium roughly halves while volatility barely "
              "changes, so the stock share should fall, but not to zero.")
    doc.add_heading("6.3 60/40, 50/50 and equal weights (Prof Liu points 4, 6, 10, 11)", 2)
    table(doc, ["Sharpe ratio (CVaR 5%)", "60/40", "50/50", "1/N: stocks, bonds, gold, momentum"], [
        ["Higher-rate months", "{s5_sharpe_6040_high} ({s5_cvar_6040_high})", "{s5_sharpe_5050_high} ({s5_cvar_5050_high})", "{s5_sharpe_1n_high} ({s5_cvar_1n_high})"],
        ["Rates rising", "{s5_sharpe_6040_rising} ({s5_cvar_6040_rising})", "{s5_sharpe_5050_rising} ({s5_cvar_5050_rising})", "{s5_sharpe_1n_rising} ({s5_cvar_1n_rising})"],
        ["Rates falling", "{s5_sharpe_6040_falling} ({s5_cvar_6040_falling})", "{s5_sharpe_5050_falling} ({s5_cvar_5050_falling})", "{s5_sharpe_1n_falling} ({s5_cvar_1n_falling})"],
    ], widths=[1.8, 1.3, 1.3, 1.9], note="Feb 1960 – Sep 2026, monthly rebalancing. CVaR 5% = average loss in the worst 5% of months. Rising/falling = 12-month change in the T-bill rate above +0.5 / below −0.5 percentage points.")
    para(doc, "Moving from 60/40 to 50/50 when rates are high does not raise the risk-adjusted return: it lowers volatility and "
              "CVaR, but the Sharpe ratio is unchanged. What helps is adding assets that do not depend on rates. The equal-weight "
              "mix of stocks, bonds, gold and momentum has more than twice the Sharpe ratio of 60/40 in higher-rate months and "
              "stays positive while rates rise, when 60/40 loses money above cash.")
    doc.add_heading("6.4 Good, middle and bad conditions (Prof Liu points 8 and 9)", 2)
    para(doc, "We split history into thirds by the T-bill rate, a valuation gap (1/CAPE minus the real 10-year yield) and the "
              "federal deficit, and test stock/bond mixes from 0% to 100% stocks in each third. Today the T-bill rate is in the "
              "middle third (best share {s5_best_share_tbill_today}), valuation is in the bad third because stocks are expensive "
              "(best {s5_best_share_valuation_gap_today}), and the deficit is in the good third (best "
              "{s5_best_share_deficit_today}). Averaging these with the mean-variance answer gives **{x_stock_share} in "
              "stocks**, the X in our central message.")
    figure(doc, "fig05_best_share_terciles", "Sharpe ratio of stock/bond mixes by stock share, in good, middle and bad thirds of each variable.")

    # ------------------------------------------------------------ 7 strategies
    doc.add_heading("7 Strategies and Backtests", 1)
    para(doc, "We test the ideas on investable ETFs: SPY (stocks), IEF (Treasuries), GLD (gold) and PDP (momentum), plus PSP, HYG "
              "and VNQ for the paper's portfolios. The sample runs monthly from May 2007, when every fund exists, to September 2026 "
              "and is split in time order: everything is chosen or fitted on the first 70% (May 2007 – November 2020) and judged "
              "only on the last 30% (December 2020 – September 2026), which contains the 2022–26 high-rate period (Prof Liu point 5). "
              "Strategies rebalance monthly and pay 10 basis points per unit of turnover.")
    table(doc, ["Code", "Strategy", "Rule (high = previous month's M2 label)"], [
        ["B", "Benchmark", "Equal amounts in SPY, IEF, GLD, PDP, bought once and never rebalanced; restarted at equal weights for each period"],
        ["S1", "Paper (Exhibit 9)", "Low: 37 SPY / 17 PSP / 18 IEF / 10 VNQ / 19 PDP; high: 26 SPY / 10 PSP / 33 IEF / 3 HYG / 28 PDP"],
        ["S2", "Rate rule", "70% SPY / 30% IEF when low; 50/50 when high"],
        ["S3", "Rate + deficit", "As S2, but 60/40 when rates are high and the federal deficit is big (H2)"],
        ["S4", "Ridge mean-variance", "Weights on SPY, IEF, GLD, PDP fitted in-sample for each regime: w = (λΣ + ηI)⁻¹μ, long-only (Lecture 5)"],
    ], widths=[0.5, 1.4, 4.4])
    rows = []
    for metric, key in [("Alpha (annual, vs B)", "alpha"), ("Alpha t-stat (NW)", "alpha_t"), ("Beta (vs B)", "beta"),
                        ("Annual return", "ret"), ("Annual variance", "var"), ("Sharpe ratio", "sharpe"),
                        ("CVaR 5% (monthly)", "cvar5"), ("Max drawdown", "mdd")]:
        for tag, lab in [("is", "in"), ("oos", "out")]:
            rows.append([f"{metric} · {lab}"] + [("{" + f"s6_{tag}_{c}_{key}" + "}") if f"s6_{tag}_{c}_{key}" in R else "—"
                                                 for c in ["b", "s1", "s2", "s3", "s4"]])
    table(doc, ["Metric · sample", "B", "S1 Paper", "S2 Rate", "S3 Rate + deficit", "S4 Ridge MV"], rows,
          widths=[1.7, 0.8, 0.9, 0.9, 1.1, 0.9],
          note="In = May 2007 – Nov 2020 (in-sample); out = Dec 2020 – Sep 2026 (out-of-sample). Alpha and beta from regressing each strategy's monthly excess return on the benchmark's, Newey-West standard errors.")
    para(doc, "Out of sample, no strategy beats the benchmark. The paper's portfolios (S1) have the lowest Sharpe ratio "
              "({s6_oos_s1_sharpe}) and the deepest drawdown ({s6_oos_s1_mdd}), because private equity and real estate behaved like "
              "leveraged stocks. The rate rule (S2, {s6_oos_s2_sharpe}) cut stocks just before they rallied in 2023–25; adding the "
              "deficit (S3, {s6_oos_s3_sharpe}) helps a little but does not close the gap. S4 shows the error-maximiser problem from "
              "Lecture 5: the only significant alpha in-sample ({s6_is_s4_alpha}, t = {s6_is_s4_alpha_t}) vanishes out of sample "
              "({s6_oos_s4_alpha}, t = {s6_oos_s4_alpha_t}). The benchmark, which never trades, has the best Sharpe ratio "
              "({s6_oos_b_sharpe}).")
    figure(doc, "fig06_oos_growth", "Growth of $1 out of sample (Dec 2020 – Sep 2026), after trading costs.")
    doc.add_heading("7.1 The next ten years: rates stay high or fall", 2)
    para(doc, "We simulate 2,000 ten-year paths. Rates switch between regimes with probabilities counted from history (the CVaR "
              "paper's method, Pun, Wang and Yan p.17): a higher-rate month is followed by another {mc_p_stay_high} of the time. Each "
              "simulated month draws a historical month (1960–2026) from the same regime. If rates stay high, the equal-weight "
              "benchmark has a median annual return of {mc_high_b_med} (Sharpe {mc_high_b_sharpe}) against {mc_high_s2_med} "
              "(Sharpe {mc_high_s2_sharpe}) for the rate rule; in the worst 5% of paths it still earns {mc_high_b_p5} a year. In a "
              "stress case where rates never leave the high regime, the gap widens: {mc_stress_b_med} for the benchmark against "
              "{mc_stress_s2_med} for the rate rule. Cutting stocks for bonds when rates are high costs return without buying safety.")
    figure(doc, "fig07_monte_carlo", "Distribution of 10-year annualised returns by strategy under three rate scenarios.")

    # -------------------------------------------------------------- 8 verdict
    doc.add_heading("8 Verdict and Central Message", 1)
    bullets(doc, [
        "**H0 vs H1 (replication):** the paper's result holds on its sample; {h0_rejections} of 6 tests reject H0 and the "
        "regression gives t = {reg_t_ols_eq} (paper −2.2).",
        "**H2 (deficit offset):** supported at 3 and 5 years (t = {h2_t_3y} and {h2_t_5y}), but fragile.",
        "**Out of sample:** the signal is weak (R² {oos_r2}) and failed in 2024–25; timing the stock share by the rate level did "
        "not beat a diversified buy-and-hold mix.",
    ])
    para(doc, "**Central message:** \"Being in the middle doesn't mean retreating to risk-free. The best stock share today is "
              "around {x_stock_share}, held alongside bonds, gold and momentum, and kept steady rather than switched by the level "
              "of interest rates.\" High rates do shrink the equity premium (the paper is right about history), but the effect is "
              "too noisy to trade, and assets that do not depend on rates protect a portfolio better than moving from 60/40 to "
              "50/50 (Prof Liu points 7, 8 and 12).")

    # ---------------------------------------------------------------- 9 metrics
    doc.add_heading("9 Performance Measures and Evaluation Metrics", 1)
    table(doc, ["Measure", "Definition", "Why we use it"], [
        ["Return above cash", "Return minus the 3-month T-bill (monthly, annualised ×12)", "The paper's measure of the risk premium"],
        ["Sharpe ratio", "Mean excess return ÷ its standard deviation, annualised ×√12", "Reward per unit of risk (all strategies)"],
        ["Alpha, beta", "Intercept and slope of a strategy's excess return on the benchmark's", "Skill vs exposure (Lecture 3); Newey-West t"],
        ["Annual variance", "Variance of monthly returns ×12", "Total risk, as requested"],
        ["Max drawdown", "Largest peak-to-trough fall in cumulative value", "Worst loss an investor would have lived through"],
        ["CVaR 5%", "Average loss in the worst 5% of months", "Tail risk; reported for every strategy (Prof Liu point 10)"],
        ["Certainty equivalent", "Mean excess return − ½ A σ², A = 3", "Picks a stock share where Sharpe cannot (Lecture 1)"],
        ["Newey-West t-statistic", "t-statistic robust to autocorrelation", "Rate levels persist, so ordinary t overstates significance"],
        ["Out-of-sample R²", "1 − SSE(model) / SSE(training-sample mean)", "Does the rate signal forecast? (Campbell and Thompson 2008)"],
    ], widths=[1.4, 2.8, 2.1])

    # ------------------------------------------------------------ 10 limits
    doc.add_heading("10 Limitations and Next Steps", 1)
    bullets(doc, [
        "**Proxies, not the paper's data.** Treasury and credit returns are built from yields, and momentum stands in for "
        "hedge-fund cash-plus indices; PDP is long-only, so it is closer to equity than a true cash-plus fund.",
        "**Short investable history.** The out-of-sample period is under six years and dominated by a large-company rally.",
        "**Regime thirds use the whole sample.** The good/middle/bad split describes history; it is not a trading rule.",
        "**Gold before 1971** was fixed at $35, so its early diversification is overstated as zero correlation.",
        "**Next steps:** test real cash-plus funds (DBMF, market-neutral) as their history grows; add valuation (CAPE) to the "
        "rate rule; check other countries, as the Lecture 4 checklist asks of any new signal.",
    ])

    # ------------------------------------------------------------ references
    doc.add_heading("References", 1)
    for ref in [
        "Maloney, T. (2024). Honey, the Fed Shrunk the Equity Premium: Asset Allocation in a Higher-Rate World. The Journal of Portfolio Management, 50(6).",
        "Pun, C. S., Wang, T., & Yan, Z. Data-Driven Distributionally Robust CVaR Portfolio Optimization under Regime-Switching Ambiguity Set. SSRN 4378930.",
        "Campbell, J., & Thompson, S. (2008). Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average? Review of Financial Studies, 21(4).",
        "Asvanunt, A., & Richardson, S. (2017). The Credit Risk Premium. The Journal of Fixed Income, 26(3).",
        "DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal Versus Naive Diversification. Review of Financial Studies, 22(5).",
        "French, K. R. Data Library. mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html.",
        "Shiller, R. J. Online Data. shillerdata.com. · Damodaran, A. Historical Returns. pages.stern.nyu.edu/~adamodar. · World Bank Commodity Price Data (Pink Sheet). · Federal Reserve Bank of St. Louis, FRED.",
        "Liu, P. QF600 Asset Pricing lecture notes, Weeks 1–6, SMU, 2026.",
    ]:
        para(doc, ref, after=3)

    # ------------------------------------------------------------- annexes
    doc.add_heading("Annex A Datasets", 1)
    para(doc, "Every file the notebook uses, from 02 - Dataset Metadata Group 6.md. Script-downloaded files are rebuilt by notebook §1.")
    arow = []
    for fn, f in sorted(META.items()):
        sh = max(f.get("sheets") or [{}], key=lambda x: x.get("rows", 0))
        arow.append([fn, f.get("description", ""), f.get("provider", ""), f"{sh.get('rows', '—'):,}" if isinstance(sh.get('rows'), int) else "—",
                     str(sh.get("n_columns", "—")), f"{sh.get('start', '—')} → {sh.get('end', '—')}"])
    table(doc, ["File", "Description", "Source", "Rows", "Cols", "Period"], arow, widths=[1.4, 2.1, 1.1, 0.5, 0.4, 1.0])
    doc.add_heading("Annex B Additional Results", 1)
    table(doc, ["Test (H0: no difference)", "1-month gap · t", "12-month gap · t"], [
        ["M1 full-sample median", "{h0_gap_1m_m1} · {h0_t_1m_m1}", "{h0_gap_12m_m1} · {h0_t_12m_m1}"],
        ["M2 trailing 5 years", "{h0_gap_1m_m2} · {h0_t_1m_m2}", "{h0_gap_12m_m2} · {h0_t_12m_m2}"],
        ["M3 centred 5 years", "{h0_gap_1m_m3} · {h0_t_1m_m3}", "{h0_gap_12m_m3} · {h0_t_12m_m3}"],
    ], widths=[2.2, 2.0, 2.0], note="Equity return above cash after higher- minus after lower-rate months, Jul 1926 – Dec 2023, Newey-West t.")
    table(doc, ["Exhibit 3, other horizons", "After lower", "After higher"], [
        ["Treasuries · 1M", "{ex3_treasuries_lower_1m}", "{ex3_treasuries_higher_1m}"],
        ["Treasuries · 36M", "{ex3_treasuries_lower_36m}", "{ex3_treasuries_higher_36m}"],
        ["IG credit · 1M", "{ex3_credit_lower_1m}", "{ex3_credit_higher_1m}"],
        ["IG credit · 36M", "{ex3_credit_lower_36m}", "{ex3_credit_higher_36m}"],
        ["Momentum · 1M", "{ex3_momentum_lower_1m}", "{ex3_momentum_higher_1m}"],
        ["Momentum · 36M", "{ex3_momentum_lower_36m}", "{ex3_momentum_higher_36m}"],
    ], widths=[2.2, 2.0, 2.0])
    doc.add_heading("AI Assistance Statement", 1)
    para(doc, "Prepared with the assistance of Claude (Anthropic) for code, data pipelines and drafting. All results were run "
              "from the group's notebook and checked by the group.")
    doc.save(OUT)
    print(f"wrote {OUT.name}: {FIG_N[0]} figures, {sum(1 for _ in oa.docx_anchors(Document(str(OUT))))} number anchors")


if __name__ == "__main__":
    build()
