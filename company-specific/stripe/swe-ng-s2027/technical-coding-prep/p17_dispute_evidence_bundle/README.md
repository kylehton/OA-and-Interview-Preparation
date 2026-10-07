# P17 — Dispute Evidence Bundle

**Difficulty:** Hard  
**Target:** 75 minutes  
**Entry point:** `build_dispute_report(bundle_dir, as_of_date) -> list[str]`

Read a local dispute bundle containing `charges.csv`, `disputes.csv`,
`policy.json`, and optional evidence text files. Use UTF-8, normal CSV semantics,
and `pathlib`. Paths may be strings or `Path` objects. The function never makes
network requests and never modifies the bundle.

`as_of_date` must be an exact ISO date (`YYYY-MM-DD`). A missing or unreadable
required file, malformed JSON policy, bad required header, or invalid as-of date
returns `[]`.

`policy.json` is required from Part 1 onward because its `response_days` value
is needed to form every output row:

```json
{
  "response_days": 7,
  "high_value": {
    "USD": 5000,
    "EUR": 6000
  }
}
```

`response_days` must be a non-negative integer (not a Boolean). `high_value`
must be an object; every entry must use a valid currency and a positive integer
threshold (not a Boolean). Extra top-level keys are ignored. Any violation
makes the required policy file malformed and returns `[]`.

## Part 1 — Load and join CSV records

`charges.csv` has the exact header:

```text
charge_id,merchant_id,amount,currency,captured_at
```

A charge is valid when its IDs are non-empty, amount is positive, currency is
exactly three uppercase ASCII letters, and `captured_at` is an exact UTC
timestamp of the form `YYYY-MM-DDTHH:MM:SSZ`, with no fractional seconds or
numeric offset. The first valid charge row for an ID wins; invalid rows do not
reserve the ID.

`disputes.csv` has the exact header:

```text
dispute_id,charge_id,amount,opened_on,evidence_path
```

A dispute needs non-empty IDs, a known charge, a positive amount, and an exact
ISO opening date no earlier than the charge's UTC capture date. Evidence paths
may be empty. Trim every CSV field. Charge rows must have exactly five fields,
and dispute rows must have exactly five fields; malformed rows are skipped.

Output rows use normal CSV escaping:

```text
<dispute_id>,<merchant_id>,<currency>,<amount>,<deadline>,<status>
```

The deadline is `opened_on + response_days` calendar days. Part 1 cases assume
usable evidence, an on-time `as_of_date`, and no applicable high-value rule, so
their terminal status is `READY`. Parts 2 and 3 add the other statuses without
changing this row shape.

## Part 2 — Safely read evidence files

A non-empty evidence path is resolved relative to `bundle_dir`. Evidence is
usable only when the resolved path stays inside the bundle, names a regular
`.txt` file, can be decoded as UTF-8, and contains:

1. a first nonblank line exactly equal to `charge_id=<referenced_charge_id>`;
2. at least one additional nonblank line.

Otherwise the dispute has missing evidence. Symlink and `..` escapes must be
rejected even when the outside file exists. "Exactly equal" means after
removing only the line ending, not after trimming other surrounding whitespace.
Missing evidence changes status but does not make the dispute row invalid.

## Part 3 — Policy, deadlines, and review status

Determine final status in this precedence order:

1. `EXPIRED` when `as_of_date` is later than the deadline;
2. `MISSING_EVIDENCE` when evidence is unusable;
3. `REVIEW` when the currency has a high-value threshold and the dispute amount
   is greater than or equal to it;
4. otherwise `READY`.

The deadline itself is still on time.

## Part 4 — Idempotency and per-charge allocation

Process disputes in input order. The first valid dispute row for an ID wins.
Invalid rows do not reserve their ID. Total accepted dispute amounts against a
charge may not exceed that charge's amount. This limit is per charge, not per
merchant or currency group.

Evidence usability and the resulting status do not affect acceptance: an
accepted `MISSING_EVIDENCE` or `EXPIRED` dispute still reserves its ID and its
portion of the charge allocation.

Sort final rows by deadline and then dispute ID. CSV quoting is part of the
answer.

## Example

```python
build_dispute_report("fixtures/basic", "2026-01-10")
# [
#   "dp_1,m_1,USD,4000,2026-01-12,REVIEW",
#   'dp_2,"merchant,quoted",EUR,5000,2026-01-13,MISSING_EVIDENCE',
# ]
```
