# C\_G18 — Airline Ticket Prices vs Fuel Costs Analysis

> **Course:** Data & Visual Analytics (DVA) — Capstone Project
> **Team:** Group 18
> **Academic Year:** 2025–2026

---

## Problem Statement

Jet fuel is the single largest operating expense for commercial airlines, routinely accounting for **20–30% of total operating costs**. When global crude oil prices spike — often triggered by geopolitical conflicts, OPEC supply decisions, or macroeconomic shocks — airlines must decide whether to absorb these costs, pass them on to passengers via higher base fares or fuel surcharges, or hedge against future price movements.

This project investigates the **quantitative relationship between jet fuel price movements and airline ticket pricing behaviour** across multiple carriers, routes, and global conflict phases. By integrating commodity price data, airline financial reports, route-level cost structures, and passenger fare histories, the analysis seeks to determine:

- How quickly and to what degree fuel cost increases are passed on to consumers.
- Whether fuel surcharges are applied systematically or opportunistically.
- Which routes and carriers are most sensitive to fuel price volatility.
- How geopolitical disruptions amplify or dampen these price transmission effects.

** Key Insight**

Airline ticket pricing is influenced by fuel costs, but primarily driven by demand, route characteristics, and geopolitical disruptions rather than direct cost pass-through.

---

## Objectives

| # | Objective |
|---|-----------|
| 1 | Quantify the **price pass-through rate** from jet fuel costs to average ticket prices over time. |
| 2 | Analyse the **structure and timing of fuel surcharges** relative to underlying oil price movements. |
| 3 | Identify which **airlines, regions, and route types** exhibit the highest sensitivity to fuel price shocks. |
| 4 | Examine the **financial impact** on airline profitability margins during high fuel-cost periods. |
| 5 | Assess the role of **geopolitical conflict phases** as a moderating variable in fuel-price–ticket-price dynamics. |
| 6 | Deliver an **interactive Tableau dashboard** that allows stakeholders to explore these relationships visually. |

---

## Project Structure

```text
├── README.md
├── requirements.txt
├── data/
│   ├── raw/                 # Raw unprocessed datasets
│   └── processed/           # Final merged datasets for Tableau
├── docs/
│   └── data_dictionary.md   # Data dictionaries for datasets
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── reports/                 # Presentation and report PDFs
├── scripts/
│   └── etl_pipeline.py      # Consolidated ETL scripts
└── tableau/                 # Tableau workbooks and dashboards
```

---

## Dataset Description

### Raw Datasets (`data/raw/`)

The project uses **six raw CSV datasets**, assembled from publicly available airline industry databases, commodity price repositories, and geopolitical event archives.

| File | Size | Est. Rows | Est. Columns | Description |
|------|------|-----------|--------------|-------------|
| `airline_ticket_prices.csv` | ~2.1 MB | ~18,000 | 14 | Monthly average base fares by airline, route, region, and travel class |
| `fuel_surcharges.csv` | ~1.3 MB | ~12,000 | 13 | Fuel surcharge amounts per route segment and distance band, by carrier |
| `oil_jet_fuel_prices.csv` | ~8.6 KB | ~180 | 8 | Monthly Brent crude and jet kerosene spot prices (USD/barrel & USD/gallon) |
| `airline_financial_impact.csv` | ~110 KB | ~900 | 12 | Quarterly airline-level revenue, COGS, fuel cost share, and EBITDA margin |
| `route_cost_impact.csv` | ~504 KB | ~7,500 | 11 | Route-level operational cost breakdowns including fuel cost per ASK |
| `conflict_oil_events.csv` | ~7.4 KB | ~150 | 9 | Timeline of geopolitical events tagged with conflict phase and oil impact level |

### Processed Datasets (`data/processed/`)

After the ETL pipeline runs, the six raw files are merged into **three logically paired processed datasets**:

