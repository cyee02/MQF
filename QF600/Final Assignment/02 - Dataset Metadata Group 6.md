# Dataset Metadata · Group 6

QF600 Asset Pricing · Group Project · Deliverable 02

Datasets used by `03 - execution_script_group_6.ipynb`. Script-downloaded files are rebuilt by notebook §1; manually obtained files are listed with their download link. The same information appears in Annex A of the Project Report.

<!-- AUTO:BEGIN data_sync -->

_Last synced: 2026-11-01T22:08:31 · 18 dataset(s)._

## Summary

| # | File | Description | Source | Frequency | Period | Rows | Columns |
|---|------|-------------|--------|-----------|--------|------|---------|
| 1 | `damodaran_annual.csv` | Annual returns: S&P 500, small cap, 3M T-bill, 10Y T-bond, Baa corporate, real estate, gold (parsed) | Aswath Damodaran (NYU Stern) | annual | 1928-01-01 → 2025-01-01 | 98 | 8 |
| 2 | `damodaran_histretSP.xls` | Damodaran raw workbook | Aswath Damodaran (NYU Stern) | annual | 1890-01-01 → 2025-01-01 | 143 | 7 |
| 3 | `etf_prices_daily.csv` | ETF adjusted closes: SPY, IEF, TLT, HYG, VNQ, PSP, GLD, RSP | Yahoo Finance via `yfinance` | daily | 2002-01-02 → 2026-10-30 | 6248 | 10 |
| 4 | `ff3_monthly.csv` | Fama-French 3 factors: Mkt-RF, SMB, HML, RF (% per month) | Ken French Data Library | monthly | 1926-07-01 → 2026-09-01 | 1203 | 5 |
| 5 | `ff_umd_monthly.csv` | Momentum factor UMD (% per month) | Ken French Data Library | monthly | 1927-01-01 → 2026-09-01 | 1197 | 2 |
| 6 | `fred_aaa_baa.csv` | Moody's seasoned Aaa and Baa corporate bond yields (%) | FRED | monthly | 1919-01-01 → 2026-09-01 | 1293 | 3 |
| 7 | `fred_cpi.csv` | CPI, all urban consumers, not seasonally adjusted | FRED | monthly | 1913-01-01 → 2026-09-01 | 1364 | 2 |
| 8 | `fred_deficit_gdp.csv` | Federal surplus or deficit (−), % of GDP, fiscal year | FRED | annual | 1929-01-01 → 2025-01-01 | 97 | 2 |
| 9 | `fred_dgs3mo.csv` | 3-month Treasury constant-maturity yield (annualised %) | FRED | daily | 1981-09-01 → 2026-10-29 | 11290 | 3 |
| 10 | `fred_gdp.csv` | Nominal GDP, $ billions | FRED | annual | 1929-01-01 → 2025-01-01 | 97 | 2 |
| 11 | `fred_gs10.csv` | 10-year Treasury constant-maturity yield (%) | FRED | monthly | 1953-04-01 → 2026-09-01 | 882 | 2 |
| 12 | `fred_interest_gdp.csv` | Federal interest outlays, % of GDP (for primary deficit) | FRED | annual | 1940-01-01 → 2025-01-01 | 86 | 2 |
| 13 | `fred_mts_deficit.csv` | Monthly Treasury statement surplus or deficit (−), $ millions | FRED | monthly | 1980-10-01 → 2026-09-01 | 552 | 2 |
| 14 | `fred_tb3ms.csv` | 3-month T-bill rate, secondary market (annualised %) | FRED | monthly | 1934-01-01 → 2026-09-01 | 1113 | 3 |
| 15 | `shiller_ie_data.xls` | Shiller raw workbook | Robert Shiller | monthly | 1871-01-01 → 2026-09-01 | 1878 | 20 |
| 16 | `shiller_monthly.csv` | S&P composite P, D, E, CPI, real EPS, CAPE (parsed from ie_data.xls) | Robert Shiller | monthly | 1871-01-01 → 2026-10-01 | 1870 | 10 |
| 17 | `wb_cmo_monthly.xlsx` | World Bank Pink Sheet raw workbook | World Bank Commodity Price Data (Pink Sheet) | Monthly | — → — | 808 | 17 |
| 18 | `wb_gold_monthly.csv` | Gold price, $/troy oz (parsed from the Pink Sheet) | World Bank Commodity Price Data (Pink Sheet) | monthly | 1960-01-01 → 2026-09-01 | 801 | 2 |

