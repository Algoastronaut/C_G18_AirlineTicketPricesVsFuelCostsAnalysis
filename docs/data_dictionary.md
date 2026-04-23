# 📖 Data Dictionary — Airline Ticket Prices vs Fuel Costs Analysis

> **Project:** C\_G18 — Airline Ticket Prices vs Fuel Costs Analysis  
> **Course:** Data & Visual Analytics (DVA) Capstone  
> **Last Updated:** April 2026

---

## Part A — Raw Data Overview

### A1. Dataset Inventory

The project ingests **six raw CSV files**, each representing a distinct data domain. Together they form a multi-dimensional view of fuel economics, airline pricing, route operations, financial health, and geopolitical context.

| # | File | Size | Est. Rows | Est. Columns | Domain |
|---|------|------|-----------|--------------|--------|
| 1 | `airline_ticket_prices.csv` | ~2.1 MB | ~18,000 | 14 | Passenger fare |
| 2 | `fuel_surcharges.csv` | ~1.3 MB | ~12,000 | 13 | Surcharge policy |
| 3 | `oil_jet_fuel_prices.csv` | ~8.6 KB | ~180 | 8 | Commodity prices |
| 4 | `airline_financial_impact.csv` | ~110 KB | ~900 | 12 | Airline financials |
| 5 | `route_cost_impact.csv` | ~504 KB | ~7,500 | 11 | Route economics |
| 6 | `conflict_oil_events.csv` | ~7.4 KB | ~150 | 9 | Geopolitical events |

---

### A2. Source & Collection Method

| File | Assumed Source | Collection Method |
|------|---------------|-------------------|
| `airline_ticket_prices.csv` | U.S. DOT DB1B database; European CAA fare filings | Quarterly public disclosure; web aggregation |
| `fuel_surcharges.csv` | IATA fuel surcharge bulletins; airline tariff filings | Manual compilation from airline websites and IATA publications |
| `oil_jet_fuel_prices.csv` | U.S. Energy Information Administration (EIA); IATA Jet Fuel Monitor | Monthly automated data download |
| `airline_financial_impact.csv` | Airline annual reports (10-K / 20-F); ICAO financial statistics | Structured extraction from PDF/HTML financial filings |
| `route_cost_impact.csv` | ICAO cost-per-ASK statistics; airline operational disclosures | Aggregated from ICAO Economics report series |
| `conflict_oil_events.csv` | ACLED; OPEC press releases; Reuters historical news | Manual tagging and curation of geopolitical event timelines |

---

### A3. Data Types & Structure

| File | Primary Structure | Temporal Granularity | Key Identifiers |
|------|------------------|---------------------|-----------------|
| `airline_ticket_prices.csv` | Panel (airline × route × month) | Monthly | `airline`, `iata_code`, `route`, `month` |
| `fuel_surcharges.csv` | Panel (airline × km_range × month) | Monthly | `airline`, `km_range`, `month`, `conflict_phase` |
| `oil_jet_fuel_prices.csv` | Time-series | Monthly | `month` |
| `airline_financial_impact.csv` | Panel (airline × quarter) | Quarterly | `airline`, `month`, `conflict_phase` |
| `route_cost_impact.csv` | Panel (airline × route × month) | Monthly | `airline`, `route`, `month`, `conflict_phase` |
| `conflict_oil_events.csv` | Event log | Daily (normalised to Monthly) | `event_id`, `event_date`, `conflict_phase` |

---

### A4. Known Raw Data Limitations

| Limitation | Affected File(s) | Impact |
|------------|-----------------|--------|
| **Missing surcharge records** | `fuel_surcharges.csv` | ~18% of airline–route–month combos lack a matching surcharge entry |
| **Quarterly vs. monthly mismatch** | `airline_financial_impact.csv` | Financial metrics must be forward-filled across 3 monthly rows |
| **Inconsistent date formats** | `conflict_oil_events.csv` | `event_date` stored as full ISO date (`YYYY-MM-DD`) vs. `YYYY-MM` elsewhere |
| **Sparse oil price history** | `oil_jet_fuel_prices.csv` | Only ~180 monthly rows; earliest records may have proxy/interpolated values |
| **Route naming inconsistencies** | `airline_ticket_prices.csv`, `route_cost_impact.csv` | Same route expressed as `JFK-LHR` and `LHR-JFK` depending on source |
| **Self-reported financials** | `airline_financial_impact.csv` | Figures are airline-disclosed and may reflect accounting treatments |
| **Survivorship bias** | All files | Only airlines with continuous reporting are represented; bankrupt carriers excluded |

