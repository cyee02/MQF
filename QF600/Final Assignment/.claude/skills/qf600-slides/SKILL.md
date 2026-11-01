---
name: qf600-slides
description: QF600 final project only. Create or update 04 - Presentation Slides Group 6.pptx AND 05 - Presentation Script.docx together for the Group 6 presentation (04 Nov 2026, 20 min incl. Q&A), in the group's dark house style, with a speaker tag on every slide, big-screen-readable figures, few words, click animations, and speaker notes holding script, timing and [CLICK n] cues. Use for any slide, deck, presentation, speaker-notes or script request in QF600/Final Assignment. Not for QF620.
---

# QF600 slides + script

Scope: `04 - Presentation Slides Group 6.pptx` and `05 - Presentation Script.docx`, always edited **together**. Python: `.venv/bin/python`; helpers in `scripts/deck.py`, `scripts/pptx_anim.py`, `scripts/office_anchors.py`.

## Read first
- `context/08_slide_style.md`: canvas, palette, **minimum font sizes**, fixed elements, notes format, animation rules.
- `context/09_group.md`: presenter placeholders and time budget. Use `Presenter 1`…`Presenter 5` until the mapping is confirmed there.
- `context/02_execution_plan.md`: slide skeleton; `context/10_prof_feedback.md`: which slide answers which point.
- `context/01_requirements.md`: R3.x, R4.1.

## Create (only if the deck doesn't exist)
`prs = deck.open_template()` (from `templates/slides_template.pptx`), then build slides with `deck.title_slide(...)` / `deck.content_slide(prs, badge, title, speaker)`. These add the named fixed elements (`title`, `badge`, `tag:speaker`, `page`). Save as `04 - Presentation Slides Group 6.pptx`.

## Every slide must have
1. **Speaker tag** top-right (`tag:speaker`), including the title, conclusion and annex slides (R3.3).
2. A **title that states the finding**, ≤ 12 words.
3. **≤ 40 words** of body text. Prefer one figure + one stat tile.
4. **Figures** via `deck.add_figure(slide, fig_id, x, y, w)` from `figures/` (shape `fig:<id>`), ≥ 55% of slide width; chart text ≥ 12 pt as rendered. If a figure isn't readable at that size, re-export it from the notebook (`qf600-notebook`) instead of shrinking text.
5. **Numbers** via `deck.add_stat(slide, key, display, label, …)` (shape `num:<key>`), with `display` from `outputs/results.json`.
6. **Speaker notes** via `deck.set_notes(slide, speaker, start, end, script)`: header `[NAME · m:ss–m:ss]`, spoken script, `[CLICK n]` on its own line where the presenter clicks, and `→ Hand over to <next presenter>` on each presenter's last slide.
7. **Animations only when they help the argument** (reveal step by step): `pptx_anim.set_click_animations(slide, [["fig:…"], ["num:…"]])`. Each inner list = one click; the count must equal the `[CLICK n]` markers.

## Deck rules
- Order follows `context/02` skeleton; end with a CONCLUSION slide (central message, stat tiles, NEXT STEPS, disclaimers from `context/08` §5), then **Annex** slides with the key visuals (R3.4).
- Timings contiguous from 0:00; ≈ 3:00 per presenter; **talk ends ≤ 16:00** (R4.1); every presenter has ≥ 1 slide (R3.2).
- Existing deck: edit only the shapes/notes you were asked to change; keep hand edits. Back up to `.sync/backups/<timestamp>/` first and ask the user to close PowerPoint.

## The script (05)
Mirror the deck exactly: for each slide a Heading 2 `Slide n · <title>`, then `Speaker: <name> · Start m:ss · End m:ss`, then the script paragraphs (same text and `[CLICK n]` markers as the notes). Start from `templates/script_template.docx` if 05 doesn't exist. Group each presenter's slides together so each member can print their part.

## After editing
Run the `qf600-sync-check` skill. C3 (titles/speakers), C4 (timings), C5 (clicks) and C7 (guideline) must pass.
