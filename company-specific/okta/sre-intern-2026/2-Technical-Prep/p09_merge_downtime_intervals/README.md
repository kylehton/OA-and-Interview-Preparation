# P09 — Merge Downtime Intervals (Intervals + Sorting)

Each non-empty line in the file has the format:

    <service> <start> <end>

Where:
- `start` and `end` are integer seconds since epoch
- Intervals are **inclusive**: `[start, end]`
- Assume `start <= end` for valid intervals (there may be invalid intervals provided in input)

---

## Task 1 — Merge Downtime Intervals

Implement:

```python
merge_downtime(filepath: str) -> dict[str, list[tuple[int, int]]]
```

### Rules

For each service:

- Parse valid intervals:
  - Must have exactly 3 tokens
  - `start` and `end` must be integers
  - `start <= end`
- Sort intervals by `start` ascending
- Merge intervals that are:
  - **Overlapping**: `next.start <= current.end`
  - **Adjacent**: `next.start == current.end + 1`
- Return merged intervals sorted by start ascending

Invalid lines must be ignored.

---

## Example Runthrough

**Input:**
```python
# file contents:
api 10 20
api 18 25
api 26 30
db 5 7
db 9 10
db x y        # invalid
api 40 35     # invalid (start > end)
```

**Output:**
```python
{
  "api": [(10, 30)],
  "db": [(5, 7), (9, 10)]
}
# api:
# (10,20) + (18,25) overlap
# (26,30) adjacent to merged (10,25) since 26 == 25+1
# → merged into (10,30)
#
# db:
# (5,7) and (9,10) neither overlap nor adjacent
```

---

## Task 2 — Total Downtime Seconds

Implement:

```python
total_downtime_seconds(merged: dict) -> dict[str, int]
```

Total downtime per service:

```
sum(end - start + 1)
```

Because intervals are inclusive.

**Note:** Intervals in parameter *merged* are based on your implementation of *merge_downtime* function. (Guarantees sorted order)

---

## Example Runthrough (Total Downtime)

**Input:**
```python
merged = {
  "api": [(10, 30)],
  "db": [(5, 7), (9, 10)]
}
```

**Output:**
```python
{
  "api": 21,
  "db": 5
}
# api: 30 - 10 + 1 = 21
# db: (7 - 5 + 1) + (10 - 9 + 1) = 3 + 2 = 5
```

---

## Notes

- Sorting per service costs O(n log n).
- Merging is O(n).
- Overall complexity dominated by sorting.
- Be careful with:
  - Inclusive interval math (+1)
  - Adjacent detection (end + 1)
  - Ignoring malformed lines