---

---

## Part B — Column-Level Data Dictionary

> **Stage Legend:**
> - `RAW` — column exists in the raw source file, used as-is
> - `CLEANED` — column exists in raw but was standardised, imputed, or type-corrected
> - `FEATURE-ENGINEERED` — column was derived or created during transformation

---

### B1. `airline_ticket_prices.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `month` | string → datetime | Year-month of the ticket price observation | `2022-03` | CLEANED | Cast to `datetime64[ns]`; used as primary temporal join key |
| `airline` | string | Full name of the airline carrier | `Delta Air Lines` | CLEANED | Stripped whitespace; lowercased for join key matching |
| `iata_code` | string | 2-letter IATA airline code | `DL` | CLEANED | Uppercased; validated against IATA registry |
| `country` | string | Country of airline registration | `United States` | CLEANED | Stripped and lowercased for join consistency |
| `region` | string | Geographic region of the airline | `North America` | CLEANED | Standardised to 6 predefined region labels |
| `route` | string | Origin–destination airport pair | `JFK-LHR` | CLEANED | Normalised to alphabetical order (`A-B` format) to resolve bidirectional duplicates |
| `avg_route_km` | float64 | Average great-circle distance of the route in kilometres | `5,540.0` | CLEANED | Nulls filled with route-median; used to derive `km_range` |
| `travel_class` | string | Cabin class of the fare | `Economy` | CLEANED | Standardised to `Economy`, `Business`, `First` |
| `conflict_phase` | string | Geopolitical conflict phase label active during the month | `Active Conflict` | CLEANED | Mode-imputed for sparse records |
| `avg_ticket_price_usd` | float64 | Average base fare (excluding taxes and surcharges) in USD | `487.50` | CLEANED | Rows null on this field dropped if also missing fuel data; Winsorised at 1st/99th percentile |
| `ticket_count` | int64 | Number of tickets sampled for the monthly average | `3,200` | CLEANED | Nulls filled with route-month median |
| `taxes_fees_usd` | float64 | Average government taxes and airport fees per ticket in USD | `78.40` | CLEANED | Median-imputed by country |
| `total_fare_usd` | float64 | Total fare including taxes and fees (`avg_ticket_price_usd + taxes_fees_usd`) | `565.90` | CLEANED | Recalculated post-imputation to ensure consistency |
| `km_range` | string | Distance band derived from `avg_route_km` | `4501–9000 km` | FEATURE-ENGINEERED | Binned using `map_km()` function; required for Pair 3 merge join key |
| `year` | int64 | Calendar year extracted from `month` | `2022` | FEATURE-ENGINEERED | Derived via `pd.DatetimeIndex.year` |
| `month_num` | int64 | Calendar month number (1–12) extracted from `month` | `3` | FEATURE-ENGINEERED | Derived for seasonality modelling |
| `price_change_pct` | float64 | Month-over-month % change in `avg_ticket_price_usd` | `+4.2` | FEATURE-ENGINEERED | Computed as `(current - prev) / prev * 100`; first row per route is NaN |
| `real_ticket_price_usd` | float64 | Inflation-adjusted ticket price using CPI (base year 2019) | `431.20` | FEATURE-ENGINEERED | Deflated using monthly CPI index joined from external source |
| `is_outlier` | bool | Flag indicating the row was identified as a statistical outlier | `False` | FEATURE-ENGINEERED | Set using IQR method on `avg_ticket_price_usd`; True rows retained but flagged |

---

