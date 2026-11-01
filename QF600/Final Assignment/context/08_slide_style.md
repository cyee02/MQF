# 08 · Slide style (for `04 - Presentation Slides Group 6.pptx`)

Extracted from the group's two earlier decks in `reference_style/`:
- `QF600_Asset Pricing Grp Homework #1_Grp 6v2.pptx` (HW1, 22 slides)
- `QF600_Group HW (Updated Slides) 30 09 26.pptx` (HW2, 12 slides, **the primary template**)

Both decks share one look. HW2 is the cleaner one to copy.

## 1. Canvas
- **16:9, 10.0 × 5.625 in** (9,144,000 × 5,143,500 EMU), one layout (`slideLayout1`).
- **Dark background `#1A1D1C`** set per slide (not on the master).
- No animations in the references (no `<p:timing>`). We add them (see §6).

## 2. Palette (hex)

| Role | Hex | Use |
|------|-----|-----|
| Background | `1A1D1C` | Slide fill |
| Card | `262A29` | Rounded panels / stat boxes |
| Highlight card | `1F3A34` | "THE FIX · LECTURE" / key-insight panels |
| Warm card | `3D2A21` | Warning / cost panels |
| Title text | `EEF0EF` | Titles, big numbers |
| Body text | `C8CECB` | Paragraphs |
| Muted text | `9EA6A3` | Captions, speaker tag, page number, data notes |
| **Accent teal** | `5CC6A7` | Primary accent: section badge, labels, key numbers |
| Accent blue | `5B8DEF` | Series 2 / comparison |
| Accent orange | `E2692F` | Series 3 / risk / negative |
| Accent gold | `F0B64A` | Series 4 / gold |

Charts use the same accents in this order: teal, blue, orange, gold. Chart backgrounds are transparent or `1A1D1C`; gridlines `262A29`.

## 3. Typography

| Element | Font | Reference size | **Our minimum (big-screen rule)** |
|---------|------|----------------|------------------------------------|
| Slide title | Cambria | 21 pt | **24 pt** |
| Big stat number | Cambria | 18–20 pt | **28 pt** |
| Card heading | Cambria | 18 pt | 18 pt |
| Body text | Calibri | 8.5–9.5 pt | **14 pt** |
| Label / kicker (CAPS) | Calibri | 9 pt, teal | **12 pt** |
| Caption / data note | Calibri | 8 pt, muted | **11 pt** |
| Speaker tag | Calibri | 9 pt, muted | **12 pt** |
| Table text | Calibri | 10 pt | **12 pt** |
| Chart text (rendered on slide) | — | — | **≥ 12 pt at final size** |

The references are dense (8–9 pt body). The user asked for figures readable on a big screen and few words, so **our minimums override the reference sizes**. Keep fonts and colours, raise sizes, and cut words to fit.

## 4. Fixed elements on every content slide (positions in inches from top-left)

| Element | Position (x, y, w, h) | Style |
|---------|----------------------|-------|
| Section badge (circle) | 0.40, 0.30, 0.36, 0.36 | teal fill `5CC6A7`, number in `1A1D1C` Calibri 13 pt |
| Title | 0.92, 0.26, 7.30, 0.45 | Cambria, `EEF0EF` |
| **Speaker tag** | **8.30, 0.30, 1.30, 0.36** (top-right corner) | Calibri, `9EA6A3`. Text = presenter name (placeholder `Presenter n` until confirmed) |
| Page number | 9.30, 5.30, 0.30, 0.20 | Calibri 8 pt `9EA6A3` |
| Data note (optional) | bottom-left, ≈ 0.40, 5.05 | Calibri, muted: "Data: … · Source: …" |

The speaker tag is **mandatory on every slide**, including the title, conclusion and annex slides (guideline R3.3). On the title slide, list all five members in the subtitle line, in title-slide order (`context/09`).

## 5. Slide patterns used in the references
- **Title slide:** kicker line `QF600 ASSET PRICING · GROUP PROJECT` (caps, teal) → big question as title (one accent word in teal) → one-line description → key equation box → member names line → footer line (course · group · deliverable).
- **Content slide:** badge + title stating the *finding* (not the topic), e.g. "Task 2: naive MVO is an error maximiser". Left: chart/table (≈ 60% width). Right: 1–2 cards (a `1F3A34` "THE FIX · LECTURE" card with the formula, and a `262A29` stat card with a big teal number + one line).
- **Conclusion slide:** title `CONCLUSION`; one-sentence answer with one teal phrase; 3–4 stat tiles (big number + label); `NEXT STEPS` numbered list; closing line "Thank you, and happy to take questions."; disclaimer line in muted text.
- **Annex slides:** badge letter (`A`, `B`), title `Annex A: …`, speaker tag reads `Annex` in HW2. **We use the presenter's name instead** (guideline R3.3).
- **Disclaimers (bottom of conclusion slide):** "Coursework only. Past returns do not predict future returns. Not investment advice." and "Prepared with the assistance of Claude (Anthropic) for code review and slide drafting. All results were checked by the Group."

## 6. Speaker notes = presenter script
Every slide's notes start with a header line in this exact format (from the references):

```
[PRESENTER 2 · 2:20–3:00]
```

i.e. `[<NAME IN CAPS> · <start m:ss>–<end m:ss>]`, then the script in plain spoken sentences. Our additions:
- `[CLICK n]` on its own line at the point the presenter clicks for animation n (n = 1, 2, …). The number of `[CLICK n]` markers must equal the number of click-triggered animations on the slide.
- A last line `→ Hand over to <next presenter>` on each presenter's final slide.
- Timing: cumulative start/end times, ≈ 3:00 per presenter, **total ≤ 16:00** to leave ≥ 4 min Q&A (guideline R4.1).

## 7. Words and figures
- **≤ 40 words of body text per slide** (excluding title, tag, data note).
- One message per slide. The title says the finding.
- One main figure per slide, ≥ 55% of slide width. Exported from the notebook at 2× scale; chart text ≥ 12 pt **as rendered on the slide**.
- Prefer a big stat tile over a sentence.
- Tables ≤ 5 rows × 5 columns on a slide. Longer tables go to the annex or the report.

## 8. Animations (when necessary)
Use only **Appear / Fade on click** to build an argument step by step (e.g. reveal "higher-rate" bars after "lower-rate" bars; reveal the conclusion tile last). No motion paths or flying entrances. python-pptx cannot create animations directly, so `scripts/pptx_anim.py` injects `<p:timing>` XML for named shapes. Each click = one `[CLICK n]` in the notes.
