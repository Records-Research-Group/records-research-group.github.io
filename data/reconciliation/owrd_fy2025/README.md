# OWRD FY2025 portal↔production reconciliation

Reproduction materials for findings F3 (portal↔ledger divergence) and the
OWRD portion of F2 (person-payee exclusion). Published 2026-11-23.

## Inputs

- **Agency production** — `resp064_OWRD_sweep_vendor_payments_2026-11-09.xlsx`
  (Oregon Water Resources Department response to RRG-64, received
  2026-11-09; payment-level vendor payments, fields include `Doc Date`,
  `Fiscal Year` = appropriation-year tag, `Sfms Trans Amt`, `Agy Obj`,
  `Fund`, `Cur Doc No`). This workbook's `agency_extract_owrd_fy2025.csv`
  contains the 6,965 rows tagged `Fiscal Year = 2025` by the agency.
- **Portal extract** — `data.oregon.gov` Socrata dataset `y9g9-xsxs`
  ("Agency Expenditures — Multi-Year Report"), rows where `agency = 690`
  (WATER RESOURCES, DEPT OF) and `fiscal_year = 2025`. Pulled 2026-11-23;
  622 vendor×expend-class rows, the same granularity the portal publishes
  (vendor aggregates, not payment-level). The portal's own FY tag is
  transaction-date based.

## Result

| Component | n | Amount |
|---|---:|---:|
| Production total (FY2025 tag) | 6,965 rows | $33,982,830.31 |
| Portal total (FY2025) | 622 rows | $32,666,271.83 |
| **Gap (production − portal)** | | **$1,316,558.48** |
| Production-only payees | 246 | +$4,122,981.67 |
| Portal-only payees | 22 | −$5,293,327.98 |
| Shared-vendor net delta | 374 (131 nonzero) | +$2,486,904.79 |

Components sum exactly to the gap. See
[reconciliation.csv](reconciliation.csv).

## Reading the components

- **Portal-only payees** are inter-agency transfers (DAS $2.72M, DOJ
  $2.09M, Employment, Secretary of State, State Police, PERS) — the
  portal counts intra-state transfers the vendor-payment export
  excludes.
- **Production-only payees** mix FY-boundary grants (City of Beaverton
  $2.74M dated 2025-07-10, tagged FY25 by appropriation year) and
  payees the portal suppresses — including named individuals; see
  `f2_person_payees_owrd.csv` for the reproducible filter (obj
  6801/6725, fund 4330: 44 payees / $1,120,783.20 within FY25 tags;
  131 payees / $3,489,700.86 across all production years).
- **Shared-vendor delta** is FY-tagging: 597 production rows tagged
  FY25 carry Doc Dates after 2025-06-30 ($6,682,744.24) because the
  agency tags by appropriation year while the portal books by
  transaction date.

The two totals measure spending under different coverage and fiscal-year
conventions; the components quantify each convention's contribution at
payee level. Whether additional convention differences exist below the
payee-aggregate level is not resolved — the portal publishes only
vendor×class×FY aggregates.

## Prior internal figures

An earlier working note cited 208 grant payees / ~$1.08M (F2) and "131
shared vendors" for the delta component. The published filters here are
the governing definitions: the shared-delta count reproduces as 131
nonzero-delta vendors of 374 matched; the grant-recipient class
reproduces as 44/$1,120,783.20 under the stated obj+fund filter —
earlier figures used slightly different cuts. DSL replication
(`f2_person_payees_dsl.csv`) yields 17 production-only payees /
$100,018.43 under the stated window; an earlier note counted
16/$205,619 under a different window.

## Reproduce

```python
# portal side
GET https://data.oregon.gov/resource/y9g9-xsxs.json
    ?$where=agency='690' AND fiscal_year='2025'&$limit=5000
# agency side: rows where `Fiscal Year` = 2025 in the OWRD production
# payee match key: upper(name), strip non-alphanumeric, collapse spaces
```

## Files

Reading order: rules → inputs → component table → lists → F2 lists.

| File | Contents |
|---|---|
| [MATCHING_RULES.md](MATCHING_RULES.md) | Deterministic payee-key, fiscal-year, and component definitions. No manual name reconciliation. |
| [agency_extract_owrd_fy2025.csv](agency_extract_owrd_fy2025.csv) | Agency input: 6,965 production rows the agency tagged `Fiscal Year = 2025`, from the 14,257-row OWRD production workbook. |
| [portal_extract_owrd_fy2025.csv](portal_extract_owrd_fy2025.csv) | Portal input: 622 rows pulled 2026-11-23 from data.oregon.gov `y9g9-xsxs` (`agency='690'`, `fiscal_year='2025'`). |
| [reconciliation.csv](reconciliation.csv) | Signed component totals; components sum to the $1,316,558.48 gap exactly. |
| [unmatched_production_only.csv](unmatched_production_only.csv) | 246 production payees absent from the portal extract (+$4,122,981.67). |
| [unmatched_portal_only.csv](unmatched_portal_only.csv) | 22 portal payees absent from the agency extract (−$5,293,327.98). |
| [shared_vendor_delta.csv](shared_vendor_delta.csv) | 374 payee keys present in both extracts with per-vendor delta; 131 carry nonzero delta (+$2,486,904.79 net). |
| [f2_person_payees_owrd.csv](f2_person_payees_owrd.csv) | F2 person-payee list, OWRD: production-only payees under the obj 6801/6725 + fund 4330 filter (131 names across all production years). |
| [f2_person_payees_dsl.csv](f2_person_payees_dsl.csv) | F2 person-payee list, DSL: 17 production-only payees under the stated window — a partial-scope comparison. |
| [RRG_F2F3_VERIFICATION_PACKET.md](RRG_F2F3_VERIFICATION_PACKET.md) | Single-file verification snapshot: this README, the matching rules, all component lists, and both full extracts inline. Generated 2026-11-23; the individual files above are authoritative. |

Raw-file routes for automated readers:
`https://raw.githubusercontent.com/Records-Research-Group/records-research-group.github.io/main/data/reconciliation/owrd_fy2025/<filename>`
