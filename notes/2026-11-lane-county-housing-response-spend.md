# Lane County homelessness-response spending, CY2023–2025

*Research note. Posted 2026-11-13. Dataset: [`../data/lane_county_housing_response_rollup.csv`](../data/lane_county_housing_response_rollup.csv).*

## What this is

A rollup of Lane County voucher-register payments to
homelessness-response and housing-assistance program lines for
calendar years 2023–2025. Built to make one number checkable: how
much the county spends managing the housing shortage after the fact.

## Source & method

- **Source:** Lane County voucher payment register covering
  CY2023–2025, produced under the Oregon Public Records Law
  (ORS 192.311 et seq.).
- **Normalization:** payments keyed to the county's own expenditure
  account codes and program labels; no reclassification of the
  county's accounting.
- **Scope:** program lines in the county's Human Services
  housing/homelessness block (codes 3427060–3427070), plus the
  Oregon Rehousing Initiative (3427032), Long-Term Rental
  Assistance (3427038), the Statewide Shelter Program (3427040),
  Governor's Executive Order 23-02 homelessness-response funding
  (3427076), and Housing & Community Development (5152070).
- **Figures are gross voucher payments.** Much of this spending is
  restricted state and federal pass-through money administered by
  the county; it is not all discretionary county money. About $0.6M
  of payments carry no parseable date in the register export and are
  counted in the total only, not in the per-year figures.

## Findings

- **Total, CY2023–2025: $46,955,415** across 16 program lines and
  5,745 payments.
- **By year:** 2023 — $5.6M · 2024 — $22.1M · 2025 — $18.7M
  (undated — $0.6M). The 2024 jump reflects Executive Order 23-02
  shelter-capacity funding arriving in the register.
- **Largest program lines:** Executive Order 23-02 — $14.5M;
  Continuum of Care — $8.1M; Prevention & Diversion — $6.8M;
  Statewide Shelter Program — $4.4M; Long-Term Rental Assistance —
  $4.2M; Emergency Housing Account — $2.2M; Oregon Rehousing
  Initiative — $1.9M.

## What this does and does not show

This note establishes the *scale* of downstream-response spending —
shelter, rent assistance, rehousing, and homelessness services. It
does **not** show waste: most lines are restricted pass-through
programs performing triage that the housing shortage makes
necessary, and most cannot legally be redirected to construction.
It does not include staff costs paid outside the voucher register,
budgeted (versus actual) amounts, or spending by cities, the
housing authority, or nonprofits from other funding streams.

## Data

[`lane_county_housing_response_rollup.csv`](../data/lane_county_housing_response_rollup.csv)
— aggregate totals by program line and year. We publish the
aggregate rather than the row-level register to limit republishing
of individual payee names; the underlying register is a public
record obtainable from Lane County.
