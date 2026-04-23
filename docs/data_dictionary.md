# 📖 Data Dictionary — Airline Ticket Prices vs Fuel Costs Analysis

> **Project:** C\_G18 — Airline Ticket Prices vs Fuel Costs Analysis
> **Course:** Data & Visual Analytics (DVA) Capstone
> **Last Updated:** April 2026

---

## Part A — Raw Data Overview

### A1. Dataset Inventory

| # | File | Size | Est. Rows | Est. Columns | Domain |
|---|------|------|-----------|--------------|--------|
| 1 | `airline_ticket_prices.csv` | ~2.1 MB | ~18,000 | 14 | Passenger fare |
| 2 | `fuel_surcharges.csv` | ~1.3 MB | ~12,000 | 13 | Surcharge policy |
| 3 | `oil_jet_fuel_prices.csv` | ~8.6 KB | ~180 | 8 | Commodity prices |
| 4 | `airline_financial_impact.csv` | ~110 KB | ~900 | 12 | Airline financials |
| 5 | `route_cost_impact.csv` | ~504 KB | ~7,500 | 11 | Route economics |
| 6 | `conflict_oil_events.csv` | ~7.4 KB | ~150 | 9 | Geopolitical events |

### A2. Source & Collection Method

| File | Assumed Source | Collection Method |
|------|---------------|-------------------|
| `airline_ticket_prices.csv` | U.S. DOT DB1B database; European CAA fare filings | Quarterly public disclosure; web aggregation |
| `fuel_surcharges.csv` | IATA fuel surcharge bulletins; airline tariff filings | Manual compilation from airline websites and IATA publications |
| `oil_jet_fuel_prices.csv` | U.S. Energy Information Administration (EIA); IATA Jet Fuel Monitor | Monthly automated data download |
| `airline_financial_impact.csv` | Airline annual reports (10-K / 20-F); ICAO financial statistics | Structured extraction from PDF/HTML financial filings |
| `route_cost_impact.csv` | ICAO cost-per-ASK statistics; airline operational disclosures | Aggregated from ICAO Economics report series |
| `conflict_oil_events.csv` | ACLED; OPEC press releases; Reuters historical news | Manual tagging and curation of geopolitical event timelines |

### A3. Data Types & Structure

| File | Primary Structure | Temporal Granularity | Key Identifiers |
|------|------------------|---------------------|-----------------|
| `airline_ticket_prices.csv` | Panel (airline × route × month) | Monthly | `airline`, `iata_code`, `route`, `month` |
| `fuel_surcharges.csv` | Panel (airline × km_range × month) | Monthly | `airline`, `km_range`, `month`, `conflict_phase` |
| `oil_jet_fuel_prices.csv` | Time-series | Monthly | `month` |
| `airline_financial_impact.csv` | Panel (airline × quarter) | Quarterly | `airline`, `month`, `conflict_phase` |
| `route_cost_impact.csv` | Panel (airline × route × month) | Monthly | `airline`, `route`, `month`, `conflict_phase` |
| `conflict_oil_events.csv` | Event log | Daily (normalised to Monthly) | `event_id`, `event_date`, `conflict_phase` |

### A4. Known Raw Data Limitations

| Limitation | Affected File(s) | Impact |
|------------|-----------------|--------|
| **Missing surcharge records** | `fuel_surcharges.csv` | ~18% of airline–route–month combos lack a matching surcharge entry |
| **Quarterly vs. monthly mismatch** | `airline_financial_impact.csv` | Financial metrics must be forward-filled across 3 monthly rows |
| **Inconsistent date formats** | `conflict_oil_events.csv` | `event_date` stored as full ISO date vs. `YYYY-MM` elsewhere |
| **Sparse oil price history** | `oil_jet_fuel_prices.csv` | Only ~180 monthly rows; earliest records may have interpolated values |
| **Route naming inconsistencies** | `airline_ticket_prices.csv`, `route_cost_impact.csv` | Same route expressed as `JFK-LHR` and `LHR-JFK` depending on source |
| **Self-reported financials** | `airline_financial_impact.csv` | Figures are airline-disclosed and may reflect accounting treatments |
| **Survivorship bias** | All files | Only airlines with continuous reporting represented; bankrupt carriers excluded |
