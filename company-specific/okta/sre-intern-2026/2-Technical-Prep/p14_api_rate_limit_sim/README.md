# P14 — API Client Simulation with 429 Handling (REST-flavored)

You are given a log file of outbound API requests your service attempted:

    <ts> <request_id> <endpoint>

You are also given an "API result file" mapping request_id -> response code:

    <request_id> <status_code>

The API can return 429 (rate limited). If a request gets 429, you must retry it later.

## Task

Implement:

    schedule_retries(requests_path: str, results_path: str, retry_delay_seconds: int) -> list[tuple[int,str]]

Return a list of (scheduled_ts, request_id) representing retries to perform.

Rules:
- Only schedule retries for requests whose status_code == 429
- The retry is scheduled at original_ts + retry_delay_seconds
- If a request_id appears multiple times in requests file, treat them as separate attempts and schedule separately.
- If a request_id from requests has no entry in results, ignore it.
- Ignore invalid lines in either file.
- Output sorted by scheduled_ts asc, then request_id asc.

Follow-up:
Implement:
    dedupe_latest_retry(...) -> list[tuple[int,str]]
If the same request_id gets multiple 429s, only keep the latest scheduled retry.