### B2. `fuel_surcharges.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `month` | string → datetime | Year-month of the surcharge schedule | `2022-03` | CLEANED | Cast to `datetime64[ns]` |
| `airline` | string | Airline carrier applying the surcharge | `British Airways` | CLEANED | Lowercased and stripped for join key |
| `iata_code` | string | 2-letter IATA code | `BA` | CLEANED | Uppercased |
| `country` | string | Country of the airline | `United Kingdom` | CLEANED | Standardised casing |
| `region` | string | Geographic region | `Europe` | CLEANED | Standardised to 6 predefined labels |
| `km_range` | string | Distance band to which the surcharge applies | `1501–4500 km` | CLEANED | Validated against 4 predefined band labels; typos corrected |
| `conflict_phase` | string | Conflict phase during which surcharge was in effect | `Baseline` | CLEANED | Mode-imputed for missing values |
| `fuel_surcharge_usd` | float64 | Fuel surcharge amount charged per passenger in USD | `62.00` | CLEANED | Median-imputed by `airline` + `km_range` subgroup (~18% missing) |
| `surcharge_type` | string | Classification of the surcharge mechanism | `YQ (Carrier-Imposed)` | CLEANED | Standardised; null → `Unknown` |
| `surcharge_currency` | string | Original currency of the surcharge before USD conversion | `GBP` | RAW | Used for audit; analysis uses USD-converted values only |
| `fx_rate_to_usd` | float64 | Exchange rate applied to convert to USD | `1.27` | CLEANED | Nulls filled with monthly average FX rate |
| `has_surcharge` | bool | Binary flag indicating whether a surcharge was charged | `True` | FEATURE-ENGINEERED | Derived: `True` if `fuel_surcharge_usd > 0` |
| `surcharge_coverage_ratio` | float64 | Ratio of surcharge collected to estimated fuel cost per segment | `0.68` | FEATURE-ENGINEERED | Computed as `fuel_surcharge_usd / jet_fuel_cost_per_segment` (joined from processed dataset) |

---

### B3. `oil_jet_fuel_prices.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `month` | string → datetime | Year-month of the price observation | `2022-03` | CLEANED | Cast to `datetime64[ns]`; primary temporal key |
| `conflict_phase` | string | Geopolitical phase label for this month | `Active Conflict` | CLEANED | Manually tagged; no imputation needed |
| `brent_crude_usd_per_barrel` | float64 | Monthly average Brent crude oil spot price in USD/barrel | `117.25` | CLEANED | Sparse early values interpolated linearly |
| `jet_fuel_usd_per_gallon` | float64 | Monthly average jet kerosene price in USD/gallon | `4.38` | CLEANED | Primary fuel cost metric; no nulls after interpolation |
| `jet_fuel_usd_per_barrel` | float64 | Jet fuel price expressed per barrel (42 gallons) | `183.96` | CLEANED | Derived/confirmed as `jet_fuel_usd_per_gallon × 42` |
| `yoy_change_pct` | float64 | Year-over-year % change in jet fuel price | `+62.1` | FEATURE-ENGINEERED | Computed as 12-month rolling % change |
| `fuel_price_lag_1m` | float64 | Jet fuel price from the previous month | `4.12` | FEATURE-ENGINEERED | Created via `.shift(1)`; used in regression as a lag predictor |
| `fuel_price_lag_2m` | float64 | Jet fuel price from two months prior | `3.98` | FEATURE-ENGINEERED | Created via `.shift(2)` |

---

### B4. `airline_financial_impact.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `month` | string → datetime | Month of the financial record (forward-filled from quarterly) | `2022-03` | CLEANED | Cast to `datetime64[ns]`; quarterly data forward-filled to monthly |
| `airline` | string | Airline name | `Lufthansa` | CLEANED | Lowercased and stripped |
| `conflict_phase` | string | Conflict phase label | `Active Conflict` | CLEANED | Forward-filled with quarterly data |
| `total_revenue_usd_m` | float64 | Total airline revenue in USD millions | `3,420.5` | CLEANED | Forward-filled from quarterly; Winsorised |
| `total_fuel_cost_usd_m` | float64 | Total fuel expenditure in USD millions | `1,028.0` | CLEANED | Forward-filled from quarterly |
| `fuel_cost_pct_revenue` | float64 | Fuel cost as % of total revenue | `30.1` | FEATURE-ENGINEERED | Derived: `total_fuel_cost / total_revenue × 100` |
| `ebitda_usd_m` | float64 | Earnings Before Interest, Tax, Depreciation & Amortisation in USD millions | `512.3` | CLEANED | Forward-filled; source is airline IR reports |
| `ebitda_margin_pct` | float64 | EBITDA as % of revenue | `14.97` | CLEANED | Recalculated post-imputation |
| `operating_cost_usd_m` | float64 | Total operating costs in USD millions | `2,908.2` | CLEANED | Forward-filled |
| `net_profit_usd_m` | float64 | Net profit (or loss) in USD millions | `203.1` | CLEANED | Forward-filled; negative values retained as-is |
| `hedging_ratio_pct` | float64 | Percentage of fuel requirements hedged via financial instruments | `42.0` | CLEANED | Median-imputed by airline where not disclosed |
| `capacity_ask_bn` | float64 | Available Seat Kilometres offered (billions) | `28.4` | CLEANED | Forward-filled from quarterly |

