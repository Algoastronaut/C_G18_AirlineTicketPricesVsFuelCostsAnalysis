# ✈️ C\_G18 — Airline Ticket Prices vs Fuel Costs Analysis

> **Course:** Data & Visual Analytics (DVA) — Capstone Project
> **Team:** Group 18
> **Academic Year:** 2025–2026

---

## 🧩 Problem Statement

Jet fuel is the single largest operating expense for commercial airlines, routinely accounting for **20–30% of total operating costs**. When global crude oil prices spike — often triggered by geopolitical conflicts, OPEC supply decisions, or macroeconomic shocks — airlines must decide whether to absorb these costs, pass them on to passengers via higher base fares or fuel surcharges, or hedge against future price movements.

This project investigates the **quantitative relationship between jet fuel price movements and airline ticket pricing behaviour** across multiple carriers, routes, and global conflict phases. By integrating commodity price data, airline financial reports, route-level cost structures, and passenger fare histories, the analysis seeks to determine:

- How quickly and to what degree fuel cost increases are passed on to consumers.
- Whether fuel surcharges are applied systematically or opportunistically.
- Which routes and carriers are most sensitive to fuel price volatility.
- How geopolitical disruptions amplify or dampen these price transmission effects.

---

## 🎯 Objectives

| # | Objective |
|---|-----------|
| 1 | Quantify the **price pass-through rate** from jet fuel costs to average ticket prices over time. |
| 2 | Analyse the **structure and timing of fuel surcharges** relative to underlying oil price movements. |
| 3 | Identify which **airlines, regions, and route types** exhibit the highest sensitivity to fuel price shocks. |
| 4 | Examine the **financial impact** on airline profitability margins during high fuel-cost periods. |
| 5 | Assess the role of **geopolitical conflict phases** as a moderating variable in fuel-price–ticket-price dynamics. |
| 6 | Deliver an **interactive Tableau dashboard** that allows stakeholders to explore these relationships visually. |

---

## 📁 Dataset Description

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

## 🔄 ETL Pipeline

The ETL pipeline transforms raw multi-source data into clean, analysis-ready paired datasets. It is implemented across the Jupyter notebooks (01–05) and consolidated in `scripts/etl_pipeline.py`.

### 🔵 Extraction

**Sources:**
- **Jet fuel & crude oil prices** — U.S. Energy Information Administration (EIA) and IATA Fuel Monitor monthly reports.
- **Airline ticket prices** — U.S. DOT DB1B and equivalent European CAA datasets, supplemented with aggregated fare data by route.
- **Fuel surcharges** — individual airline tariff filings, IATA industry bulletins, and publicly disclosed surcharge schedules.
- **Airline financial data** — ICAO financial data publications and airline investor relations reports (10-K, 20-F).
- **Route cost data** — ICAO cost-per-ASK (Available Seat Kilometre) statistics and route-level operational data.
- **Conflict/geopolitical events** — ACLED (Armed Conflict Location & Event Data Project) and Reuters historical archives.

All datasets are stored in `data/raw/` as flat CSVs. A `month` field (`YYYY-MM`) and `conflict_phase` label are the primary join keys across datasets.

### 🟡 Transformation

| Step | Description |
|------|-------------|
| Distance band engineering | `avg_route_km` binned into `km_range` (≤1500 / 1501–4500 / 4501–9000 / >9000 km) |
| Event date normalisation | `event_date` (`YYYY-MM-DD`) truncated to `YYYY-MM` via `str[:7]` |
| Duplicate column removal | `df.loc[:, ~df.columns.duplicated()]` applied post-merge |
| Missing value handling | Forward-fill (quarterly→monthly), median imputation (numeric), mode imputation (categorical), row drop (core fields null) |
| Outlier treatment | IQR detection → Winsorise at 1st/99th percentile → flag with `is_outlier` |
| Type conversion | `month` → `datetime64[ns]`; monetary fields → `float64`; flags → `bool` |
| Feature engineering | `year`, `month_num`, `price_change_pct`, `real_ticket_price_usd`, `fuel_price_lag_1m/2m`, `surcharge_coverage_ratio` |

### 🟢 Loading

- Processed datasets written to `data/processed/` as clean CSVs.
- Tableau dashboard consumes all three processed CSVs directly.
- No database backend — all storage is flat-file CSV for reproducibility.
