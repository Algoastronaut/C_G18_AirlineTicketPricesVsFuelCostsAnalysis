# C_G18 — Airline Ticket Prices vs Fuel Costs Analysis

**Course:** Data & Visual Analytics (DVA) — Capstone Project  
**Team:** Group 18  
**Academic Year:** 2025-2026  
**Sector:** Aviation & Travel Industry  
**Institute:** Newton School of Technology  
**Faculty Mentor:** Prof. Archit Raj  
**Submitted:** 28 April 2026

---

## Problem Statement

Jet fuel is one of the largest airline operating costs (about 20-30% of total operating expenses). Fuel price volatility creates a key strategic question for airlines: **how much of fuel cost increase is passed to passengers through fares and surcharges?**

This project evaluates the relationship between fuel prices and airline ticket prices across different market phases (pre-pandemic, COVID-19, recovery, and geopolitical conflict periods).

---

## Executive Summary

### Approach

- Integrated six aviation and macro datasets (fuel, fares, surcharges, route costs, financial metrics, conflict events).
- Built a Python ETL pipeline for cleaning, feature engineering, and integration.
- Performed EDA and statistical analysis (correlation, OLS regression, t-test, ARIMA forecasting, K-Means clustering).
- Published findings through an interactive Tableau dashboard.

### Headline Findings

- Fuel prices increase airline cost pressure, but pass-through to fares is **partial**, not 1:1.
- Fuel-fare correlation is weak (~0.28), and regression explanatory power is low (R2 ~0.08).
- Demand conditions and global events influence ticket prices more strongly than fuel cost alone.
- Conflict and recovery phases show higher volatility and fare spikes.

---

## Objectives

1. Quantify fuel-to-fare pass-through behavior.
2. Evaluate fuel surcharge behavior relative to fuel movement.
3. Compare sensitivity by airline type, route class, and region.
4. Measure conflict phase impact on pricing dynamics.
5. Build a decision-focused Tableau dashboard.

---

## Sector and Business Context

Commercial aviation operates on thin margins and is exposed to external shocks. Recent years combined demand shocks (COVID-19), recovery shifts, and conflict-linked fuel volatility (for example Russia-Ukraine and US-Iran tensions), making pricing decisions more complex.

### Primary Stakeholders

- C-suite leaders (financial and risk decisions)
- Revenue management teams (fare optimization)
- Pricing strategy teams (competitive positioning)

### Business Value

- Supports demand-aware dynamic pricing
- Improves fuel-risk and hedging planning
- Helps evaluate surcharge strategy transparency
- Strengthens resilience planning for disruption phases

---

## Scope

### In Scope

- Monthly Brent crude and jet fuel trend tracking
- Ticket fare and fuel surcharge analysis
- Phase-based comparison (pre-pandemic, COVID-19, recovery, conflict)
- Statistical relationship testing (correlation + regression + t-test)

### Out of Scope

- Real-time prediction of individual ticket prices
- Full airline-by-airline hedging attribution
- Exhaustive route-level coverage of all global carriers

---

## Project Structure

```text
├── README.md
├── requirements.txt
├── data/
│   ├── raw/
│   └── processed/
├── docs/
│   └── data_dictionary.md
├── notebooks/
│   ├── 01_extraction.ipynb
│   ├── 02_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_final_load_prep.ipynb
├── scripts/
│   └── etl_pipeline.py
├── tableau/
└── reports/
```

---

## Data and ETL Pipeline

### Raw Datasets

- `airline_ticket_prices.csv`
- `fuel_surcharges.csv`
- `oil_jet_fuel_prices.csv`
- `airline_financial_impact.csv`
- `route_cost_impact.csv`
- `conflict_oil_events.csv`

### Primary Analysis Dataset

- `3_ticket_prices_and_surcharges.csv` (generated in `data/processed/`)
- Core analytical merge: ticket prices + fuel surcharges

### Cleaning and Transformation

- Column standardization (lowercase, underscores)
- Type conversion and date normalization
- Missing value handling (time-aware fill and defaults)
- Invalid value treatment (e.g., infinite ratio values)
- IQR-based outlier detection with retention via `is_extreme_fare`
- Feature engineering:
  - Time features (`year`, `month_num`, `quarter`)
  - Pricing ratios (`fuel_surcharge_ratio`, `taxes_ratio`, `base_ratio`)
  - Change features (`yoy_price_change_pct`, `yoy_surcharge_change_pct`)
  - Efficiency metrics (`fare_per_km`, `crude_jet_ratio`)

---

## Notebook Workflow

