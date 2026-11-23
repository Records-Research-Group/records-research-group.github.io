# Matching rules — OWRD FY2025 reconciliation

Deterministic rules used for every artifact in this folder. No manual
name reconciliation was applied; every unmatched payee is listed raw in
the `unmatched_*` files.

## Payee key

```
key(vendor) =
    uppercase(vendor_name)
    strip all non-[A-Z0-9 space] characters
    collapse runs of whitespace to single space
    trim
```

Applied identically to production `Vendor Name` and portal `VENDOR`.

## Fiscal-year definitions

- **Production side:** the agency's own `Fiscal Year` field
  (appropriation-year tag). FY2025 = rows tagged `2025`, regardless of
  `Doc Date`. 597 of those rows carry `Doc Date` after 2025-06-30
  ($6,682,744.24) — the appropriation-vs-transaction-date asymmetry
  that produces most of the shared-vendor delta.
- **Portal side:** the dataset's `fiscal_year` field, which is
  transaction-date based (verified: portal FY boundaries align with
  payment dates, not appropriation tags).

## Components

- `production_only` = payee keys in agency extract absent from portal
  extract. Signed positive (production exceeds portal).
- `portal_only` = payee keys in portal extract absent from agency
  extract. Signed negative (portal exceeds production).
- `shared_net_delta` = Σ(production_total − portal_total) over payee
  keys present in both. 374 keys matched; 131 carry nonzero delta.
- Gap identity: production_only + portal_only + shared_net_delta
  = production_total − portal_total. Verified: components sum to
  $1,316,558.48 exactly.

## Known limits

- Payee-key matching is name-string equality after normalization; the
  same entity under two spellings counts as two payees. This can shift
  amounts between the three components but cannot change the total gap.
- The portal publishes vendor×expend-class×FY aggregates only;
  payment-level attributes (doc numbers, obj codes, funds) exist solely
  on the production side, so person-payee identification (F2) uses
  production-side `Agy Obj`/`Fund`/`Doc` fields — stated per file.
- DSL comparison (`f2_person_payees_dsl.csv`) uses production window
  2024-07-24 → 2026-10-28 against portal FY2025+FY2026 rows; it is a
  partial-scope comparison and labeled as such.
