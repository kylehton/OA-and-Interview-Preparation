# P08 — Processor Reconciliation Join

**Difficulty:** Medium  
**Target:** 50 minutes  
**Entry point:** `reconcile(internal_rows, processor_rows, include_orphans=False) -> list[str]`

Parse all rows with normal CSV rules, including quoted fields. Trim every parsed
field. Malformed or invalid rows are ignored. Format returned rows with normal
CSV escaping as well.

## Part 1 — Exact matches

Internal rows:

```text
<internal_id>,<processor_id>,<positive_amount>,<currency>
```

Processor rows:

```text
<processor_id>,<positive_amount>,<currency>,<status>
```

IDs must be non-empty, currencies are exactly three uppercase ASCII letters,
and status is one of `SUCCEEDED`, `REFUNDED`, or `FAILED`.

For each valid internal row in input order, find a processor row with the same
processor ID, amount, currency, and status `SUCCEEDED`. Return:

```text
<internal_id>,MATCH,<processor_id>
```

## Part 2 — Missing and mismatched records

When no processor row has that ID, return:

```text
<internal_id>,MISSING,-
```

When the ID exists but no available row is an exact successful match, consume
the earliest available row for that ID and return:

```text
<internal_id>,MISMATCH,<processor_id>
```

Valid internal IDs are not required to be unique; every valid internal row is
processed independently in input order.

## Part 3 — Processor orphans

When `include_orphans=True`, append every unconsumed valid processor row in its
original order:

```text
-,ORPHAN,<processor_id>
```

## Part 4 — Duplicate IDs and one-to-one matching

Each processor row may be consumed at most once. Process internal rows in input
order. Among available processor rows with the requested ID:

1. consume the earliest exact successful match, if one exists;
2. otherwise consume the earliest row for that ID;
3. if none remain, mark the internal row `MISSING`.

This matching rule applies even when processor IDs repeat.

## Example

```python
internal = ["i1,p1,100,USD", "i2,p1,80,USD", "i3,p2,50,EUR"]
processor = ["p1,80,USD,SUCCEEDED", "p1,100,USD,SUCCEEDED"]

reconcile(internal, processor)
# ["i1,MATCH,p1", "i2,MATCH,p1", "i3,MISSING,-"]
```
