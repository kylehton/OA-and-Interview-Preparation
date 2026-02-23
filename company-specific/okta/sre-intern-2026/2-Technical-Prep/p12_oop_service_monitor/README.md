# P12 — Service Monitor (OOP + Data Structures)

Design a small monitoring component that tracks request outcomes per service.

---

## Task 1 — Implement ServiceMonitor

```python
class ServiceMonitor:

    def record(self, service: str, status_code: int) -> None:
        ...

    def error_rate(self, service: str) -> float:
        ...

    def top_unhealthy(self, n: int) -> list[tuple[str, float]]:
        ...
```

### Rules

- A request is considered an error if:
  ```
  status_code >= 500
  ```
- `error_rate = errors / total`
- Round error_rate to **4 decimal places**
- If service has no records → return `0.0`
- `record` ignores:
  - empty service
  - non-int status_code

### Sorting Rules for top_unhealthy(n)

Sort by:

1. error_rate descending  
2. total_requests descending  
3. service ascending  

Return up to `n` services.

---

## Example Runthrough

**Input:**
```python
monitor = ServiceMonitor()

monitor.record("api", 200)
monitor.record("api", 500)
monitor.record("api", 503)

monitor.record("auth", 200)
monitor.record("auth", 200)

monitor.record("", 500)        # ignored
monitor.record("db", "500")    # ignored (not int)
```

**Output:**
```python
monitor.error_rate("api")      # 0.6667
monitor.error_rate("auth")     # 0.0
monitor.error_rate("missing")  # 0.0

monitor.top_unhealthy(2)
# [("api", 0.6667), ("auth", 0.0)]
#
# api: 2 errors / 3 total = 0.6667
# auth: 0 / 2 = 0.0
# sorted by error_rate desc, then total_requests desc, then service asc
```

---

## Notes

- Use a dictionary like:
  ```
  { service: [total_count, error_count] }
  ```
- error_rate rounding:
  ```
  round(errors / total, 4)
  ```
