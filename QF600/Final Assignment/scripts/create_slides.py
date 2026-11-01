"""Create the first version of 04 - Presentation Slides Group 6.pptx and 05 - Presentation Script.docx.

    python scripts/create_slides.py         # refuses to overwrite existing files

One definition per slide drives both files, so titles, speakers, timings and [CLICK n]
cues match. Numbers on slides are num:<key> shapes from outputs/results.json; figures are
the notebook's *_slide.png versions (large text for the big screen). After the first
version exists, edit both files in place with the qf600-slides skill; never re-run this.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from docx import Document
from docx.shared import Pt

sys.path.insert(0, str(Path(__file__).parent))
import deck as D            # noqa: E402
from pptx_anim import set_click_animations  # noqa: E402

ROOT = D.ROOT
OUT_PPTX = ROOT / "04 - Presentation Slides Group 6.pptx"
OUT_SCRIPT = ROOT / "05 - Presentation Script.docx"
R = {k: v["display"] for k, v in json.loads((ROOT / "outputs" / "results.json").read_text()).items()}
DATA_NOTE = "Data: Ken French, FRED, Shiller, Damodaran, World Bank, Yahoo Finance · Jul 1926 – Sep 2026 · Group 6 calculations"


def stat(s, key, label, x, y, w=2.75, h=1.2, color="teal"):
    D.add_stat(s, key, R[key], label, x, y, w, h, color)
    return [f"bg.num:{key}", f"num:{key}", f"label.{key}"]


def card(s, name, x, y, w, h, kicker, body, highlight=False):
    D.add_card(s, name, x, y, w, h, kicker=kicker, body=body, highlight=highlight)
    return [f"bg.{name}", f"kicker.{name}", name]


def fig(s, fig_id, x, y, w):
    D.add_figure(s, f"{fig_id}_slide", x, y, w)
    return [f"fig:{fig_id}_slide"]


SLIDES = []   # (slide, speaker, start, end, script) for the script document


def finish(s, speaker, start, end, script, clicks=None):
    if clicks:
        set_click_animations(s, clicks)
    D.set_notes(s, speaker, start, end, script)
    SLIDES.append((s, speaker, start, end, script))


def build():
    for p in (OUT_PPTX, OUT_SCRIPT):
        if p.exists():
            sys.exit(f"{p.name} already exists: edit it in place (qf600-slides), don't regenerate.")
    prs = D.open_template()

    # 1 · title ------------------------------------------------------------
    s = D.title_slide(prs, "QF600 ASSET PRICING  ·  GROUP PROJECT  ·  GROUP 6",
                      "Did the Fed shrink the equity premium, and what should we hold now?",
                      "Replicating and stress-testing Maloney (2024) on a century of US data",
                      "Chew Junhong  ·  Marcus Tan Jun Lin  ·  Chia Chong Yee  ·  Abirame d/o Asohan  ·  Ramona Chia Ming Li",
                      "QF600 Asset Pricing · Prof Liu Peng · 04 November 2026", "Presenter 1")
    finish(s, "Presenter 1", "0:00", "0:40",
           "Good morning. We are Group 6. Our project asks a question every investor has faced since 2022: "
           "when cash pays four or five percent again, should we still hold as much in stocks? "
           "We start from Thomas Maloney's 2024 paper, Honey, the Fed Shrunk the Equity Premium, "
           "replicate it, try to prove it wrong, and turn what we find into an allocation.")

    # 2 · question + hypotheses ----------------------------------------------
    s = D.content_slide(prs, "1", "Do high rates shrink stocks' reward?", "Presenter 1")
    stat(s, "today_tbill", "3-month T-bill rate, Sep 2026: a higher-rate month", 0.4, 1.0, w=3.0, h=1.5)
    a = card(s, "txt:s2.parta", 3.7, 1.0, 5.9, 1.5, "PART A · REPLICATE THE PAPER",
             "H0: the rate level makes no difference\nH1: after high rates, stocks earn less above cash")
    b = card(s, "txt:s2.partb", 3.7, 2.7, 5.9, 1.5, "PART B · TRY TO PROVE IT WRONG",
             "H2: the Sharpe ratio holds up\nH3: a big deficit offsets high rates", highlight=True)
    finish(s, "Presenter 1", "0:40", "1:50",
           f"The T-bill rate is {R['today_tbill']} today, so by the paper's own rule we are in a higher-rate month. "
           "We wrote our hypotheses down before looking at any results, in two parts. "
           "Part A replicates the paper: H0 says the rate level makes no difference to stocks' return above cash; "
           "H1 is the paper's claim that it shrinks.\n[CLICK 1]\n"
           "Part B is ours, and tries to prove the paper wrong. H2: even if returns fall, the return per unit of risk, "
           "the Sharpe ratio, holds up. H3: a big government deficit keeps company profits growing, offsetting high rates.",
           clicks=[b])

    # 3 · data & regimes --------------------------------------------------------
    s = D.content_slide(prs, "1", "A century of rate regimes", "Presenter 1")
    fig(s, "fig01_regimes", 0.4, 0.95, 9.2)
    D.add_datanote(s, DATA_NOTE)
    finish(s, "Presenter 1", "1:50", "3:00",
           "The paper used Global Financial Data, which SMU doesn't subscribe to, so we rebuilt its dataset from free sources: "
           "Ken French for stocks and momentum, FRED for rates and the deficit, Shiller for earnings and valuation, and the World "
           "Bank for gold. Our bond series tracks Damodaran's published returns with a correlation of "
           f"{R['bond_check_corr']}. Each dot is a month; orange months are higher-rate under the paper's trailing five-year rule, "
           "the only rule an investor could have used at the time.\n→ Hand over to Presenter 2")

    # 4 · Exhibit 3 ----------------------------------------------------------------
    s = D.content_slide(prs, "2", "Replication: premiums shrink after high rates", "Presenter 2")
    fig(s, "fig02_exhibit3_replication", 0.4, 1.0, 6.4)
    lo = stat(s, "ex3_equities_lower_12m", "stocks above cash, 12 months after LOW rates", 7.0, 1.0)
    hi = stat(s, "ex3_equities_higher_12m", "after HIGH rates (paper: 10.3% vs 5.8%)", 7.0, 2.4, color="orange")
    D.add_datanote(s, "Bars = ours, diamonds = paper (Exhibit 3) · Jul 1926 – Dec 2023 · average of the paper's three regime rules")
    finish(s, "Presenter 2", "3:00", "4:30",
           "First, does the paper's result hold on its own sample? The bars are ours, the diamonds are the paper's Exhibit 3. "
           f"In the twelve months after a lower-rate month, stocks earned {R['ex3_equities_lower_12m']} a year above cash.\n[CLICK 1]\n"
           f"After a higher-rate month, only {R['ex3_equities_higher_12m']}. The paper had 10.3 and 5.8, so our free data "
           "reproduces it closely. Credit shows the same pattern; Treasuries barely change.",
           clicks=[hi])

    # 5 · H0 / H2 -----------------------------------------------------------------
    s = D.content_slide(prs, "2", "H0 rejected, and risk doesn't explain it", "Presenter 2")
    fig(s, "fig03_h2_sharpe", 0.4, 1.0, 5.8)
    stat(s, "h0_rejections", "of 6 tests reject H0 (Newey-West, 5%)", 6.5, 1.0, w=3.1, h=1.1)
    stat(s, "reg_t_ols_eq", "t-stat, rate predicts returns (paper −2.2)", 6.5, 2.25, w=3.1, h=1.1)
    h2 = stat(s, "h2_gap_paper", "Sharpe gap; 95% interval excludes 0 → H2 rejected", 6.5, 3.5, w=3.1, h=1.1, color="orange")
    finish(s, "Presenter 2", "4:30", "6:10",
           f"Formally, {R['h0_rejections']} of our 6 tests reject H0, using Newey-West errors because rate levels persist. "
           f"The paper's regression gives t of {R['reg_t_ols_eq']}, against minus 2.2 in the paper. So H1, the paper's claim, holds.\n"
           "Our first challenge, H2, asked whether high-rate periods are just calmer, so the reward per unit of risk is the same.\n[CLICK 1]\n"
           f"It isn't. The Sharpe ratio is {R['h2_sharpe_lower_paper']} after lower-rate months and {R['h2_sharpe_higher_paper']} "
           "after higher-rate months, almost exactly the paper's 0.57 and 0.31, and the bootstrap interval for the gap excludes zero. "
           "H2 is rejected.\n→ Hand over to Presenter 3",
           clicks=[h2])

    # 6 · H3 -------------------------------------------------------------------------
    s = D.content_slide(prs, "3", "H3: a big deficit doesn't offset high rates", "Presenter 3")
    fig(s, "fig04_h3_deficit", 0.4, 1.0, 5.8)
    stat(s, "eps_growth_lower", "real earnings growth after LOW rates (paper 11%)", 6.5, 1.0, w=3.1, h=1.0)
    stat(s, "eps_growth_higher", "after HIGH rates (paper 1%)", 6.5, 2.1, w=3.1, h=1.0, color="orange")
    h3 = stat(s, "h3_diff_high", "big vs small deficit, after high rates: not significant", 6.5, 3.2, w=3.1, h=1.2, color="orange")
    finish(s, "Presenter 3", "6:10", "7:40",
           f"Why do premiums shrink? The paper's answer is profits. We confirm it: real earnings grew {R['eps_growth_lower']} a year "
           f"after lower-rate months and {R['eps_growth_higher']} after higher-rate months.\n"
           "Our second challenge, H3, says a big deficit should keep profits up, because government spending becomes company income. "
           "That could explain 2024 and 2025.\n[CLICK 1]\n"
           f"It doesn't. After high-rate months, a big deficit goes with a {R['h3_diff_high']} difference in the next year's return, "
           f"with a t-stat of {R['h3_t_high']}: the wrong sign and not significant. H3 is rejected.",
           clicks=[h3])

    # 7 · OOS ----------------------------------------------------------------------------
    s = D.content_slide(prs, "3", "Right about history, weak as a forecast", "Presenter 3")
    stat(s, "oos_r2", "out-of-sample R², fitted 1926–95, tested 1996–2026", 0.4, 1.0, w=2.95, h=1.45)
    stat(s, "recent_eq_2024", "stocks above cash in 2024, a high-rate year", 3.5, 1.0, w=2.95, h=1.45, color="orange")
    stat(s, "conc_gap_2024", "S&P 500 cap-weight minus equal-weight, 2024", 6.6, 1.0, w=3.0, h=1.45, color="blue")
    stat(s, "cape_latest", "CAPE today: near its historical high", 0.4, 2.65, w=2.95, h=1.45, color="gold")
    v = card(s, "txt:s7.verdict", 3.5, 2.65, 6.1, 1.45, "VERDICT ON THE PAPER", "Partly true: real in a century of data, too weak to time markets.", highlight=True)
    finish(s, "Presenter 3", "7:40", "9:20",
           "Does the pattern forecast? We fitted the regression on 1926 to 1995 only and tested it on 1996 to 2026. "
           f"Out-of-sample R squared is {R['oos_r2']}: barely better than assuming an average return. "
           f"And 2024 broke it outright: stocks beat cash by {R['recent_eq_2024']} despite high rates. Not because of the deficit, "
           f"but because a few giant companies drove the market: the cap-weighted S&P beat the equal-weighted one by {R['conc_gap_2024']}, "
           f"and valuations are stretched, with CAPE at {R['cape_latest']}.\n[CLICK 1]\n"
           "So our verdict: partly true. Real in history, too weak to time the market with.\n→ Hand over to Presenter 4",
           clicks=[v])

    # 8 · diversifiers -------------------------------------------------------------------
    s = D.content_slide(prs, "4", "Gold and momentum protect better than bonds", "Presenter 4")
    stat(s, "s5_sharpe_6040_high", "60/40 Sharpe in high-rate months", 0.4, 1.0, w=2.95, h=1.3, color="blue")
    stat(s, "s5_sharpe_5050_high", "50/50: less risk, same Sharpe", 3.5, 1.0, w=2.95, h=1.3, color="blue")
    eq = stat(s, "s5_sharpe_1n_high", "equal weight: stocks, bonds, gold, momentum", 6.6, 1.0, w=3.0, h=1.3)
    stat(s, "s5_corr_bonds_rising", "bond–stock correlation when rates rise", 0.4, 2.5, w=2.95, h=1.3, color="orange")
    stat(s, "s5_corr_gold_rising", "gold–stock correlation when rates rise", 3.5, 2.5, w=2.95, h=1.3, color="gold")
    stat(s, "s5_cvar_1n_high", "equal-weight CVaR 5%, high rates (60/40 higher)", 6.6, 2.5, w=3.0, h=1.3)
    D.add_datanote(s, "Monthly, Feb 1960 – Sep 2026 · stocks, 10-year Treasuries, World Bank gold, momentum (T-bill + UMD)")
    finish(s, "Presenter 4", "9:20", "10:50",
           "Now, what should an investor hold? We used the longest data we have, 1960 to today, with four assets: stocks, bonds, "
           "gold and momentum. Prof Liu asked whether moving from 60/40 to 50/50 helps when rates are high. "
           f"It cuts risk, but the Sharpe ratio is the same: {R['s5_sharpe_6040_high']} against {R['s5_sharpe_5050_high']}. "
           f"Bonds are a weaker cushion when rates rise, with a correlation of {R['s5_corr_bonds_rising']} to stocks; gold stays near zero.\n"
           "[CLICK 1]\n"
           f"Holding all four in equal amounts more than doubles the Sharpe ratio, to {R['s5_sharpe_1n_high']}, with a smaller tail "
           f"loss: CVaR of {R['s5_cvar_1n_high']}.",
           clicks=[eq])

    # 9 · stock share ---------------------------------------------------------------------
    s = D.content_slide(prs, "4", "How much in stocks today?", "Presenter 4")
    fig(s, "fig05_best_share_terciles", 0.4, 1.0, 6.4)
    stat(s, "s5_wstar_high_A3", "mean-variance share, high rates (A = 3)", 7.0, 1.0, h=1.2, color="blue")
    x = stat(s, "x_stock_share", "recommended stock share today", 7.0, 2.4, h=1.4)
    finish(s, "Presenter 4", "10:50", "12:30",
           "So how much in stocks? Mean-variance says: stock share equals the premium over risk aversion times variance. "
           f"With risk aversion 3, that's {R['s5_wstar_high_A3']} after higher-rate months. Prof Liu suggested splitting history into "
           "good, middle and bad conditions. Today rates are in the middle third, stocks are expensive, and the deficit is large. "
           "Each chart shows the best stock share in each third.\n[CLICK 1]\n"
           f"Averaging the evidence gives about {R['x_stock_share']} in stocks: not zero, not all-in.\n→ Hand over to Presenter 5",
           clicks=[x])

    # 10 · backtest --------------------------------------------------------------------------
    s = D.content_slide(prs, "5", "Backtest: nothing beats simple diversification", "Presenter 5")
    fig(s, "fig06_oos_growth", 0.4, 1.0, 6.2)
    D.add_text(s, "txt:s10.head", "OUT OF SAMPLE · SHARPE · CVaR 5%", 6.8, 0.95, 2.9, 0.3, D.SIZE["kicker"], "teal", bold=True)
    for k, (code, lab) in enumerate([("b", "B  Benchmark"), ("s1", "S1  Paper"), ("s2", "S2  Rate rule"),
                                     ("s3", "S3  + Deficit"), ("s4", "S4  Ridge MV")]):
        y = 1.35 + k * 0.62
        D.add_text(s, f"txt:s10.{code}", lab, 6.8, y, 1.45, 0.5, D.SIZE["body"], "body")
        D.add_text(s, f"num:s6_oos_{code}_sharpe", R[f"s6_oos_{code}_sharpe"], 8.25, y, 0.65, 0.5, D.SIZE["body"] + 2,
                   "teal" if code == "b" else "title", D.SERIF, bold=True)
        D.add_text(s, f"num:s6_oos_{code}_cvar5", R[f"s6_oos_{code}_cvar5"], 8.95, y, 0.7, 0.5, D.SIZE["body"], "muted")
    D.add_datanote(s, "ETFs SPY, IEF, GLD, PDP (+ PSP, HYG, VNQ for S1) · fitted May 2007 – Nov 2020, tested Dec 2020 – Sep 2026 · 10 bps costs")
    finish(s, "Presenter 5", "12:30", "13:50",
           "Finally, we tested the ideas with real ETFs. Everything was chosen on the first 70 percent of the data, 2007 to 2020, and "
           "judged only on the last 30 percent, December 2020 to September 2026, which includes the high-rate years. "
           f"The benchmark simply holds stocks, bonds, gold and momentum in equal amounts and never trades. Its Sharpe ratio is "
           f"{R['s6_oos_b_sharpe']}. The paper's own portfolios score {R['s6_oos_s1_sharpe']}; our rate rule {R['s6_oos_s2_sharpe']}; "
           f"adding the deficit {R['s6_oos_s3_sharpe']}. The optimised portfolio had a significant alpha in-sample, which vanished "
           "out of sample: Lecture 5's error maximiser in action.")

    # 11 · Monte Carlo ------------------------------------------------------------------------
    s = D.content_slide(prs, "5", "Next 10 years: diversification wins either way", "Presenter 5")
    fig(s, "fig07_monte_carlo", 0.4, 1.0, 6.4)
    stat(s, "mc_high_b_med", "benchmark, rates stay high (median per year)", 7.0, 1.0, h=1.15)
    stat(s, "mc_high_s2_med", "rate rule, rates stay high", 7.0, 2.3, h=1.15, color="blue")
    stat(s, "mc_stress_s2_med", "rate rule if rates never fall", 7.0, 3.6, h=1.15, color="orange")
    finish(s, "Presenter 5", "13:50", "14:50",
           "We also simulated the next ten years, 2,000 times, with rates switching as often as they have in history. "
           f"If rates stay high, the benchmark's median return is {R['mc_high_b_med']} a year, against {R['mc_high_s2_med']} for the "
           f"rate rule. If rates never come down, cutting stocks for bonds does even worse: {R['mc_stress_s2_med']}.")

    # 12 · conclusion -----------------------------------------------------------------------------
    s = D.content_slide(prs, "✓", "CONCLUSION", "Presenter 5")
    card(s, "txt:s12.message", 0.4, 0.95, 9.2, 1.0, "CENTRAL MESSAGE",
         "Being in the middle doesn't mean retreating to risk-free.", highlight=True)
    stat(s, "x_stock_share", "stocks, held with bonds, gold and momentum", 0.4, 2.1, w=2.95, h=1.3)
    stat(s, "s6_oos_b_sharpe", "benchmark Sharpe out of sample: best of all", 3.5, 2.1, w=2.95, h=1.3, color="blue")
    stat(s, "oos_r2", "rate signal R² out of sample: too weak to time", 6.6, 2.1, w=3.0, h=1.3, color="orange")
    card(s, "txt:s12.next", 0.4, 3.55, 9.2, 1.1, "NEXT STEPS",
         "1  Real cash-plus funds as their history grows   2  Add valuation to the rate rule   3  Test other countries")
    D.add_datanote(s, "Coursework only. Past returns do not predict future returns. Not investment advice. "
                      "Prepared with the assistance of Claude (Anthropic); all results were checked by the Group.")
    finish(s, "Presenter 5", "14:50", "15:40",
           "To conclude. High rates do shrink the equity premium: the paper is right about history, and the gap isn't explained by "
           "risk or by the deficit. But the signal is too weak to trade. So our central message: being in the middle doesn't mean "
           f"retreating to risk-free. Hold about {R['x_stock_share']} in stocks, alongside bonds, gold and momentum, and keep it steady "
           "rather than switching on the level of rates. Thank you, and we're happy to take questions.")

    # annexes (backup, shown only if asked) ---------------------------------------------------------
    s = D.content_slide(prs, "A", "Annex A: key charts", "Presenter 5")
    fig(s, "fig02_exhibit3_replication", 0.4, 1.0, 4.5)
    fig(s, "fig06_oos_growth", 5.1, 1.0, 4.5)
    finish(s, "Presenter 5", "15:40", "15:50", "Backup slide, only if asked: the replication of Exhibit 3 and the out-of-sample backtest.")
    s = D.content_slide(prs, "B", "Annex B: tests of H2 and H3", "Presenter 5")
    fig(s, "fig03_h2_sharpe", 0.4, 1.0, 4.5)
    fig(s, "fig04_h3_deficit", 5.1, 1.0, 4.5)
    finish(s, "Presenter 5", "15:50", "16:00", "Backup slide, only if asked: the Sharpe-ratio test (H2) and the deficit test (H3).")

    prs.save(OUT_PPTX)

    # ---------------------------------------------------------------- script
    doc = Document(str(ROOT / "templates" / "script_template.docx"))
    for p in list(doc.paragraphs)[2:]:
        p._element.getparent().remove(p._element)
    current = None
    for n, (s, speaker, start, end, script) in enumerate(SLIDES, 1):
        title = next(sh.text_frame.text for sh in s.shapes if sh.name == "title")
        if speaker != current:
            doc.add_heading(f"{speaker}", 1)
            current = speaker
        doc.add_heading(f"Slide {n} · {title}", 2)
        meta = doc.add_paragraph(f"Speaker: {speaker} · Start {start} · End {end}")
        meta.runs[0].italic = True
        for line in script.split("\n"):
            p = doc.add_paragraph(line)
            if line.startswith("[CLICK") or line.startswith("→"):
                p.runs[0].bold = True
            for r in p.runs:
                r.font.size = Pt(12)
    doc.save(OUT_SCRIPT)
    print(f"wrote {OUT_PPTX.name} ({len(SLIDES)} slides) and {OUT_SCRIPT.name}")


if __name__ == "__main__":
    build()
