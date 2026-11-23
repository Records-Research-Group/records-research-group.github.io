# Datasets — Records Research Group

All files are derived exclusively from public sources and dedicated to
the public domain under [CC0 1.0](../LICENSE).

**Citable deposit:** doi:[10.5281/zenodo.23904505](https://doi.org/10.5281/zenodo.23904505)
— the three `or_*` CSVs as a versioned, DOI'd dataset on Zenodo (CERN).
Cite that DOI for stability; this directory is the working copy.

## `lane_county_housing_response_rollup.csv`

Aggregate totals of Lane County voucher-register payments to
homelessness-response and housing-assistance program lines,
CY2023–2025: one row per program line × year (expenditure account
code, program label, payment count, total dollars). Source: county
voucher payment register produced under the Oregon Public Records
Law; scope and caveats documented in the accompanying
[research note](../notes/2026-11-lane-county-housing-response-spend.html).
Aggregate published in place of the row-level register to limit
republishing of individual payee names.

## `wellpath_57233_contract_ladder.csv`

Per-instrument ladder for Lane County contract #57233 (Wellpath LLC —
medical, dental, and mental-health services at the Lane County Adult
Corrections facility): one row per executed instrument with its
increment and cumulative contract authority as stated in the
instrument itself, FY2023 base through Amendment 7 (term to
June 30, 2027). Source: complete executed instrument file released by
Lane County in two no-charge productions on public-records request
#26-1042 (ORS 192.311 et seq.). Figures are contract authority
(authorized ceiling), not payments made. Scope and caveats documented
in the accompanying
[research note](../notes/2026-11-wellpath-57233-contract.html).

## `accessibility_scoreboard.csv`

Per-request ledger for the Oregon records accessibility study: 163
requests filed Oct–Nov 2026 across ~130 bodies (state, county,
municipal, federal), with first responses, statuses, fees quoted vs
paid, fee-waiver outcomes (ORS 192.324(5)), and petition filings.
Rendered at [`../scoreboard.html`](../scoreboard.html) with stable
per-row anchors (`#rrg-NN`). Regenerated from the study ledger by
[`../_build_scoreboard.py`](../_build_scoreboard.py); updated as
correspondence arrives.

## `findings.csv`

Machine-readable index of the published findings (F1–F8): title,
bodies covered, witness rows in the scoreboard, status, and page
anchor. Rendered at [`../findings/`](../findings/).

## `or_muni_fac_overlay.csv`

Oregon public entities (counties, cities, school districts, higher-ed,
special districts) cross-referenced against Federal Audit Clearinghouse
(FAC) Single Audit submissions, audit years 2018–2025. One row per
entity: EIN, entity type, audit-year coverage, finding counts
(including repeat, material-weakness, and noncompliance findings),
questioned costs, low-risk-auditee rate, and total federal expenditure
in the latest audited year. Source: GSA FAC public data
(`fac.gov` dissemination tables).

## `or_dhs_fy2024_vendors_fac.csv`

Oregon DHS/OHA FY2024 vendor-payment records joined against FAC Single
Audit data and Oregon Secretary of State business-registry records.
One row per vendor: payment amounts, entity resolution
(registry match tier/confidence), and FAC audit history. Sources:
state vendor-payment records, GSA FAC public data, Oregon SOS business
registry.

## `or_invisibility_index.csv`

Vendor-level public-record presence matrix for Oregon DHS/OHA payees:
each vendor's visibility across public corpora — SOS registry, FAC,
NPPES (health-care provider registry), FSRS sub-award data, and
ORS 418.259 quarterly reports — as raw per-corpus counts. Sources:
state vendor-payment records, Oregon SOS, GSA FAC, CMS NPPES,
USAspending/FSRS, ODHS quarterly reports.

## What's withheld

The published CSVs contain source data and factual join fields only.
Internally derived screening columns — `fraud_risk_score`,
`is_shell_company`, `fraud_flags`, `has_exclusion_match`,
`is_hcbs_provider`, `entity_class`, `corpus_resolved`,
`sos_mill_only`, `nppes_namesake_n`, `fsrs_namesake_n`,
`ors259_severe`, `dark_score` — are withheld pending validation;
they are unvalidated heuristics, not findings of fact. Columns named
`match_tier` / `match_conf` / `match_note` document how entity
resolution was performed and are retained as join provenance.
