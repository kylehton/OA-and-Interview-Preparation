# P05 — Rate Limiter (OOP + Sliding Window)

Implement a per-instance rate limiter:

    RateLimiter(max_requests: int, window_seconds: int)

Method:

    allow(timestamp: int) -> bool

`timestamp` is an integer seconds since epoch (monotonic non-decreasing calls are NOT guaranteed).

Allow rules:
- A request at time T is allowed if the number of allowed requests in the window
  [T - window_seconds + 1, T] is < max_requests.
- If allowed, it counts toward future windows.
- If rejected, it does NOT count.

## Example Runthrough

**Input:**
```python
10
10
10
12

max_requests = 2
window_seconds = 3
```

**Output:**
```python
[True, True, False, False]  # [8..10], [8..10], [8..10], [10..12] -> counts 0/1/2/2 (max=2)
```

At times: 10 (allow), 10 (allow), 10 (reject), 12 (allow)
- Window at T=10 is [8..10] includes 2 allowed -> reject third
- Window at T=12 is [10..12] includes allowed at 10,10 (2) so would reject if counted,
  but window_seconds=3 => [10..12] includes both -> actually still 2, so allow would be False.

Careful! This is why the exact bounds matter.

Use the defined bounds above.

## Requirements
- You may assume timestamps are non-negative.
