# P01 — Log Error Rate Aggregator (File I/O + Parsing)

You are given an access log file where each non-empty line is:

    <iso8601_timestamp> <service> <status_code>

Example:

    2026-02-17T10:00:00 auth-service 200
    2026-02-17T10:00:01 auth-service 500

---

## Task 1 — Compute Error Rate Per Service

Implement:

```python
compute_error_rate(filepath: str) -> dict[str, float]
```

### Rules

A line is valid only if:

- It splits into exactly 3 tokens
- `status_code` is an integer
- `service` is non-empty

For each service:

- total = number of valid lines
- errors = count where `status_code >= 500`
- error_rate = errors / total
- Round to **4 decimal places**

If a service has 0 valid lines → it must not appear.

Process file line-by-line (large file safe).

---

## Example Runthrough

**Input:**
```python
2026-02-17T10:00:00 auth 200
2026-02-17T10:00:01 auth 500
2026-02-17T10:00:02 billing 503
2026-02-17T10:00:03 billing 200
bad line
```

**Output:**
```python
{
    "auth": 0.5,
    "billing": 0.5
}
# auth: 1 error / 2 total = 0.5
# billing: 1 error / 2 total = 0.5
# invalid lines ignored
```

---

## Task 2 — Services Sorted by Error Rate

Implement:

```python
services_by_error_rate(filepath: str) -> list[tuple[str, float]]
```

Return list of `(service, error_rate)` sorted by:

1. error_rate descending  
2. total_requests descending  
3. service lexicographically ascending  

---

## Example Runthrough (Sorted)

**Input:**
```python
2026-02-17T10:00:00 auth 200
2026-02-17T10:00:01 auth 500
2026-02-17T10:00:02 billing 503
2026-02-17T10:00:03 billing 200
2026-02-17T10:00:04 billing 503
```

**Output:**
```python
[("billing", 0.6667), ("auth", 0.5)]
# billing: 2 errors / 3 total = 0.6667
# auth: 1 / 2 = 0.5
# sorted by error_rate desc
```

---

## Notes

- Use a dictionary like:
  ```
  { service: [total_count, error_count] }
  ```
- Round with:
  ```
  round(errors / total, 4)
  ```
- Time complexity: O(n)
- Memory: O(#services)
- Timestamp does not need validation beyond being a token.