## 1. `damodaran_annual.csv`

- **Description:** Annual returns: S&P 500, small cap, 3M T-bill, 10Y T-bond, Baa corporate, real estate, gold (parsed)
- **Provider:** Aswath Damodaran (NYU Stern)
- **Source / link:** https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls (sheet "Returns by year")
- **How obtained:** script
- **File size:** 13 KB · sha256 `49805d1b909f`

**Shape:** 98 rows × 8 columns · annual · 1928-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Year | int64 | 0 |
| SP500 | float64 | 0 |
| SmallCap | float64 | 0 |
| TBill_3M | float64 | 0 |
| TBond_10Y | float64 | 0 |
| Baa_Corp | float64 | 0 |
| RealEstate | float64 | 0 |
| Gold | float64 | 0 |

## 2. `damodaran_histretSP.xls`

- **Description:** Damodaran raw workbook
- **Provider:** Aswath Damodaran (NYU Stern)
- **Source / link:** https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls
- **How obtained:** script
- **File size:** 528 KB · sha256 `28b8110916a1`

**Shape (sheet `Explanations and FAQ`):** 17 rows × 2 columns

| Column | Type | Missing |
|--------|------|---------|
| End Game | object | 0 |
| My objective in this spreadsheet is to compute the annual returns you would have earned on major financial asset classses, on an annual basis, inclusive of both cash payout during the year and the price appreciation. | object | 2 |

**Shape (sheet `Returns by year`):** 127 rows × 37 columns

| Column | Type | Missing |
|--------|------|---------|
| Date updated: | object | 3 |
| 2026-01-01 00:00:00 | object | 15 |
| Unnamed: 2 | object | 22 |
| Unnamed: 3 | object | 20 |
| Unnamed: 4 | object | 16 |
| Unnamed: 5 | object | 22 |
| Unnamed: 6 | object | 21 |
| Unnamed: 7 | object | 22 |
| Unnamed: 8 | object | 26 |
| Unnamed: 9 | object | 28 |
| Unnamed: 10 | object | 28 |
| Unnamed: 11 | object | 18 |
| Unnamed: 12 | object | 20 |
| Unnamed: 13 | object | 23 |
| Unnamed: 14 | object | 24 |
| Unnamed: 15 | object | 27 |
| Unnamed: 16 | object | 18 |
| Unnamed: 17 | object | 24 |
| Unnamed: 18 | object | 28 |
| Unnamed: 19 | object | 60 |
| Unnamed: 20 | object | 19 |
| Unnamed: 21 | object | 21 |
| Unnamed: 22 | object | 21 |
| Unnamed: 23 | object | 21 |
| Unnamed: 24 | object | 21 |
| Unnamed: 25 | object | 21 |
| Unnamed: 26 | object | 21 |
| Unnamed: 27 | object | 21 |
| Unnamed: 28 | object | 27 |
| Unnamed: 29 | object | 28 |
| Unnamed: 30 | object | 28 |
| Unnamed: 31 | object | 28 |
| Unnamed: 32 | object | 28 |
| Unnamed: 33 | object | 23 |
| Unnamed: 34 | object | 24 |
| Unnamed: 35 | object | 27 |
| Unnamed: 36 | object | 28 |

**Shape (sheet `S&P 500 & Raw Data`):** 100 rows × 11 columns · annual · 1927-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Unnamed: 0 | object | 0 |
| Unnamed: 1 | object | 0 |
| Unnamed: 2 | object | 0 |
| Unnamed: 3 | object | 0 |
| Unnamed: 4 | object | 0 |
| Unnamed: 5 | object | 1 |
| Unnamed: 6 | object | 0 |
| Unnamed: 7 | object | 1 |
| Unnamed: 8 | object | 0 |
| Unnamed: 9 | object | 1 |
| Unnamed: 10 | object | 1 |

**Shape (sheet `Small Cap`):** 98 rows × 4 columns · annual · 1928-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Year | int64 | 0 |
| Return | float64 | 0 |
| Unnamed: 2 | float64 | 0 |
| Unnamed: 3 | object | 97 |

