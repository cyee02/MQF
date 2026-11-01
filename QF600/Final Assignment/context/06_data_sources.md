# 06 · Data sources

Registry of every dataset the project uses. **`qf600-data-sync` keeps this file, `02 - Dataset Metadata Group 6.md` and `.sync/datasets.json` in step.** Add a row here *before* writing download code.

- **Status:** `planned` (not yet downloaded) · `downloaded` (file in `datasets/`) · `pending-user` (user to supply) · `dropped`.
- **Method:** `script` (notebook §1 or `scripts/download_data.py`) · `manual` (download by hand, share via `qf600-bundle`).
- **Key:** name of the `credentials.yaml` entry, if an API key is needed.
- Filenames are what the file must be called in `datasets/`.
- **Series IDs and URLs marked ⚠ must be checked on first download** (sites move files).

## Core datasets

All script datasets are downloaded by notebook §1 (`03 - execution_script_group_6.ipynb`). Series IDs and URLs were verified on 01 Nov 2026.

| ID | Dataset | Provider | Series / URL | Freq | Period needed | Method | Key | Expected file | Status |
|----|---------|----------|--------------|------|---------------|--------|-----|---------------|--------|
| D01 | 3-month T-bill rate, secondary market (annualised %) | FRED | `TB3MS` | Monthly | 1934-01 → latest | script | `fred_key` | `fred_tb3ms.csv` | downloaded |
| D02 | Fama-French 3 factors: Mkt-RF, SMB, HML, RF (% per month) | Ken French Data Library | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip` | Monthly | 1926-07 → latest | script | — | `ff3_monthly.csv` | downloaded |
| D03 | Momentum factor UMD (% per month) | Ken French Data Library | `https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip` | Monthly | 1927-01 → latest | script | — | `ff_umd_monthly.csv` | downloaded |
| D04 | 10-year Treasury constant-maturity yield (%) | FRED | `GS10` | Monthly | 1953-04 → latest | script | `fred_key` | `fred_gs10.csv` | downloaded |
| D05 | Moody's seasoned Aaa and Baa corporate bond yields (%) | FRED | `AAA`, `BAA` | Monthly | 1919-01 → latest | script | `fred_key` | `fred_aaa_baa.csv` | downloaded |
| D06 | Federal surplus or deficit (−), % of GDP, fiscal year | FRED | `FYFSGDA188S` | Annual | 1929 → latest | script | `fred_key` | `fred_deficit_gdp.csv` | downloaded |
| D07 | Federal interest outlays, % of GDP (for primary deficit) | FRED | `FYOIGDA188S` | Annual | 1940 → latest | script | `fred_key` | `fred_interest_gdp.csv` | downloaded |
| D08 | Monthly Treasury statement surplus or deficit (−), $ millions | FRED | `MTSDS133FMS` | Monthly | 1980-10 → latest | script | `fred_key` | `fred_mts_deficit.csv` | downloaded |
| D09 | CPI, all urban consumers, not seasonally adjusted | FRED | `CPIAUCNS` | Monthly | 1913 → latest | script | `fred_key` | `fred_cpi.csv` | downloaded |
| D10 | S&P composite P, D, E, CPI, real EPS, CAPE (parsed from ie_data.xls) | Robert Shiller | `https://shillerdata.com/` (link to ie_data.xls found on the page; the Yale copy stopped in 2023) | Monthly | 1871 → latest | script | — | `shiller_monthly.csv` | downloaded |
| D11 | Shiller raw workbook | Robert Shiller | `https://shillerdata.com/` → `ie_data.xls` | Monthly | 1871 → latest | script | — | `shiller_ie_data.xls` | downloaded |
| D12 | Annual returns: S&P 500, small cap, 3M T-bill, 10Y T-bond, Baa corporate, real estate, gold (parsed) | Aswath Damodaran (NYU Stern) | `https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls` (sheet "Returns by year") | Annual | 1928 → 2025 | script | — | `damodaran_annual.csv` | downloaded |
| D13 | Damodaran raw workbook | Aswath Damodaran (NYU Stern) | `https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls` | Annual | 1928 → 2025 | script | — | `damodaran_histretSP.xls` | downloaded |
| D14 | ETF adjusted closes: SPY, IEF, TLT, HYG, VNQ, PSP, GLD, RSP, PDP (momentum, from 2007-03) | Yahoo Finance via `yfinance` | tickers | Daily | 2002-01 → latest (HYG from 2007-04) | script | — | `etf_prices_daily.csv` | downloaded |
| D15 | 3-month Treasury constant-maturity yield (annualised %) | FRED | `DGS3MO` | Daily | 1981-09 → latest | script | `fred_key` | `fred_dgs3mo.csv` | downloaded |
| D16 | Nominal GDP, $ billions | FRED | `GDPA` | Annual | 1929 → latest | script | `fred_key` | `fred_gdp.csv` | downloaded |
| D19 | Global Financial Data (Finaeon) | GFD | API (paid licence) | — | — | — | — | — | **dropped**: SMU has no Finaeon subscription; trial covers US stocks from 2019 only |
| D20 | Gold price, $/troy oz (parsed from the Pink Sheet) | World Bank Commodity Price Data (Pink Sheet) | `https://www.worldbank.org/en/research/commodity-markets` → `CMO-Historical-Data-Monthly.xlsx`, sheet "Monthly Prices" | Monthly | 1960-01 → latest | script | — | `wb_gold_monthly.csv` | downloaded |
| D21 | World Bank Pink Sheet raw workbook | World Bank Commodity Price Data (Pink Sheet) | as D20 | Monthly | 1960-01 → latest | script | — | `wb_cmo_monthly.xlsx` | downloaded |

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
