# P02 — Top-K IPs (Heap + File I/O)

Log file format (one request per line):

    <timestamp> <ip> <endpoint>

Example:

    2026-02-17T10:00:00 10.0.0.1 /login

---

## Task — Top K IP Addresses

Implement:

```python
top_k_ips(filepath: str, k: int) -> list[str]
```

### Rules

- Count frequency of valid IP addresses.
- Return top `k` IPs sorted by:
  1. frequency descending  
  2. ip lexicographically ascending (tie-break)

If `k` > number of unique IPs → return all unique IPs sorted by the same rules.

### Validity

Ignore lines that:

- Do not split into exactly 3 tokens
- Have empty IP token

Process file line-by-line (large file safe).

Use a heap (or `heapq.nlargest`) for top-k selection.

---

## Example Runthrough

**Input:**
```python
# file contents:
2026-02-17T10:00:00 1.1.1.1 /a
2026-02-17T10:00:01 2.2.2.2 /b
2026-02-17T10:00:02 1.1.1.1 /c
2026-02-17T10:00:03 3.3.3.3 /d
2026-02-17T10:00:04 1.1.1.1 /e
2026-02-17T10:00:05 2.2.2.2 /f
bad line

k = 2
```

**Output:**
```python
["1.1.1.1", "2.2.2.2"]
# counts:
# 1.1.1.1 → 3
# 2.2.2.2 → 2
# 3.3.3.3 → 1
# sorted by frequency desc, ip asc
```

---

## Notes

- Use a dictionary: `{ ip: count }`
- Sorting rule equivalent to:
  ```
  key = (-count, ip)
  ```
- Time complexity:
  - Counting → O(n)
  - Top-k using heap → O(m log k)
    where m = number of unique IPs
- Memory: O(#unique_ips)