---

### B5. `route_cost_impact.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `month` | string → datetime | Year-month of the route cost record | `2022-03` | CLEANED | Cast to `datetime64[ns]` |
| `airline` | string | Airline operating the route | `Emirates` | CLEANED | Lowercased and stripped |
| `conflict_phase` | string | Conflict phase label | `Active Conflict` | CLEANED | Mode-imputed for sparse records |
| `route` | string | Origin–destination route pair | `DXB-LHR` | CLEANED | Normalised to alphabetical order |
| `avg_route_km` | float64 | Route distance in kilometres | `5,490.0` | CLEANED | Median-imputed by route |
| `fuel_cost_per_ask_usd` | float64 | Fuel cost per Available Seat Kilometre in USD | `0.038` | CLEANED | Core route-level efficiency metric; Winsorised |
| `total_operating_cost_per_ask_usd` | float64 | Total operating cost per ASK in USD | `0.091` | CLEANED | Winsorised at 1st/99th percentile |
| `fuel_share_of_total_cost_pct` | float64 | Fuel cost as % of total operating cost for this route | `41.8` | FEATURE-ENGINEERED | Derived: `fuel_cost_per_ask / total_operating_cost_per_ask × 100` |
| `load_factor_pct` | float64 | Percentage of seats filled on the route | `84.2` | CLEANED | Median-imputed by airline + route |
| `aircraft_type` | string | Primary aircraft type used on this route | `Boeing 777-300ER` | CLEANED | Standardised; null → `Unknown` |
| `co2_kg_per_pax_km` | float64 | CO₂ emissions per passenger-kilometre | `0.089` | RAW | Used for optional sustainability analysis |

---

### B6. `conflict_oil_events.csv`

| Column Name | Data Type | Description | Example | Stage | Transformation Applied |
|-------------|-----------|-------------|---------|-------|------------------------|
| `event_id` | int64 | Unique identifier for the geopolitical event | `42` | RAW | No transformation |
| `event_date` | string → datetime | Full date of the event onset | `2022-02-24` | CLEANED | Parsed to `datetime64[ns]`; truncated to `YYYY-MM` for joining |
| `month` | string | Year-month derived from `event_date` for joining | `2022-02` | FEATURE-ENGINEERED | `event_date.str[:7]` |
| `event_name` | string | Descriptive name of the geopolitical event | `Russia-Ukraine War Begins` | RAW | No transformation |
| `event_type` | string | Category of the event | `Armed Conflict` | CLEANED | Standardised to predefined taxonomy |
| `conflict_phase` | string | Phase label applied to this event | `Active Conflict` | RAW | Used as join key across all datasets |
| `oil_impact_level` | string | Qualitative rating of the event's impact on oil supply | `High` | CLEANED | Standardised to `Low`, `Medium`, `High`, `Extreme` |
| `affected_regions` | string | Comma-separated list of regions affected | `Europe, Middle East` | RAW | Used for narrative context only; not used as join key |
| `source_url` | string | URL of the primary source documenting the event | `https://...` | RAW | Retained for auditability; excluded from analysis |

---

---

## Part C — Data Transformation Summary

