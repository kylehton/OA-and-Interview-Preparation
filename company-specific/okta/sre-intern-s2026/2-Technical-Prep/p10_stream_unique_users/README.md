# P10 — Unique Users (Streaming + Memory Awareness)

Each line in the file has the format:

    <timestamp> <user_id> <event>

Example:

    2026-02-17T10:00:00 u1 login

---

## Task 1 — Count Unique Users

Implement:

```python
count_unique_users(filepath: str) -> int
```

### Rules

- A valid line:
  - Has exactly 3 tokens
  - `user_id` is non-empty
- Ignore invalid lines
- Must stream line-by-line (do not load entire file)
- O(unique_users) memory is acceptable

Return:
- Number of distinct `user_id`s

---

## Example Runthrough

**Input:**
```python
# file contents:
2026-02-17T10:00:00 u1 login
2026-02-17T10:01:00 u2 login
2026-02-17T10:02:00 u1 logout
invalid_line
2026-02-17T10:03:00  login   # invalid (missing user_id)
```

**Output:**
```python
2
# valid user_ids: u1, u2
# duplicates ignored
# invalid lines ignored
```

---

## Task 2 — Top Active Users

Implement:

```python
top_active_users(filepath: str, k: int) -> list[tuple[str, int]]
```

### Rules

- Count number of valid events per `user_id`
- Return top `k` users sorted by:
  1. count descending
  2. user_id ascending (tie-break)

---

## Example Runthrough (Top K)

**Input:**
```python
# file contents:
2026-02-17T10:00:00 u1 login
2026-02-17T10:01:00 u2 login
2026-02-17T10:02:00 u1 logout
2026-02-17T10:03:00 u3 login
2026-02-17T10:04:00 u2 logout

k = 2
```

**Output:**
```python
[("u1", 2), ("u2", 2)]
# counts:
# u1 -> 2
# u2 -> 2
# u3 -> 1
# sorted by count desc, then user_id asc
# top 2 returned
```

---

## Notes

- Use a set for unique counting.
- Use a dictionary for frequency counting.
- Sorting costs O(n log n).
- For very large datasets, a heap of size k can reduce sorting cost to O(n log k).
- Always process file line-by-line for memory safety.