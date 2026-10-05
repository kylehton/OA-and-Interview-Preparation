# D04 — Reconciliation Import Failures

**Difficulty:** Medium  
**Target:** 40 minutes

The reconciliation job compares internal payments with rows exported by a
processor. Support has provided examples involving quoted identifiers,
duplicate processor IDs, and invalid negative amounts.

## Contract

Internal CSV records:

```text
<internal_id>,<processor_id>,<positive_amount>,<currency>
```

Processor CSV records:

```text
<processor_id>,<positive_amount>,<currency>,<SUCCEEDED|REFUNDED|FAILED>
```

- Use standard CSV parsing and formatting, including quotes and embedded commas.
- Ignore malformed rows and rows with non-positive amounts.
- Process internal rows in input order.
- Each processor row can be consumed at most once.
- For an internal row, prefer the earliest available exact `SUCCEEDED` match.
- Otherwise consume the earliest available row with its processor ID and report
  `MISMATCH`; report `MISSING` when none remains.
- With `include_orphans=True`, append all unconsumed processor rows in their
  original order.

Output CSV fields are `(internal_id, result, processor_id)`. Use `-` for the
internal ID of an orphan and the processor ID of a missing row.

Run `pytest -q`. Do not add a dataframe or CSV dependency.

