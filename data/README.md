# Datasets — Records Research Group

All files are derived exclusively from public sources and dedicated to
the public domain under [CC0 1.0](../LICENSE).

**Citable deposit:** doi:[10.5281/zenodo.23904505](https://doi.org/10.5281/zenodo.23904505)
— the three `or_*` CSVs as a versioned, DOI'd dataset on Zenodo (CERN).
Cite that DOI for stability; this directory is the working copy.

## `accessibility_scoreboard.csv`

Per-request ledger for the Lane County records accessibility study:
requests filed, first responses, statuses, fees quoted vs paid, and
fee-waiver outcomes (ORS 192.324(5)). Rendered at
[`../scoreboard.html`](../scoreboard.html). Updated as correspondence
arrives.

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
