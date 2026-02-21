# P13 — HTTP Log Router (String Parsing + Robustness)

Each line in the file has the format:

    <method> <path> <status>

Examples:

    GET /api/v1/users 200
    POST /api/v1/login 401

---

## Task 1 — Route Statistics

Implement:

```python
route_stats(filepath: str) -> dict[str, dict[str, int]]
```

### Normalization Rule

Replace numeric path segments with `{id}`.

Example:

```
/api/v1/users/123/profile
→ /api/v1/users/{id}/profile
```

Only segments that are **pure digits** should be replaced.

---

### Validity Rules

- Line must contain exactly 3 tokens
- `status` must be an int
- `method` is ignored beyond validation
- Bucket status:
  - 200–299 → `"2xx"`
  - 400–499 → `"4xx"`
  - 500–599 → `"5xx"`
  - All others ignored

Each route should always include:

```
{"2xx": 0, "4xx": 0, "5xx": 0}
```

---

## Example Runthrough

**Input:**
```python
# file contents:
GET /api/v1/users/123/profile 200
GET /api/v1/users/456/profile 500
POST /api/v1/login 401
POST /api/v1/login 404
GET /api/v1/users/789/profile 201
GET /api/v1/users/123/profile abc     # invalid (status not int)
INVALID LINE
```

**Output:**
```python
{
  "/api/v1/users/{id}/profile": {"2xx": 2, "4xx": 0, "5xx": 1},
  "/api/v1/login": {"2xx": 0, "4xx": 2, "5xx": 0}
}
# users/{id}/profile:
# 200, 201 → 2xx = 2
# 500 → 5xx = 1
#
# login:
# 401, 404 → 4xx = 2
#
# invalid lines ignored
```

---

## Task 2 — Top Routes by 5xx

Implement:

```python
top_routes_by_5xx(filepath: str, k: int) -> list[tuple[str, int]]
```

### Rules

- Use normalized routes
- Sort by:
  1. 5xx count descending
  2. route ascending (tie-break)
- Return top `k`

---

## Example Runthrough (Top K)

**Input:**
```python
# same file contents as above
k = 1
```

**Output:**
```python
[("/api/v1/users/{id}/profile", 1)]
# users/{id}/profile has 1 five-hundred error
# login has 0
# top 1 returned
```

---

## Notes

- Split path by `/`, replace segments where `segment.isdigit()`.
- Be careful not to replace version segments like `v1` (not purely digits).
- Time complexity: O(N log N) due to sorting.
- Use streaming (line-by-line parsing).