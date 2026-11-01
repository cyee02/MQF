# 07 · Notebook style (for `03 - execution_script_group_6.ipynb`)

Distilled from the QF627 pre-course notebooks (`reference_style/QF627_PreCourse_0[1-4]_*.ipynb`, gitignored, in the team bundle). Lessons 3 (pandas) and 4 (lets-plot) are the closest models. **Follow this file; you don't need the originals.**

## 1. Notebook skeleton

```markdown
# QF600 · Asset Pricing
## Group Project · Group 6 · Equity Risk Premium in a Higher-Rate World · `Execution Script`
```

```markdown
> One-paragraph framing in a blockquote: what this notebook does and the question it answers.
```

```markdown
## 👉 <a id="top">Table of contents</a> 👈

1. [Setup](#s0)
2. [Data & hypotheses](#s1)
3. [Replication of the paper](#s2)
...
```

Every section header follows this exact pattern, with an anchor and a back-link:

```markdown
## <a id="s2">2 · Replication of the paper</a>

[↑ Contents](#top)
```

Sub-sections use `###`; the workflow labels from Lesson 2 are `#### IMPORT`, `#### WRANGLE`, `#### MODEL`, `#### REPORT`, `#### VISUALIZE`. Use them inside sections where they fit.

Use `<mark>…</mark>` sparingly for the one sentence per section the reader must not miss (e.g. the result).

## 2. Narration
- A short markdown cell **before** each code block saying what it does and why (1–3 sentences, plain words).
- A markdown cell **after** each key result saying what it shows: "Stocks earned 9.1% a year above cash after low-rate years vs 6.7% after high-rate years." Write numbers into the text via the results registry (§5), never by hand.
- Cite the paper/lecture inline: `(Maloney 2024, p.6, Exhibit 3)`, `(Lecture 5, slide 14)`.

## 3. Code style
Imports in one setup cell at the top, standard aliases:

```python
import numpy as np
import pandas as pd
import datetime as dt

from lets_plot import *
LetsPlot.setup_html()
```

Method chaining in parentheses, one step per line, with `=\` assignment (the QF627 house style):

```python
prices =\
(
    pd
    .read_csv("datasets/etf_prices_daily.csv",
              index_col = "Date",
              parse_dates = ["Date"]
             )
    .resample("ME")
    .last()
)
```

- Spaces around `=` in keyword arguments (`index_col = "Date"`). This is the course style, even though it isn't PEP 8.
- Short comments at the end of a line in a chain (`.set_index("Date") # "Date" becomes .index`).
- `snake_case` variables; long, descriptive names are fine (`buy_and_hold_equity_curves`).
- Tidy/LONG frames (`melt`) before plotting.
- Inspect with `.info()`, `.shape`, `.head()` after loading. Keep it brief in the final notebook.
- Read the FRED key from `credentials.yaml` (`creds["fred_key"]`). **Never hard-code keys.**

## 4. Plotting (lets-plot grammar of graphics)

```python
regime_chart =\
(
    ggplot(rates_LONG,
           aes(x = "Date",
               y = "Rate")
          )
    + geom_line(aes(color = "Series"))
    + labs(title = "Three-month T-bill rate and higher-rate regimes",
           subtitle = "Jan 1926 – Oct 2026",
           caption = "Source: FRED TB3MS; Ken French RF",
           x = "",
           y = "Annual rate (%)")
    + theme(legend_position = "top")
    + ggsize(1000, 500)
)
regime_chart
```

- Always `labs(title, subtitle, caption = "Source: …", x, y)`.
- `facet_grid` / `facet_wrap` for small multiples; `gggrid([...], ncol = 1)` for dashboards.
- `geom_smooth(method = "loess")` for trends, not `"lm"`.
- **Slide-ready export:** every figure that goes into the report or slides is saved with `ggsave(plot, "figures/<fig_id>.png", scale = 2)` (or `.svg`), with base font ≥ 14 pt (`theme(text = element_text(size = 14))`). See `context/08` for size rules.

## 5. Results registry (project rule, not from QF627)
Every number quoted in the report, slides or script comes from one helper, so `qf600-sync-check` can trace it:

```python
results = {}
def record(key, value, fmt = "{:.1%}", note = ""):
    results[key] = {"value": float(value), "display": fmt.format(value), "note": note}
    return value
```

At the end of the notebook: write `outputs/results.json`. Keys are `snake_case` and stable, e.g. `ex3_eq_lower_12m`, `reg_tbill_t_eq`, `s0_sharpe`. Figure IDs are also stable: `fig01_regimes`, `fig02_ex3_bars`, ...

## 6. Section order
Matches `context/02` (notebook § = walkthrough step): §0 Setup · §1 Data & hypotheses · §2 Replication · §3 Profits & deficit · §4 Out-of-sample · §5 Allocation · §6 Backtest & simulation · §7 Results export.
