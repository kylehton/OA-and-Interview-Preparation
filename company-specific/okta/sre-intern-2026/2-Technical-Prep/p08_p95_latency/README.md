# P08 — P95 Latency per Service (Parsing + Percentiles)

File format:

    <service> <latency_ms>

Example:

    auth 10

    auth 20

    auth 30

## Task

Implement:

    p95_latency(filepath: str) -> dict[str, int]

For each service:
- collect valid latencies (integer >= 0)
- compute p95 as the element at index ceil(0.95*n) - 1 when values are sorted ascending
  (this is a common "nearest-rank" definition)
- return int latency value

Invalid lines ignored:
- must have exactly 2 tokens
- latency must be int >= 0

If a service has no valid samples, it should not appear.

## Follow-up
Implement `top_p95_services(filepath, k)` returning list of (service, p95) sorted by:
- p95 desc
- service asc
