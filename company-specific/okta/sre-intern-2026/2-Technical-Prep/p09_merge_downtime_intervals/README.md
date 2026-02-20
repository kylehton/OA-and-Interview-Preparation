# P09 — Merge Downtime Intervals (Intervals + Sorting)

Input file format per line:

    <service> <start> <end>

Where start and end are integer seconds since epoch.

Intervals are inclusive: [start, end]

Assume start <= end.

## Task

Implement:

    merge_downtime(filepath: str) -> dict[str, list[tuple[int,int]]]

For each service:
- parse valid intervals
- merge overlapping or adjacent intervals:
  - overlap if next.start <= current.end
  - adjacent if next.start == current.end + 1
- return merged intervals sorted by start ascending

Invalid lines ignored:
- must have 3 tokens
- start/end must be ints
- start <= end

## Follow-up
Implement:

    total_downtime_seconds(merged: dict) -> dict[str, int]

Total downtime per service = sum(end-start+1).