**Shape (sheet `T. Bond yield & return`):** 103 rows × 3 columns · annual · 1927-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Bond used:  | object | 1 |
| US treasury 10-year bond at end of each year | object | 0 |
| Unnamed: 2 | object | 4 |

**Shape (sheet `T. Bill rates`):** 100 rows × 3 columns · annual · 1934-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| FRED Graph Observations | object | 0 |
| Unnamed: 1 | object | 5 |
| Unnamed: 2 | float64 | 8 |

**Shape (sheet `Inflation Rate`):** 120 rows × 3 columns · annual · 1914-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| FRED Graph Observations | object | 0 |
| Unnamed: 1 | object | 6 |
| Unnamed: 2 | float64 | 8 |

**Shape (sheet `Summary for ppt`):** 8 rows × 10 columns

| Column | Type | Missing |
|--------|------|---------|
| Nominal | object | 2 |
| Unnamed: 1 | object | 0 |
| Unnamed: 2 | object | 1 |
| Unnamed: 3 | object | 3 |
| Unnamed: 4 | object | 4 |
| Real | object | 2 |
| Unnamed: 7 | object | 0 |
| Unnamed: 8 | object | 1 |
| Unnamed: 9 | object | 3 |
| Unnamed: 10 | object | 4 |

**Shape (sheet `Home Prices (Raw Data)`):** 143 rows × 7 columns · annual · 1890-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Home Price data from Robert Shiller's website. | object | 6 |
| Unnamed: 1 | object | 6 |
| Unnamed: 2 | object | 7 |
| Unnamed: 3 | object | 142 |
| FRED Graph Observations | object | 98 |
| Unnamed: 6 | object | 104 |
| Unnamed: 7 | float64 | 106 |

**Shape (sheet `Moody's Rates`):** 115 rows × 8 columns · annual · 1919-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| FRED Graph Observations | object | 0 |
| Unnamed: 1 | object | 6 |
| Unnamed: 2 | object | 7 |
| FRED Graph Observations.1 | object | 0 |
| Unnamed: 9 | object | 46 |
| Unnamed: 10 | float64 | 8 |
| Unnamed: 12 | float64 | 75 |
| Unnamed: 14 | float64 | 75 |

**Shape (sheet `Home Prices`):** 100 rows × 4 columns · annual · 1927-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Unnamed: 0 | object | 0 |
| Unnamed: 1 | object | 0 |
| Unnamed: 3 | object | 98 |
| Unnamed: 4 | object | 98 |

**Shape (sheet `Gold Prices`):** 99 rows × 3 columns · annual · 1927-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Year | int64 | 0 |
| Price per oz | float64 | 0 |
| Source for pre-1970: https://nma.org/wp-content/uploads/2016/09/historic_gold_prices_1833_pres.pdf (average price for year) | object | 98 |

**Shape (sheet `Nominal vs Real Data`):** 98 rows × 15 columns · annual · 1928-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Year | int64 | 0 |
| S&P 500 (includes dividends) | float64 | 0 |
| 3-month T.Bill | float64 | 0 |
| US T. Bond (10-year) | float64 | 0 |
| Inflation Rate | float64 | 0 |
| S&P 500 (Real) | float64 | 0 |
| T. Bill (Real) | float64 | 0 |
| T.Bond (Real) | float64 | 0 |
| Year.1 | int64 | 0 |
| Nominal value of $100 invested in 1928 | float64 | 0 |
| Real value of $100 invested in 1928 | float64 | 0 |
| Unnamed: 14 | object | 88 |
| Stocks | float64 | 88 |
| T. Bills | float64 | 88 |
| T. Bonds | float64 | 88 |

