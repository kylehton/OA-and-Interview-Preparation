# P14 — API Client Simulation with 429 Handling (REST-centric)

You are given:

1) A requests log:

    <ts> <request_id> <endpoint>

2) A results file:

    <request_id> <status_code>

The API may return 429 (rate limited). Those requests must be retried later.

---

## Task 1 — Schedule Retries

Implement:

```python
schedule_retries(
    requests_path: str,
    results_path: str,
    retry_delay_seconds: int
) -> list[tuple[int, str]]
```

### Rules

- Only schedule retries where `status_code == 429`
- Scheduled time:

  ```
  scheduled_ts = original_ts + retry_delay_seconds
  ```

- If a `request_id` appears multiple times in the requests file:
  - Treat each line as a separate attempt
  - Schedule separately
- If a request_id has no entry in results → ignore
- Ignore invalid lines in either file
- Output sorted by:
  1. scheduled_ts ascending
  2. request_id ascending

---

## Example Runthrough

**Input:**
```python
# requests file:
100 r1 /users
105 r2 /login
110 r1 /users
invalid line

# results file:
r1 429
r2 200
r3 429
invalid
```

retry_delay_seconds = 10
```

**Output:**
```python
[(110, "r1"), (120, "r1")]
# r1 at ts=100 → 429 → retry at 110
# r1 at ts=110 → 429 → retry at 120
# r2 → 200 → no retry
# r3 not in requests → ignored
# sorted by scheduled_ts, then request_id
```

---

## Follow-up — Deduplicate Latest Retry

Implement:

```python
dedupe_latest_retry(
    requests_path: str,
    results_path: str,
    retry_delay_seconds: int
) -> list[tuple[int, str]]
```

### Rule

If the same `request_id` gets multiple 429s:

- Keep **only the latest scheduled retry**
- Return sorted by:
  1. scheduled_ts ascending
  2. request_id ascending

---

## Example Runthrough (Deduped)

**Input:**
```python
# same files as above
retry_delay_seconds = 10
```

**Output:**
```python
[(120, "r1")]
# r1 scheduled at 110 and 120
# keep only the latest (120)
```

---

## Notes

- Parse results into a dict: {request_id: status_code}
- Validate:
  - requests lines must have exactly 3 tokens
  - results lines must have exactly 2 tokens
  - ts and status_code must be integers
- Time complexity:
  - O(N + M) parsing
  - O(K log K) sorting retries
- Be careful:
  - Multiple request lines with same ID
  - Missing result entries
  - Invalid lines