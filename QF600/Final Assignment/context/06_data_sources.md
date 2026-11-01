# 06 · Data sources

Registry of every dataset the project uses. **`qf600-data-sync` keeps this file, `02 - Dataset Metadata Group 6.md` and `.sync/datasets.json` in step.** Add a row here *before* writing download code.

- **Status:** `planned` (not yet downloaded) · `downloaded` (file in `datasets/`) · `pending-user` (user to supply) · `dropped`.
- **Method:** `script` (notebook §1 or `scripts/download_data.py`) · `manual` (download by hand, share via `qf600-bundle`).
- **Key:** name of the `credentials.yaml` entry, if an API key is needed.
- Filenames are what the file must be called in `datasets/`.
- **Series IDs and URLs marked ⚠ must be checked on first download** (sites move files).

## Core datasets

| ID | Dataset | Provider | Series / URL | Freq | Period needed | Method | Key | Expected file | Status |
|----|---------|----------|--------------|------|---------------|--------|-----|---------------|--------|
| D01 | 3-month T-bill rate (secondary market) | FRED | `TB3MS` | Monthly | 1934-01 → latest | script | `fred_key` | `fred_tb3ms.csv` | planned |
| D02 | Fama-French 3 factors (Mkt-RF, SMB, HML, **RF**) | Ken French Data Library | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip` | Monthly | 1926-07 → latest | script | — | `ff3_monthly.csv` | planned |
| D03 | Momentum factor (**UMD** / Mom) | Ken French Data Library | `…/ftp/F-F_Momentum_Factor_CSV.zip` | Monthly | 1927-01 → latest | script | — | `ff_umd_monthly.csv` | planned |
| D04 | 10-year Treasury yield | FRED | `GS10` | Monthly | 1953-04 → latest | script | `fred_key` | `fred_gs10.csv` | planned |
| D05 | Moody's Aaa / Baa corporate yields | FRED | `AAA`, `BAA` | Monthly | 1919-01 → latest | script | `fred_key` | `fred_aaa_baa.csv` | planned |
| D06 | Federal surplus/deficit, % of GDP | FRED | `FYFSGDA188S` ⚠ | Annual (fiscal yr) | 1929 → latest | script | `fred_key` | `fred_deficit_gdp.csv` | planned |
| D07 | Federal interest outlays, % of GDP (for primary deficit) | FRED | `FYOIGDA188S` ⚠ | Annual | 1940 → latest | script | `fred_key` | `fred_interest_gdp.csv` | planned |
| D08 | Monthly Treasury statement surplus/deficit (recent detail) | FRED | `MTSDS133FMS` ⚠ | Monthly | 1980 → latest | script | `fred_key` | `fred_mts_deficit.csv` | planned |
| D09 | CPI (all urban, NSA) | FRED | `CPIAUCNS` | Monthly | 1913 → latest | script | `fred_key` | `fred_cpi.csv` | planned |
| D10 | S&P composite price, dividends, earnings, real EPS, **CAPE** | Robert Shiller | `ie_data.xls` ⚠ (shillerdata.com / econ.yale.edu/~shiller/data) | Monthly | 1871 → latest | manual | — | `shiller_ie_data.xls` | planned |
| D11 | Historical annual returns: S&P 500, 3M T-bill, 10Y T-bond, Baa corp, real estate, gold | Aswath Damodaran (NYU Stern) | `https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls` ⚠ | Annual | 1928 → 2025 | manual | — | `damodaran_histretSP.xls` | **pending-user** |
| D12 | ETF adjusted closes: SPY, IEF, TLT, HYG, VNQ, PSP, GLD, RSP | Yahoo Finance via `yfinance` | tickers | Daily → resample monthly | 2005-01 → latest (HYG from 2007-04) | script | — | `etf_prices_daily.csv` | planned |
| D13 | Global Financial Data (Finaeon) | GFD | API | — | — | — | — | — | **pending-user** (decide whether used; notebook has a trial-login cell) |

## Proxies vs the paper (see `context/03` §2)

| Paper series | Our proxy | Gap to state in the report |
|--------------|-----------|----------------------------|
| 3M T-bill 1926–33 (GFD) | Ken French `RF` (1-month T-bill) for 1926-07 → 1933-12, then `TB3MS` | 1-month vs 3-month bill; RF is a monthly *return*, annualise ×12 |
| US equity returns (GFD) | `Mkt-RF + RF` (CRSP VW, all NYSE/AMEX/NASDAQ) | Broader than S&P 500 |
| Treasury returns (GFD) | Damodaran annual T-bond return; monthly approx. from `GS10`: r ≈ y_{t−1}/12 − D·Δy (D ≈ 8) | Approximation; check vs Damodaran annual |
| IG credit excess (Asvanunt & Richardson) | Damodaran Baa − T-bond (annual); monthly approx. from `BAA` yield | Not duration-matched |
| Hedge-fund EMN / trend indices | `RF + UMD` | Single-factor stand-in |
| Private equity index | PSP | Listed PE, high equity beta |
| Real estate index | VNQ | Listed REITs |

## Derived series (computed in the notebook, not stored as raw data)

| Name | Formula | Used in |
|------|---------|---------|
| `rf_m` | T-bill rate (annual %) → monthly decimal | everywhere |
| `regime_m1/m2/m3` | rules in `context/03` §3 | step 2 |
| `xret_eq` | Mkt-RF (already excess) | steps 2–6 |
| `mom_cashplus` | RF + UMD | H2, S5 |
| `primary_deficit_gdp` | −(FYFSGDA188S) − FYOIGDA188S (sign so positive = deficit) | step 3, S3 |
| `cape_gap` | 1/CAPE − real 10-yr yield (or CAPE vs its trailing median) | step 5 terciles |

## Adding a new dataset (checklist; `qf600-data-sync` follows it)
1. Add a row above (ID, provider, series/URL, freq, period, method, key, filename, status `planned`).
2. If it needs an API key: add the key name to `credentials.example.yaml`, and README step 8 (how to get the key). See `plan.md` §5.1.
3. Write the download code in notebook §1 (or `scripts/download_data.py`), saving to `datasets/<expected file>`.
4. Run `qf600-data-sync` → profiles the file, updates `02`, sets status `downloaded`.
5. If `manual`, re-pack the team bundle (`qf600-bundle`).
