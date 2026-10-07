# P07 — Webhook Retry Planner

**Difficulty:** Medium  
**Target:** 50 minutes  
**Entry point:** `plan_deliveries(endpoints, attempts, max_attempts) -> list[str]`

Inputs are comma-separated fields with surrounding whitespace trimmed. This
function analyzes historical attempts; it does not perform network calls.
Rows with the wrong number of fields are invalid. `max_attempts` is guaranteed
positive.

## Part 1 — Endpoints and completed delivery

Endpoint rows:

```text
<endpoint_id>,<base_delay>,<max_delay>
```

IDs are non-empty; both delays are positive integers with
`base_delay <= max_delay`. The first valid endpoint row for an ID wins.

Attempt rows:

```text
<timestamp>,<attempt_id>,<event_id>,<endpoint_id>,<status_code>
```

Timestamps are non-negative integers and status codes are integers from 100 to
599. IDs must be non-empty and the endpoint must exist. An HTTP 2xx status
completes that `(event_id, endpoint_id)` pair, so it produces no plan row.

Part 1 cases have at most one valid failed attempt per incomplete pair. Schedule
that pair at `timestamp + base_delay` and return:

```text
RETRY,<event_id>,<endpoint_id>,<scheduled_at>,1
```

Sort these rows by scheduled time, event ID, then endpoint ID. Part 2
generalizes the same row to multiple failures.

## Part 2 — Exponential backoff

For an incomplete pair with `n` valid failed attempts, schedule from its latest
attempt (greatest timestamp, then later input row):

```python
delay = min(base_delay * 2 ** (n - 1), max_delay)
scheduled_at = latest_timestamp + delay
```

Return the same row shape with the complete failure count:

```text
RETRY,<event_id>,<endpoint_id>,<scheduled_at>,<failure_count>
```

Keep the Part 1 retry sorting rule.

## Part 3 — Retry-After

A `429` attempt may have a sixth non-negative integer field:

```text
...,429,<retry_after_seconds>
```

When the chronologically latest attempt is such a row, use the larger of the
exponential delay and `retry_after_seconds`. A sixth field on any other status,
or an invalid sixth field, makes that attempt invalid.

## Part 4 — Idempotency and dead letters

Attempt IDs are globally unique; only the first valid row using an ID counts.
"First" means first in attempt input order, before chronological analysis.
Invalid rows do not reserve IDs. After idempotency is resolved, accepted
attempts are evaluated chronologically for latest-attempt selection. If any
valid attempt for a pair is 2xx, the pair is complete.

When an incomplete pair has at least `max_attempts` failures, output instead:

```text
DEAD,<event_id>,<endpoint_id>,<failure_count>
```

All retry rows come first. Append dead-letter rows sorted by event ID and then
endpoint ID.
