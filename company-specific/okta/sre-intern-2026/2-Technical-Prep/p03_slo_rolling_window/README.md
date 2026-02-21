# P03 — Rolling SLO Breach Detector (Sliding Window)

You are given log lines:

    <iso8601_timestamp> <service> <status_code>

Timestamps are UTC ISO8601 (e.g., 2026-02-17T10:05:30) and are non-decreasing in the file.

---

## Task

Implement:

```python
first_slo_breach(
    filepath: str,
    service: str,
    window_seconds: int,
    max_error_rate: float
) -> str | None
```

### Rules

- Consider only lines matching the given `service`
- A request is an error if `status_code >= 500`
- Rolling window includes requests with timestamps in:

  ```
  [t - window_seconds, t]   (inclusive)
  ```

- error_rate = errors / total in window
- Breach occurs if:

  ```
  error_rate > max_error_rate   (strictly greater)
  ```

Return:
- The ISO timestamp string of the **first request that causes the breach**
- The returned request must occur at a point where the window is greater than size 1.
- `None` if no breach occurs
- Ignore invalid lines:
  - not exactly 3 tokens
  - status not an int

Must run in O(n) time using a deque-like sliding window.

---

## Example Runthrough

**Input:**
```python
2026-02-17T10:00:00 api 200
2026-02-17T10:00:10 api 500
2026-02-17T10:00:20 api 500
2026-02-17T10:00:30 api 200

service = "api"
window_seconds = 15
max_error_rate = 0.5
```

**Output:**
```python
"2026-02-17T10:00:20"
# At 10:00:20 window = [10:00:05, 10:00:20]
# Includes 10:00:10 (500) and 10:00:20 (500)
# 2 errors / 2 total = 1.0 > 0.5 → breach
```

---

## Notes

- Convert ISO timestamps to epoch seconds for comparison.
- Maintain a deque storing:
  ```
  (timestamp_seconds, is_error)
  ```
- As time advances:
  - Pop from left while outside window
- Track:
  - total_count
  - error_count
- Check breach after each valid service record.
- Time complexity: O(n)
- Memory: O(window size)