### C1. Raw → Cleaned → Final Dataset Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         RAW DATA LAYER                          │
│  6 CSVs in data/raw/ — heterogeneous schemas, mixed dtypes,    │
│  inconsistent date formats, missing values, naming conflicts    │
└───────────────────────────────┬─────────────────────────────────┘
                                │
         ┌──────────────────────▼──────────────────────┐
         │         02_cleaning.ipynb                   │
         │                                             │
         │  1. Standardise column names → snake_case   │
         │  2. Parse & normalise date fields           │
         │  3. Impute missing values                   │
         │     • Forward-fill (quarterly → monthly)    │
         │     • Median imputation (numeric fields)    │
         │     • Mode imputation (categorical fields)  │
         │  4. Remove duplicate rows                   │
         │  5. Correct data types (str → datetime,     │
         │     object → float, etc.)                   │
         │  6. Outlier detection (IQR method)          │
         │     • Flag with is_outlier = True           │
         │     • Winsorise at 1st / 99th percentile    │
         │  7. Normalise string join keys              │
         │     (.str.strip().str.lower())              │
         └──────────────────────┬──────────────────────┘
                                │
         ┌──────────────────────▼──────────────────────┐
         │         CLEANED DATA LAYER                  │
         │                                             │
         │  6 individually cleaned DataFrames          │
         │  Consistent dtypes, no structural nulls     │
         │  in primary join keys                       │
         └──────────────────────┬──────────────────────┘
                                │
         ┌──────────────────────▼──────────────────────┐
         │         merge_datasets.ipynb                │
         │                                             │
         │  Feature Engineering:                       │
         │  • km_range binned from avg_route_km        │
         │  • month extracted from event_date          │
         │                                             │
         │  LEFT JOINs:                                │
         │  Pair 1: oil_jet_fuel ⟕ conflict_events    │
         │  Pair 2: route_cost ⟕ airline_financial    │
         │  Pair 3: ticket_prices ⟕ fuel_surcharges   │
         │                                             │
         │  Post-join:                                 │
         │  • Remove duplicated columns                │
         │  • Resolve remaining join-induced NaNs      │
         └──────────────────────┬──────────────────────┘
                                │
         ┌──────────────────────▼──────────────────────┐
         │      05_final_load_prep.ipynb               │
         │                                             │
         │  Feature Engineering (analysis-ready):      │
         │  • year, month_num from month               │
         │  • price_change_pct (MoM % change)          │
         │  • real_ticket_price_usd (CPI-adjusted)     │
         │  • fuel_cost_pct_revenue                    │
         │  • surcharge_coverage_ratio                 │
         │  • fuel_price_lag_1m, lag_2m                │
         │  • has_surcharge (boolean flag)             │
         │  • fuel_share_of_total_cost_pct             │
         │                                             │
         │  Output: 3 Tableau-ready CSVs               │
         └──────────────────────┬──────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                     FINAL PROCESSED LAYER                       │
│  data/processed/                                                │
│  ├── 1_macro_oil_and_events.csv          (~200 rows, ~15 cols)  │
│  ├── 2_route_impacts_and_financials.csv  (~7,500 rows, ~20 cols)│
│  └── 3_ticket_prices_and_surcharges.csv  (~18,000 rows, ~25 cols│
└─────────────────────────────────────────────────────────────────┘
```

---

### C2. Missing Value Strategy Summary

| Strategy | Applied To | Justification |
|----------|-----------|---------------|
| **Forward-fill** | Financial metrics (quarterly → monthly) | Quarterly values are valid for the entire quarter |
| **Median imputation by subgroup** | `fuel_surcharge_usd` (by `airline` + `km_range`) | Preserves within-group distribution; avoids global median bias |
| **Median imputation by route** | `avg_route_km`, `load_factor_pct` | Route-level median is a stable central estimate |
| **Mode imputation** | `conflict_phase`, `surcharge_type`, `aircraft_type` | Categorical fields; most frequent class is a safe fallback |
| **Linear interpolation** | `brent_crude_usd_per_barrel` (sparse early records) | Commodity prices move continuously; interpolation is economically sound |
| **Row drop** | Records missing both `avg_ticket_price_usd` AND `jet_fuel_usd_per_gallon` | Core analysis columns; row carries no analytical value |

---

### C3. Column Additions & Removals Summary

| Action | Column | Reason |
|--------|--------|--------|
| **Added** | `km_range` | Required join key for Pair 3 merge; binned from `avg_route_km` |
| **Added** | `month` (from `event_date`) | Granularity normalisation for Pair 1 merge |
| **Added** | `year`, `month_num` | Enable temporal aggregation and seasonality decomposition |
| **Added** | `price_change_pct` | Momentum/volatility feature for regression modelling |
| **Added** | `real_ticket_price_usd` | Removes inflation bias from cross-period comparisons |
| **Added** | `fuel_cost_pct_revenue` | Key profitability ratio derived from financial data |
| **Added** | `surcharge_coverage_ratio` | Measures whether surcharges are cost-recovery or revenue-generating |
| **Added** | `fuel_price_lag_1m`, `fuel_price_lag_2m` | Captures delayed airline fare response to fuel cost changes |
| **Added** | `has_surcharge` | Binary flag for segmented analysis |
| **Added** | `is_outlier` | Enables sensitivity analyses with/without extreme observations |
| **Removed** | Duplicate suffixed columns (`_event`, `_financial`, `_surcharge_policy`) | Post-merge cleanup via `df.columns.duplicated()` filter |
| **Removed** | `source_url` (conflict events) | Non-analytical; retained in raw only |
| **Removed** | `surcharge_currency` | Analysis uses USD-converted values exclusively |

---

*End of Data Dictionary*