| File | Est. Rows | Est. Columns | Merge Logic |
|------|-----------|--------------|-------------|
| `1_macro_oil_and_events.csv` | ~200 | ~15 | `oil_jet_fuel_prices` ⟕ `conflict_oil_events` on `month` + `conflict_phase` |
| `2_route_impacts_and_financials.csv` | ~7,500 | ~20 | `route_cost_impact` ⟕ `airline_financial_impact` on `month` + `conflict_phase` + `airline` |
| `3_ticket_prices_and_surcharges.csv` | ~18,000 | ~25 | `airline_ticket_prices` ⟕ `fuel_surcharges` on `month` + `conflict_phase` + `airline` + `iata_code` + `country` + `region` + `km_range` |

---

## ETL Pipeline

The ETL pipeline transforms raw multi-source data into clean, analysis-ready paired datasets. It is implemented across the Jupyter notebooks (01–05) and consolidated in `scripts/etl_pipeline.py`.

### Extraction

**Sources:**
- **Jet fuel & crude oil prices** — U.S. Energy Information Administration (EIA) and IATA Fuel Monitor monthly reports.
- **Airline ticket prices** — U.S. DOT DB1B and equivalent European CAA datasets, supplemented with aggregated fare data by route.
- **Fuel surcharges** — individual airline tariff filings, IATA industry bulletins, and publicly disclosed surcharge schedules.
- **Airline financial data** — ICAO financial data publications and airline investor relations reports (10-K, 20-F).
- **Route cost data** — ICAO cost-per-ASK (Available Seat Kilometre) statistics and route-level operational data.
- **Conflict/geopolitical events** — ACLED (Armed Conflict Location & Event Data Project) and Reuters historical archives.

All datasets are stored in `data/raw/` as flat CSVs. A `month` field (`YYYY-MM`) and `conflict_phase` label are the primary join keys across datasets.

### Transformation

| Step | Description |
|------|-------------|
| Distance band engineering | `avg_route_km` binned into `km_range` (≤1500 / 1501–4500 / 4501–9000 / >9000 km) |
| Event date normalisation | `event_date` (`YYYY-MM-DD`) truncated to `YYYY-MM` via `str[:7]` |
| Duplicate column removal | `df.loc[:, ~df.columns.duplicated()]` applied post-merge |
| Missing value handling | Forward-fill (quarterly→monthly), median imputation (numeric), mode imputation (categorical), row drop (core fields null) |
| Outlier treatment | IQR detection → Winsorise at 1st/99th percentile → flag with `is_outlier` |
| Type conversion | `month` → `datetime64[ns]`; monetary fields → `float64`; flags → `bool` |
| Feature engineering | `year`, `month_num`, `price_change_pct`, `real_ticket_price_usd`, `fuel_price_lag_1m/2m`, `surcharge_coverage_ratio` |

### Loading

- Processed datasets written to `data/processed/` as clean CSVs.
- Tableau dashboard consumes all three processed CSVs directly.
- No database backend — all storage is flat-file CSV for reproducibility.

---

## Notebook-Wise Explanation

| Notebook | Purpose |
|----------|---------|
| `01_extraction.ipynb` | Loads all six raw CSVs, validates schemas, checks column names/dtypes, and prints shape/null summaries. Acts as a data audit and ingestion checkpoint. |
| `02_cleaning.ipynb` | Handles missing values, removes duplicates, standardises column names (snake_case), corrects data types, and applies outlier detection + Winsorisation. |
| `03_eda.ipynb` | Performs Exploratory Data Analysis on the three processed pairs. Includes distribution plots, correlation heatmaps, time-series trend charts, and carrier/region breakdowns. |
| `04_statistical_analysis.ipynb` | Applies formal statistical tests: Pearson/Spearman correlation, OLS regression (price pass-through coefficient), Granger causality tests, and ANOVA for cross-airline surcharge differences. |
| `05_final_load_prep.ipynb` | Final data preparation for Tableau ingestion. Applies remaining transformations, exports clean CSVs, and validates output schemas. |
| `merge_datasets.ipynb` | Executes all three LEFT JOIN merge operations to produce the three processed datasets from the six raw inputs. Core data integration step. |

---

## Workflow