1. `01_extraction.ipynb` — load and validate raw datasets
2. `02_cleaning.ipynb` — clean, normalize, and engineer features
3. `03_eda.ipynb` — trend, distribution, and comparative exploration
4. `04_statistical_analysis.ipynb` — regression, hypothesis testing, forecasting, clustering
5. `05_final_load_prep.ipynb` — prepare export files for dashboarding

---

## Statistical Summary

### Regression and Correlation

- Positive fuel-fare relationship exists.
- Fuel-fare relationship is weak overall (r ~0.28).
- Low R2 (~0.08) indicates fuel alone does not explain most fare variation.

### Hypothesis Testing

- Ticket prices differ significantly across market/conflict phases (`p < 0.05`).

### Forecasting and Clustering

- ARIMA indicates stable/slightly rising near-term levels but misses sudden shocks.
- K-Means reveals three pricing regimes:
  - low-price regime
  - mid-price regime
  - high-price regime

---

## Tableau Dashboard

**Tableau Public:** [Executive Overview](https://public.tableau.com/app/profile/syed.darain.qamar7769/viz/AirlinePricesAnalysis/ExecutiveOverview)

### Dashboard Views

- Executive summary (ticket price, YoY, load factor, extreme fare %)
- Operational drill-down (fare components and route-class behavior)
- Fuel impact analysis (fuel, cost share, surcharge behavior)
- Conflict and risk analysis (phase-level pricing volatility)

### Filters

- Conflict Phase
- Airline Type
- Route Class
- Year

---

## Key Insights

1. Fuel cost increases do not translate proportionally into ticket prices.
2. Pricing behavior is multi-factor: demand, route economics, and external shocks matter heavily.
3. Conflict/recovery periods show stronger fare volatility and spikes.
4. Fuel surcharges are used strategically, not purely as direct cost recovery.
5. Long-haul segments are generally more sensitive to fuel movements.
6. Forecasts are stable in normal conditions but under-react to abrupt shocks.

---

## Recommendations

1. **Dynamic pricing:** prioritize demand and competitive context alongside fuel trends.
2. **Fuel risk management:** strengthen hedging and volatility planning.
3. **Route-level strategy:** differentiate long-haul vs short-haul pricing playbooks.
4. **Crisis response:** implement disruption-phase pricing scenarios.
5. **Demand-capacity alignment:** improve load factor management to stabilize revenue.

---

## Limitations and Future Scope

### Limitations

- Historical relationships may not fully generalize under new macro regimes.
- Correlation/regression indicate association, not strict causation.
- Aggregated analysis can hide airline-specific tactical behavior.
- Forecasting model does not fully integrate exogenous risk signals.

### Future Scope

- Add advanced forecasting (SARIMA/Prophet/ML with exogenous variables)
- Expand route-level and airline-level sensitivity analysis
- Incorporate competition and macro indicators
- Build near real-time data refresh workflows
- Explore causal inference methods for stronger driver attribution

---

## How to Run

```bash
git clone https://github.com/connectwithvanshika/C_G18_AirlineTicketPricesVsFuelCostsAnalysis.git
cd C_G18_AirlineTicketPricesVsFuelCostsAnalysis

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

jupyter lab
```

Run notebooks in sequence:

```text
01_extraction -> 02_cleaning -> 03_eda -> 04_statistical_analysis -> 05_final_load_prep
```

---

## Team

| Role | Name | GitHub |
| --- | --- | --- |
| Project Lead | Vanshika Yadav | connectwithvanshika |
| Data Lead | Shrijan Sanidhya | ShrijanSanidhya |
| ETL Lead | Killi Akshith Kumar | Akshith17323 |
| Analysis Lead | Saumya Soni | Algoastronaut |
| Visualization Lead | Syed Darain Qamar | darain24 |
| Strategy Lead | B Mohith Venkata Sai Krishna | mohith0705 |
| PPT & Quality Lead | Vanshika Yadav | connectwithvanshika |

---

## Contribution Matrix

| Team Member | Dataset & Sourcing | ETL & Cleaning | EDA & Analysis | Statistical Analysis | Tableau Dashboard | Report Writing | PPT & Viva |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Vanshika Yadav | - | - | - | ✓ | - | ✓ | ✓ |
| Shrijan Sanidhya | ✓ | ✓ | - | - | - | ✓ | - |
| Killi Akshith Kumar | ✓ | ✓ | ✓ | - | - | - | - |
| Saumya Soni | - | - | - | ✓ | - | ✓ | ✓ |
| Syed Darain Qamar | ✓ | - | - | - | ✓ | - | ✓ |
| B Mohith Venkata Sai Krishna | ✓ | ✓ | ✓ | - | - | - | - |

---

For academic use only. Data used is public, aggregated, or educationally prepared.