**Shape (sheet `Sheet11`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Sheet12`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Sheet13`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Sheet14`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Sheet15`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Sheet16`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

## 3. `etf_prices_daily.csv`

- **Description:** ETF adjusted closes: SPY, IEF, TLT, HYG, VNQ, PSP, GLD, RSP
- **Provider:** Yahoo Finance via `yfinance`
- **Source / link:** tickers
- **How obtained:** script
- **File size:** 987 KB · sha256 `e132d3be35ac`

**Shape:** 6,248 rows × 10 columns · daily · 2002-01-02 → 2026-10-30

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| GLD | float64 | 726 |
| HYG | float64 | 1326 |
| IEF | float64 | 144 |
| PDP | float64 | 1298 |
| PSP | float64 | 1212 |
| RSP | float64 | 334 |
| SPY | float64 | 0 |
| TLT | float64 | 144 |
| VNQ | float64 | 690 |

## 4. `ff3_monthly.csv`

- **Description:** Fama-French 3 factors: Mkt-RF, SMB, HML, RF (% per month)
- **Provider:** Ken French Data Library
- **Source / link:** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_Factors_CSV.zip
- **How obtained:** script
- **File size:** 39 KB · sha256 `f5ea2fa174b3`

**Shape:** 1,203 rows × 5 columns · monthly · 1926-07-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| Mkt-RF | float64 | 0 |
| SMB | float64 | 0 |
| HML | float64 | 0 |
| RF | float64 | 0 |

## 5. `ff_umd_monthly.csv`

- **Description:** Momentum factor UMD (% per month)
- **Provider:** Ken French Data Library
- **Source / link:** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip
- **How obtained:** script
- **File size:** 19 KB · sha256 `124506fc2c44`

**Shape:** 1,197 rows × 2 columns · monthly · 1927-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| UMD | float64 | 0 |

## 6. `fred_aaa_baa.csv`

- **Description:** Moody's seasoned Aaa and Baa corporate bond yields (%)
- **Provider:** FRED
- **Source / link:** AAA, BAA
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 27 KB · sha256 `51540d981b9d`

**Shape:** 1,293 rows × 3 columns · monthly · 1919-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| AAA | float64 | 0 |
| BAA | float64 | 0 |

## 7. `fred_cpi.csv`

- **Description:** CPI, all urban consumers, not seasonally adjusted
- **Provider:** FRED
- **Source / link:** CPIAUCNS
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 23 KB · sha256 `a631d33d12bf`

**Shape:** 1,364 rows × 2 columns · monthly · 1913-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| CPI | float64 | 0 |

## 8. `fred_deficit_gdp.csv`

- **Description:** Federal surplus or deficit (−), % of GDP, fiscal year
- **Provider:** FRED
- **Source / link:** FYFSGDA188S
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 2 KB · sha256 `c9d346b932a1`

**Shape:** 97 rows × 2 columns · annual · 1929-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| surplus_pct_gdp | float64 | 0 |

## 9. `fred_dgs3mo.csv`

- **Description:** 3-month Treasury constant-maturity yield (annualised %)
- **Provider:** FRED
- **Source / link:** DGS3MO
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 296 KB · sha256 `62a30f6934fb`

**Shape:** 11,290 rows × 3 columns · daily · 1981-09-01 → 2026-10-29

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| DGS3MO_pct | float64 | 0 |
| DGS3MO | float64 | 0 |

## 10. `fred_gdp.csv`

- **Description:** Nominal GDP, $ billions
- **Provider:** FRED
- **Source / link:** GDPA
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 2 KB · sha256 `a805944a009b`

**Shape:** 97 rows × 2 columns · annual · 1929-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| gdp_busd | float64 | 0 |

## 11. `fred_gs10.csv`

- **Description:** 10-year Treasury constant-maturity yield (%)
- **Provider:** FRED
- **Source / link:** GS10
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 14 KB · sha256 `a216686276a7`

**Shape:** 882 rows × 2 columns · monthly · 1953-04-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| GS10 | float64 | 0 |

## 12. `fred_interest_gdp.csv`

- **Description:** Federal interest outlays, % of GDP (for primary deficit)
- **Provider:** FRED
- **Source / link:** FYOIGDA188S
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 2 KB · sha256 `96326fb727e4`

**Shape:** 86 rows × 2 columns · annual · 1940-01-01 → 2025-01-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| interest_pct_gdp | float64 | 0 |

## 13. `fred_mts_deficit.csv`

- **Description:** Monthly Treasury statement surplus or deficit (−), $ millions
- **Provider:** FRED
- **Source / link:** MTSDS133FMS
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 12 KB · sha256 `3c1a6f3be5bd`

**Shape:** 552 rows × 2 columns · monthly · 1980-10-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| surplus_musd | float64 | 0 |

## 14. `fred_tb3ms.csv`

- **Description:** 3-month T-bill rate, secondary market (annualised %)
- **Provider:** FRED
- **Source / link:** TB3MS
- **How obtained:** script (API key `fred_key` in `credentials.yaml`)
- **File size:** 29 KB · sha256 `83a4c4e94f1b`

**Shape:** 1,113 rows × 3 columns · monthly · 1934-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| TB3MS_pct | float64 | 0 |
| TB3MS | float64 | 0 |

## 15. `shiller_ie_data.xls`

- **Description:** Shiller raw workbook
- **Provider:** Robert Shiller
- **Source / link:** https://shillerdata.com/ → ie_data.xls
- **How obtained:** script
- **File size:** 1,675 KB · sha256 `98a54927942e`

**Shape (sheet `Disclaimer`):** 0 rows × 0 columns

| Column | Type | Missing |
|--------|------|---------|

**Shape (sheet `Data`):** 1,878 rows × 20 columns · monthly · 1871-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Unnamed: 0 | object | 5 |
| Unnamed: 1 | object | 4 |
| Unnamed: 2 | object | 10 |
| Unnamed: 3 | object | 10 |
| Unnamed: 4 | object | 3 |
| Unnamed: 5 | object | 6 |
| Unnamed: 6 | object | 4 |
| Unnamed: 7 | object | 6 |
| Unnamed: 8 | object | 10 |
| Unnamed: 9 | object | 4 |
| Unnamed: 10 | object | 10 |
| Unnamed: 11 | object | 8 |
| Unnamed: 12 | object | 121 |
| Unnamed: 14 | object | 121 |
| Unnamed: 16 | object | 125 |
| Unnamed: 17 | object | 5 |
| Unnamed: 18 | object | 4 |
| Unnamed: 19 | object | 125 |
| Unnamed: 20 | object | 125 |
| Unnamed: 21 | object | 125 |

## 16. `shiller_monthly.csv`

- **Description:** S&P composite P, D, E, CPI, real EPS, CAPE (parsed from ie_data.xls)
- **Provider:** Robert Shiller
- **Source / link:** https://shillerdata.com/ (link to ie_data.xls found on the page; the Yale copy stopped in 2023)
- **How obtained:** script
- **File size:** 227 KB · sha256 `19dbcd14cfa1`

**Shape:** 1,870 rows × 10 columns · monthly · 1871-01-01 → 2026-10-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| P | float64 | 0 |
| D | float64 | 4 |
| E | float64 | 4 |
| CPI | float64 | 0 |
| GS10 | float64 | 0 |
| real_P | float64 | 0 |
| real_D | float64 | 4 |
| real_E | float64 | 4 |
| CAPE | float64 | 120 |

## 17. `wb_cmo_monthly.xlsx`

- **Description:** World Bank Pink Sheet raw workbook
- **Provider:** World Bank Commodity Price Data (Pink Sheet)
- **Source / link:** as D20
- **How obtained:** script
- **File size:** 586 KB · sha256 `ea1c35082787`

**Shape (sheet `Mismatch Details`):** 154 rows × 7 columns

| Column | Type | Missing |
|--------|------|---------|
| MISMATCH DETAILS | object | 0 |
| Unnamed: 1 | object | 1 |
| Unnamed: 2 | object | 1 |
| Unnamed: 3 | object | 1 |
| Unnamed: 4 | object | 1 |
| Unnamed: 5 | object | 1 |
| Unnamed: 6 | object | 1 |

**Shape (sheet `Monthly Prices`):** 806 rows × 72 columns

| Column | Type | Missing |
|--------|------|---------|
| World Bank Commodity Price Data (The Pink Sheet) | object | 2 |
| Unnamed: 1 | object | 3 |
| Unnamed: 2 | object | 3 |
| Unnamed: 3 | object | 3 |
| Unnamed: 4 | object | 3 |
| Unnamed: 5 | object | 3 |
| Unnamed: 6 | object | 3 |
| Unnamed: 7 | object | 3 |
| Unnamed: 8 | object | 3 |
| Unnamed: 9 | object | 3 |
| Unnamed: 10 | object | 3 |
| Unnamed: 11 | object | 3 |
| Unnamed: 12 | object | 3 |
| Unnamed: 13 | object | 3 |
| Unnamed: 14 | object | 3 |
| Unnamed: 15 | object | 3 |
| Unnamed: 16 | object | 3 |
| Unnamed: 17 | object | 3 |
| Unnamed: 18 | object | 3 |
| Unnamed: 19 | object | 3 |
| Unnamed: 20 | object | 3 |
| Unnamed: 21 | object | 3 |
| Unnamed: 22 | object | 3 |
| Unnamed: 23 | object | 3 |
| Unnamed: 24 | object | 3 |
| Unnamed: 25 | object | 3 |
| Unnamed: 26 | object | 3 |
| Unnamed: 27 | object | 3 |
| Unnamed: 28 | object | 3 |
| Unnamed: 29 | object | 3 |
| Unnamed: 30 | object | 3 |
| Unnamed: 31 | object | 3 |
| Unnamed: 32 | object | 3 |
| Unnamed: 33 | object | 7 |
| Unnamed: 34 | object | 3 |
| Unnamed: 35 | object | 3 |
| Unnamed: 36 | object | 3 |
| Unnamed: 37 | object | 3 |
| Unnamed: 38 | object | 3 |
| Unnamed: 39 | object | 3 |
| Unnamed: 40 | object | 3 |
| Unnamed: 41 | object | 3 |
| Unnamed: 42 | object | 3 |
| Unnamed: 43 | object | 3 |
| Unnamed: 44 | object | 3 |
| Unnamed: 45 | object | 3 |
| Unnamed: 46 | object | 3 |
| Unnamed: 47 | object | 3 |
| Unnamed: 48 | object | 3 |
| Unnamed: 49 | object | 3 |
| Unnamed: 50 | object | 3 |
| Unnamed: 51 | object | 3 |
| Unnamed: 52 | object | 3 |
| Unnamed: 53 | object | 3 |
| Unnamed: 54 | object | 3 |
| Unnamed: 55 | object | 3 |
| Unnamed: 56 | object | 3 |
| Unnamed: 57 | object | 3 |
| Unnamed: 58 | object | 3 |
| Unnamed: 59 | object | 3 |
| … 12 more | | |

**Shape (sheet `Monthly Indices`):** 808 rows × 17 columns

| Column | Type | Missing |
|--------|------|---------|
| Unnamed: 0 | object | 4 |
| Unnamed: 1 | object | 6 |
| Unnamed: 2 | object | 6 |
| Unnamed: 3 | object | 5 |
| Unnamed: 4 | object | 5 |
| Unnamed: 5 | object | 6 |
| Unnamed: 6 | object | 5 |
| Unnamed: 7 | object | 6 |
| Unnamed: 8 | object | 6 |
| Unnamed: 9 | object | 6 |
| Unnamed: 10 | object | 5 |
| Unnamed: 11 | object | 6 |
| Unnamed: 12 | object | 6 |
| Unnamed: 13 | object | 5 |
| Unnamed: 14 | object | 6 |
| Unnamed: 15 | object | 6 |
| Unnamed: 16 | object | 5 |

**Shape (sheet `Description`):** 118 rows × 3 columns

| Column | Type | Missing |
|--------|------|---------|
| World Bank Commodity Price Data (The Pink Sheet) | object | 56 |
| Unnamed: 1 | object | 13 |
| Unnamed: 19 | object | 36 |

**Shape (sheet `Index Weights`):** 71 rows × 10 columns

| Column | Type | Missing |
|--------|------|---------|
| Weights Used in the World Bank Commodity Price Index (in Percent) 1/ | object | 58 |
| Unnamed: 1 | object | 68 |
| Unnamed: 2 | object | 59 |
| Unnamed: 3 | object | 63 |
| Unnamed: 4 | object | 49 |
| Unnamed: 5 | object | 51 |
| Unnamed: 8 | object | 17 |
| Unnamed: 11 | object | 20 |
| Unnamed: 14 | object | 51 |
| Unnamed: 18 | object | 70 |

## 18. `wb_gold_monthly.csv`

- **Description:** Gold price, $/troy oz (parsed from the Pink Sheet)
- **Provider:** World Bank Commodity Price Data (Pink Sheet)
- **Source / link:** https://www.worldbank.org/en/research/commodity-markets → CMO-Historical-Data-Monthly.xlsx, sheet "Monthly Prices"
- **How obtained:** script
- **File size:** 12 KB · sha256 `83682aa8b286`

**Shape:** 801 rows × 2 columns · monthly · 1960-01-01 → 2026-09-01

| Column | Type | Missing |
|--------|------|---------|
| Date | object | 0 |
| gold_usd_oz | int64 | 0 |

<!-- AUTO:END data_sync -->