```
RAW DATA SOURCES  (EIA / IATA / DOT DB1B / ICAO / ACLED)
        │
        ▼
01_extraction.ipynb     → Load CSVs, validate schemas, null/dtype audit
        │
        ▼
02_cleaning.ipynb       → Impute nulls, remove duplicates, standardise dtypes, treat outliers
        │
        ▼
merge_datasets.ipynb    → Pair 1: Oil + Events
                          Pair 2: Routes + Financials
                          Pair 3: Tickets + Surcharges  →  data/processed/
        │
        ▼
03_eda.ipynb            → Distributions, correlations, time-series trends, carrier analysis
        │
        ▼
04_statistical_analysis.ipynb  → Correlation, OLS Regression, Granger Causality, ANOVA
        │
        ▼
05_final_load_prep.ipynb  → Final transforms, export clean CSVs, Tableau-ready
        │
        ▼
Tableau Dashboard       → Interactive visualisations, stakeholder-facing insights
```

---

## Tech Stack

| Layer | Tool / Library | Purpose |
|-------|---------------|---------|
| **Language** | Python 3.12 | Core analysis language |
| **Data Manipulation** | `pandas` | DataFrame operations, merges, transformations |
| **Numerical Computing** | `numpy` | Array operations, statistical calculations |
| **Visualisation** | `matplotlib`, `seaborn` | EDA plots, correlation heatmaps |
| **Statistical Analysis** | `scipy`, `statsmodels` | Correlation tests, OLS regression, Granger causality |
| **Notebooks** | JupyterLab / Jupyter Notebook | Interactive analysis environment |
| **BI Dashboard** | Tableau Public / Tableau Desktop | Interactive stakeholder dashboards |
| **Version Control** | Git + GitHub | Source control and collaboration |
| **Environment** | `venv` / `conda` | Python environment isolation |

---

## Tableau Dashboard

