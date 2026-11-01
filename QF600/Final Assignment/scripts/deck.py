"""Slide building blocks in the Group 6 house style (context/08_slide_style.md).

Every helper names its shapes so sync tools can find them:
    title, badge, page, datanote, tag:speaker, fig:<id>, num:<key>, txt:<key>

    from deck import *
    prs = open_template()
    s = content_slide(prs, badge="2", title="Stocks earned less above cash after high rates",
                      speaker="Presenter 2")
    add_figure(s, "fig02_ex3_bars", x=0.4, y=0.95, w=6.0)
    add_card(s, "txt:s2.fix", x=6.7, y=0.95, w=2.9, h=2.0, kicker="PAPER · EXHIBIT 3",
             body="Lower: 10.3%  ·  Higher: 5.8%", highlight=True)
    set_notes(s, "Presenter 2", "3:10", "4:00", "Script…\\n[CLICK 1]\\nMore script…")
    prs.save("04 - Presentation Slides Group 6.pptx")
"""
from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "slides_template.pptx"

C = {k: RGBColor.from_string(v) for k, v in {
    "bg": "1A1D1C", "card": "262A29", "card_hi": "1F3A34", "card_warm": "3D2A21",
    "title": "EEF0EF", "body": "C8CECB", "muted": "9EA6A3",
    "teal": "5CC6A7", "blue": "5B8DEF", "orange": "E2692F", "gold": "F0B64A"}.items()}
SIZE = {"title": 24, "stat": 28, "card_head": 18, "body": 14, "kicker": 12,
        "caption": 11, "tag": 12, "table": 12, "page": 8}
SERIF, SANS = "Cambria", "Calibri"


def open_template() -> Presentation:
    return Presentation(str(TEMPLATE))


def _bg(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = C["bg"]


def add_text(slide, name, text, x, y, w, h, size=SIZE["body"], color="body", font=SANS,
             bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = name
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    for m in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, m, 0)
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        r = p.add_run()
        r.text = line
        r.font.size, r.font.name, r.font.bold = Pt(size), font, bold
        r.font.color.rgb = C[color]
    return tb


def _rect(slide, name, x, y, w, h, fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.name = name
    sh.fill.solid()
    sh.fill.fore_color.rgb = C[fill]
    sh.line.fill.background()
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        sh.adjustments[0] = 0.06
    return sh


def _fixed(slide, badge, title, speaker, page):
    _rect(slide, "badge_bg", 0.40, 0.30, 0.36, 0.36, "teal", MSO_SHAPE.OVAL)
    add_text(slide, "badge", badge, 0.40, 0.30, 0.36, 0.36, 13, "bg", SANS, True,
             PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    add_text(slide, "title", title, 0.92, 0.24, 7.25, 0.50, SIZE["title"], "title", SERIF,
             anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, "tag:speaker", speaker, 8.20, 0.30, 1.40, 0.36, SIZE["tag"], "muted",
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, "page", str(page), 9.25, 5.30, 0.35, 0.20, SIZE["page"], "muted", align=PP_ALIGN.RIGHT)


def content_slide(prs, badge, title, speaker):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    _bg(s)
    _fixed(s, badge, title, speaker, len(prs.slides))
    return s


def title_slide(prs, kicker, question, subtitle, members, footer, speaker):
    s = prs.slides.add_slide(prs.slide_layouts[0])
    for ph in list(s.placeholders):
        ph._element.getparent().remove(ph._element)
    _bg(s)
    add_text(s, "tag:speaker", speaker, 8.20, 0.30, 1.40, 0.36, SIZE["tag"], "muted",
             align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, "kicker", kicker, 0.6, 0.9, 8.5, 0.3, SIZE["kicker"], "teal", bold=True)
    add_text(s, "title", question, 0.6, 1.3, 8.8, 1.3, 32, "title", SERIF)
    add_text(s, "subtitle", subtitle, 0.6, 2.75, 8.8, 0.5, 16, "body")
    add_text(s, "members", members, 0.6, 4.35, 8.8, 0.3, SIZE["body"], "body")
    add_text(s, "footer", footer, 0.6, 4.85, 8.8, 0.3, SIZE["caption"], "muted")
    return s


def add_card(slide, name, x, y, w, h, kicker="", body="", highlight=False, warm=False):
    _rect(slide, f"bg.{name}", x, y, w, h, "card_warm" if warm else ("card_hi" if highlight else "card"))
    if kicker:
        add_text(slide, f"kicker.{name}", kicker, x + 0.15, y + 0.12, w - 0.3, 0.25, SIZE["kicker"], "teal", bold=True)
    return add_text(slide, name, body, x + 0.15, y + (0.45 if kicker else 0.15), w - 0.3,
                    h - (0.6 if kicker else 0.3), SIZE["body"], "body")


def add_stat(slide, key, value, label, x, y, w=2.6, h=1.5, color="teal"):
    """Big number tile. `key` is the results.json key → shape num:<key>."""
    _rect(slide, f"bg.num:{key}", x, y, w, h, "card")
    add_text(slide, f"num:{key}", value, x + 0.15, y + 0.12, w - 0.3, 0.6, SIZE["stat"], color, SERIF)
    add_text(slide, f"label.{key}", label, x + 0.15, y + 0.78, w - 0.3, h - 0.9, SIZE["body"], "body")


def add_figure(slide, fig_id, x, y, w=None, h=None):
    png = ROOT / "figures" / f"{fig_id}.png"
    pic = slide.shapes.add_picture(str(png), Inches(x), Inches(y),
                                   Inches(w) if w else None, Inches(h) if h else None)
    pic.name = f"fig:{fig_id}"
    return pic


def add_datanote(slide, text):
    add_text(slide, "datanote", text, 0.40, 5.05, 8.7, 0.3, SIZE["caption"], "muted")


def set_notes(slide, speaker, start, end, script):
    """Notes header '[NAME · m:ss–m:ss]' then the script (with [CLICK n] markers)."""
    slide.notes_slide.notes_text_frame.text = f"[{speaker.upper()} · {start}–{end}]\n{script.strip()}"
