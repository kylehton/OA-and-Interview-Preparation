# P02 — Top-K IPs (Heap + File I/O)

Log file format (one request per line):

    <timestamp> <ip> <endpoint>

Example:
    2026-02-17T10:00:00 10.0.0.1 /login

## Task

Implement:

    top_k_ips(filepath: str, k: int) -> list[str]

Return the top `k` most frequent IP addresses.

### Tie-breaking
Sort by:
1) frequency descending
2) ip lexicographically ascending

If `k` > number of unique IPs, return all unique IPs sorted by above rules.

### Validity
Ignore lines that:
- don't split into exactly 3 tokens
- have empty IP token

### Constraints
- Process file line-by-line.
- Use a heap (or nlargest) for top-k selection.
