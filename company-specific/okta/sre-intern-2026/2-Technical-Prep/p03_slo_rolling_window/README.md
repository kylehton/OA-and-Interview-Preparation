# P03 — Rolling SLO Breach Detector (Sliding Window)

You are given a log file with lines:

    <iso8601_timestamp> <service> <status_code>

Timestamps are ISO8601 like: 2026-02-17T10:05:30
All timestamps are in UTC and are non-decreasing in the file.

## Task

Implement:

    first_slo_breach(filepath: str, service: str, window_seconds: int, max_error_rate: float) -> str | None

Return the ISO timestamp of the **first request** that causes the rolling window
error rate to exceed `max_error_rate`.

Definition:
- Consider only lines for `service`.
- A request is an error if status_code >= 500.
- Rolling window includes requests with timestamps in [t - window_seconds, t] inclusive.
- error_rate = errors / total in that window.
- Breach occurs if error_rate > max_error_rate (strictly greater).

Return:
- timestamp string (exact token from input) when breach first occurs
- None if never breached
- Ignore invalid lines (bad token count or status not int)

## Constraints
- O(n) time; use a deque-like sliding window; do not rescan.
