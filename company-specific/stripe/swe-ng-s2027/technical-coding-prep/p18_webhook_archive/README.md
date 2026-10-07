# P18 — Webhook Archive Recovery

**Difficulty:** Hard  
**Target:** 75 minutes  
**Entry point:** `plan_webhook_archive(manifest_path, output_path=None) -> list[str]`

Recover a retry plan from an endpoint CSV and sharded newline-delimited JSON
attempt logs. Attempt shards may be plain `.jsonl` or gzip-compressed
`.jsonl.gz`. Use only the Python standard library.

The UTF-8 JSON manifest is:

```json
{
  "endpoint_file": "endpoints.csv",
  "attempt_files": ["attempts_01.jsonl", "attempts_02.jsonl.gz"],
  "max_attempts": 3
}
```

All three fields are required. `max_attempts` is a positive integer and not a
Boolean. Resolve paths relative to the manifest directory and reject any path
whose resolved target escapes it. The endpoint file must be a regular `.csv`;
attempt files must be regular files with one of the two suffixes above.
Malformed manifests or endpoint files return `[]`. Bad attempt shards are
skipped without aborting other shards. `endpoint_file` must be a string and
`attempt_files` must be a list; non-string entries inside that list are skipped.

## Part 1 — CSV endpoints and JSONL attempts

The endpoint CSV has this exact header:

```text
endpoint_id,base_delay,max_delay
```

IDs are non-empty, delays are positive integers, and
`base_delay <= max_delay`. Every endpoint data row must have exactly three
fields. The first valid endpoint row for an ID wins.

Every nonblank attempt-log line must decode to a JSON object with:

```json
{
  "timestamp": 10,
  "attempt_id": "a_1",
  "event_id": "event_1",
  "endpoint_id": "ep_1",
  "status": 500
}
```

Timestamp must be a non-negative integer, status an integer from `100` through
`599`, IDs non-empty strings, and the endpoint known. Python Booleans are not
integers for this problem. Blank, malformed, or invalid lines are ignored.
Extra object keys are ignored, except for the special `retry_after` validation
defined in Part 3. JSON string values are used exactly as stored and are not
whitespace-trimmed.
Any valid 2xx attempt completes its `(event_id, endpoint_id)` pair, which then
produces no output row.

Part 1 cases have at most one valid failed attempt per incomplete pair. Schedule
it at `timestamp + base_delay` and return a normal CSV-formatted row:

```text
RETRY,<event_id>,<endpoint_id>,<scheduled_at>,1
```

Sort these rows by scheduled time, event ID, then endpoint ID. Part 2
generalizes this plan to multiple attempts.

## Part 2 — Backoff and chronological recovery

For an incomplete pair with `n` valid failed attempts:

```python
delay = min(base_delay * 2 ** (n - 1), max_delay)
```

Schedule from the latest attempt: greatest timestamp, breaking a tie by later
manifest-file order and then later line order.

Return the same CSV row shape with the complete failure count:

```text
RETRY,<event_id>,<endpoint_id>,<scheduled_at>,<failure_count>
```

Keep the Part 1 retry sorting rule.

## Part 3 — Retry-After, gzip, and idempotency

A `429` object may contain a `retry_after` non-negative integer. When the latest
attempt contains it, use the greater of exponential delay and `retry_after`.
The field is optional for `429`; its presence on another status, or an invalid
value, makes that line invalid.

Attempt IDs are globally unique across every shard. Only the first valid line
using an ID counts. Invalid lines do not reserve IDs. Shards are ingested in
manifest order, regardless of filename.

Shard-level I/O is atomic: if a shard cannot be completely read, decompressed,
or decoded as UTF-8, ignore every line from that shard. A malformed individual
JSON line in an otherwise readable shard still only skips that line.

## Part 4 — Dead letters and output CSV

An incomplete pair with at least `max_attempts` failures is dead rather than
retried:

```text
DEAD,<event_id>,<endpoint_id>,,<failure_count>
```

Append dead rows after all retry rows, sorted by event ID and endpoint ID.

When `output_path` is provided, create parent directories and write this header
followed by exactly the returned rows:

```text
action,event_id,endpoint_id,scheduled_at,failure_count
```

Use UTF-8 and `newline=""` for CSV output.
For a valid archive with no plan rows, still write the header-only output file.
Do not create the output file when a required manifest or endpoint input is
invalid.

See `fixtures/basic/` for a complete local archive.
