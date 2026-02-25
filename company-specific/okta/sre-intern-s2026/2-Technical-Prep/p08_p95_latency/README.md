# P08 — P95 Latency per Service (Parsing + Percentiles)

Each non-empty line in the file has the format:

    <service> <latency_ms>

Example:

    auth 10
    auth 20
    auth 30

---

## Task 1 — Compute P95 Per Service

Implement:

```python
p95_latency(filepath: str) -> dict[str, int]
```

### Rules

For each service:

- Collect valid latencies:
  - Must have exactly 2 tokens
  - Latency must be integer ≥ 0
- Sort values ascending
- Compute p95 using **nearest-rank**:

  ```
  index = ceil(0.95 * n) - 1
  ```

- Return the integer latency at that index
- If a service has no valid samples → it should not appear

---

## Example Runthrough

**Input:**
```python
# file contents:
auth 10
auth 20
auth 30
auth -5        # invalid (negative)
auth abc       # invalid (not int)
db 100
db 200
invalid_line
```

**Output:**
```python
{"auth": 30, "db": 200}
# auth valid = [10, 20, 30] → n=3
# ceil(0.95*3)=ceil(2.85)=3 → index=2 → 30
# db valid = [100, 200] → n=2
# ceil(0.95*2)=ceil(1.9)=2 → index=1 → 200
```

---

## Task 2 — Top K Services by P95

Implement:

```python
top_p95_services(filepath: str, k: int)
```

Return:

- List of `(service, p95)` tuples
- Sorted by:
  1. p95 descending
  2. service ascending (tie-break)

---

## Example Runthrough (Top K)

**Input:**
```python
# file contents:
auth 10
auth 20
auth 30
db 100
db 200
cache 5
cache 7

k = 2
```

**Output:**
```python
[("db", 200), ("auth", 30)]
# db p95 = 200
# auth p95 = 30
# cache p95 = 7
# sorted by p95 desc → db, auth, cache
# top 2 returned
```

---

## Notes

- Sorting per service costs O(n log n) per service.
- Overall complexity: O(N log N) in worst case.
- Be careful with:
  - ceil computation
  - 0-based indexing
  - ignoring invalid lines