Explore the interactive visualizations here:
🔗 **[View Tableau Public Dashboard](https://public.tableau.com/app/profile/YOUR_PROFILE_LINK)** 

The dashboard provides visual exploration of ticket prices, fuel cost impact, and geopolitical events over time.

---

## Key Insights

1. **Impact of Fuel Prices on Fares:** There is a clear positive relationship between fuel prices and ticket prices. When jet fuel and crude oil prices increase, ticket fares also increase. However, the increase is not always immediate, indicating a slight lag effect in price adjustment. OLS regression shows that for every 1 unit increase in fuel price, ticket price increases by ~14.5 units. However, the model explains very little variation (R² ≈ 0.08), so fuel price alone is not a strong predictor.
2. **Airline Type Performance:** Flag carriers have slightly higher average fares compared to low-cost airlines. Load factor remains almost the same for both airline types (around 70%). Fuel cost impact (OpEx %) is also very similar, showing that both types are equally affected by fuel price changes.
3. **Fare Distribution Insights:** Most ticket prices are concentrated within a moderate range. During conflict periods and high fuel price phases, extreme fare values increase. This indicates higher price volatility during unstable conditions.
4. **Overall Pricing Dynamics:** Fuel prices have a significant impact on airline operating costs but only a limited direct impact on ticket prices. Airlines partially pass increased fuel costs to customers through surcharges, but do not fully pass fuel cost increases to customers. Ticket pricing is heavily influenced by a combination of demand fluctuations, market conditions, and external events (such as pandemics and geopolitical conflicts).

---

## Business Recommendations

1. **Dynamic Pricing Integration:** Airlines should continue to refine dynamic pricing models that weight route demand, geopolitical risk, and competitor behavior heavily, rather than relying strictly on static fuel cost pass-throughs.
2. **Proactive Fuel Hedging:** Given the lack of a full ticket price pass-through, robust fuel hedging strategies remain critical during periods of high geopolitical volatility to protect operating margins.
3. **Surcharge Communication:** Since surcharges don't fully cover fuel cost spikes, airlines should communicate these fees transparently to consumers while optimizing them based on route distance and competitive landscape.
4. **Agile Route Management:** Monitor geopolitical conflict phases and quickly reallocate capacity from highly fuel-sensitive or disruption-prone routes to more stable regions to minimize margin erosion.

---

## Challenges

| Challenge | Description | Mitigation |
|-----------|-------------|------------|
| **Multi-source schema mismatches** | Six raw datasets built independently with inconsistent column naming and date formats | Standardised all column names to `snake_case`; normalised all dates to `YYYY-MM` |
| **Granularity mismatch** | Oil price data is monthly; financial data is quarterly | Forward-fill to propagate quarterly values across monthly intervals |
| **Sparse surcharge records** | ~18% of airline–route–month combos lack a matching surcharge | Median imputation by `airline` + `km_range` subgroup |
| **Geopolitical event alignment** | Conflict events don't align neatly to calendar months | Events tagged to month of onset; multi-month conflicts propagate `conflict_phase` forward |
| **Outlier vs. legitimate extremes** | COVID-19 and 2022 oil spike are statistical outliers but economically meaningful | Retained with `is_outlier = True` flag; sensitivity analyses run with and without these periods |
| **Join key complexity (Pair 3)** | Pair 3 merge requires 7 join keys — sensitive to encoding inconsistencies | Applied `.str.strip().str.lower()` normalisation to all string-type join keys before merging |

---

## Future Improvements

- **Real-time pipeline:** Integrate live EIA and IATA API feeds using Apache Airflow for monthly auto-updates.
- **ML forecasting:** Build a time-series model (Prophet, SARIMA, or LSTM) to predict 3–6 month forward ticket prices.
- **Hedging effectiveness analysis:** Extend financial dataset to include airline-specific hedging ratios.
- **Consumer welfare analysis:** Incorporate RPK data to quantify total consumer welfare impact of fuel-driven fare increases.
- **NLP event processing:** Replace manual conflict tagging with an LLM-based news classification pipeline.
- **Expanded carrier coverage:** Extend analysis to include low-cost and ultra-low-cost carriers (LCCs / ULCCs).

---

## How to Run

### Prerequisites
- Python 3.12+
- JupyterLab or Jupyter Notebook
- Tableau Desktop or Tableau Public

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/connectwithvanshika/C_G18_AirlineTicketPricesVsFuelCostsAnalysis.git
cd C_G18_AirlineTicketPricesVsFuelCostsAnalysis

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch JupyterLab
jupyter lab
```

Run notebooks in this order from the `notebooks/` directory:

```
01_extraction.ipynb  →  02_cleaning.ipynb  →  merge_datasets.ipynb
→  03_eda.ipynb  →  04_statistical_analysis.ipynb  →  05_final_load_prep.ipynb
```

Connect Tableau to processed CSVs in `data/processed/` for the dashboard.

---

## Team

**Group 18 — DVA Capstone**

| Role | Team Member Name | GitHub Username |
|---|---|---|
| Project Lead | Vanshika Yadav | connectwithvanshika |
| Data Lead | shrijan sanidhya | ShrijanSanidhya |
| ETL Lead | Killi Akshith Kumar | Akshith17323 |
| Analysis Lead | Saumya Soni | Algoastronaut |
| Visualization Lead | Syed Darain Qamar | darain24 |
| Strategy Lead | B Mohith venkata sai krishna | mohith0705 |
| PPT & Quality Lead | Vanshika Yadav | connectwithvanshika |

## Contribution Status

 Team Member                  | Data | ETL | Analysis | Visualization | Strategy | PPT & Quality |
 ---------------------------- | ---- | --- | -------- | ------------- | -------- | ------------- |
 Vanshika Yadav               |  -   | - | ✔️       | -            | -        | ✔️                |
 Shrijan Sanidhya             | ✔️   |  -   |  -       |  -           | ✔️       |  -             |
 Killi Akshith Kumar          | ✔️   | ✔️  |  -        |  -             |  -        |  -          |
 Saumya Soni                  |  -    |  -   | ✔️       |  -             |  -        | ✔️         |
 Syed Darain Qamar            | ✔️    |  -   |  -        | ✔️            |  -        |  -         |
 B Mohith Venkata Sai Krishna |  -   |   ✔️  |  -        |  -            | ✔️       |  -          |  


> *For academic use only. All data used is publicly available or constructed for educational purposes.*
