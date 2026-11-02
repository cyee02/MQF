"""Build the three templates in templates/ (run once; the templates are committed).

    python scripts/build_templates.py

slides_template.pptx  HW2 deck's master/theme with every slide removed (needs the
                      team bundle's reference_style/ deck; skipped if absent).
report_template.docx  Cover, executive summary, numbered sections, Annex A,
                      references and AI-assistance statement, in house fonts.
script_template.docx  One section per slide: "Slide n · Title", speaker/timing line, script.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_BREAK
from docx.shared import Pt, RGBColor
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]
T = ROOT / "templates"
REF_DECK = ROOT / "reference_style" / "QF600_Group HW (Updated Slides) 30 09 26.pptx"
TEAL = RGBColor(0x1F, 0x7A, 0x63)


def slides_template():
    if not REF_DECK.exists():
        print(f"skip slides template: {REF_DECK.name} not found (unpack the team bundle)")
        return
    prs = Presentation(str(REF_DECK))
    sldIdLst = prs.slides._sldIdLst
    for sldId in list(sldIdLst):
        prs.part.drop_rel(sldId.rId)
        sldIdLst.remove(sldId)
    # The reference deck's notes master has no body placeholder, so new notes
    # slides get no text frame. Drop it; python-pptx then creates a standard one.
    pres = prs.part._element
    nm = pres.find("{http://schemas.openxmlformats.org/presentationml/2006/main}notesMasterIdLst")
    if nm is not None:
        for rel in [r for r in prs.part.rels.values() if r.reltype.endswith("/notesMaster")]:
            prs.part.drop_rel(rel.rId)
        pres.remove(nm)
    prs.save(T / "slides_template.pptx")
    print("templates/slides_template.pptx")


def _styles(doc):
    st = doc.styles
    st["Normal"].font.name, st["Normal"].font.size = "Calibri", Pt(11)
    for lvl, size in [(1, 16), (2, 13), (3, 11.5)]:
        s = st[f"Heading {lvl}"]
        s.font.name, s.font.size, s.font.color.rgb, s.font.bold = "Cambria", Pt(size), TEAL, True
    st["Title"].font.name, st["Title"].font.size = "Cambria", Pt(26)


def report_template():
    doc = Document()
    _styles(doc)
    doc.add_paragraph("QF600 Asset Pricing · Group Project", style="Subtitle")
    doc.add_paragraph("Honey, the Fed Shrunk the Equity Premium: does it still hold, and what should an investor hold now?",
                      style="Title")
    doc.add_paragraph("Group 6 · Chew Junhong · Marcus Tan Jun Lin · Chia Chong Yee · Abirame d/o Asohan · Ramona Chia Ming Li")
    doc.add_paragraph("Submitted 03 November 2026")
    doc.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)

    doc.add_heading("Executive Summary", 1)
    doc.add_paragraph("[One page, ≤ 450 words: question, method, three key numbers, central message, recommendation.]")
    doc.paragraphs[-1].add_run().add_break(WD_BREAK.PAGE)

    sections = [
        ("1 Research Problem and Impact", "[R2.3 Define the problem and why it matters to an investor.]"),
        ("2 Data", "[Sources, frequency, period, proxies vs the paper. Full detail in Annex A.]"),
        ("3 Replication of the Paper", "[R2.4 Exhibit 3, regression, Exhibit 9. Step 2.]"),
        ("4 Why: Profits and the Deficit", "[Step 3, H2.]"),
        ("5 Does It Still Hold? Out-of-Sample Tests", "[Step 4. Prof points 2, 3, 5.]"),
        ("6 What Should an Investor Hold?", "[Step 5. Prof points 4, 6–11.]"),
        ("7 Strategies and Backtests", "[Step 6. S0–S6, walk-forward, Monte Carlo.]"),
        ("8 Verdict and Central Message", "[R2.5 Solution and recommendation.]"),
        ("9 Performance Measures and Evaluation Metrics", "[R2.6 Sharpe, max drawdown, CVaR 5%, CE, t-stats, turnover.]"),
        ("10 Limitations and Next Steps", "[R2.7 No need to beat benchmarks: state what failed honestly.]"),
    ]
    for head, body in sections:
        doc.add_heading(head, 1)
        doc.add_paragraph(body)
    doc.add_heading("References", 1)
    doc.add_paragraph("Maloney, T. (2024). Honey, the Fed Shrunk the Equity Premium: Asset Allocation in a "
                      "Higher-Rate World. The Journal of Portfolio Management, 50(6).")
    doc.add_paragraph("Pun, C. S., Wang, T., & Yan, Z. Data-Driven Distributionally Robust CVaR Portfolio "
                      "Optimization under Regime-Switching Ambiguity Set. SSRN 4378930.")
    doc.add_heading("Annex A Datasets", 1)
    doc.add_paragraph("[Generated from 02 - Dataset Metadata Group 6.md: source, description, rows, columns.]")
    doc.add_heading("Annex B Additional Results", 1)
    doc.add_paragraph("[Robustness tables, per-rule breakdowns.]")
    doc.add_heading("AI Assistance Statement", 1)
    doc.add_paragraph("Prepared with the assistance of Claude (Anthropic) for code review and drafting. "
                      "All results were checked by the Group.")
    doc.save(T / "report_template.docx")
    print("templates/report_template.docx")


def script_template():
    doc = Document()
    _styles(doc)
    doc.add_paragraph("QF600 Group 6 · Presentation Script (not submitted)", style="Title")
    doc.add_paragraph("Generated alongside 04 - Presentation Slides Group 6.pptx. Each section matches one slide: "
                      "speaker, start/end time, and the script. [CLICK n] marks an animation click.")
    doc.add_heading("Slide 1 · <title>", 2)
    doc.add_paragraph("Speaker: Presenter 1 · Start 0:00 · End 0:40")
    doc.add_paragraph("<script>")
    doc.save(T / "script_template.docx")
    print("templates/script_template.docx")


if __name__ == "__main__":
    T.mkdir(exist_ok=True)
    slides_template()
    report_template()
    script_template()
