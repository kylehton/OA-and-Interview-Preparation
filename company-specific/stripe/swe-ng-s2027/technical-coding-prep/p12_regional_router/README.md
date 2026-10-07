# P12 — Capacity-Aware Regional Router

**Difficulty:** Hard  
**Target:** 60 minutes  
**Entry point:** `route_requests(commands) -> list[str]`

Process whitespace-separated commands in order and return one response per
command. Commands must have exactly the shown arity and all IDs must be
non-empty. Invalid commands return `ERROR` without changing state.

Region IDs may not contain `,` or `>` because those characters delimit the
route response and its path. Request IDs have no additional character rule.

## Part 1 — Region registry and health

```text
ADD <region> <positive_capacity>
HEALTH <region> <UP|DOWN>
```

Region IDs are unique. New regions start `UP` with load `0`. Both commands
return `OK` on success.

## Part 2 — Network and shortest-path routing

```text
LINK <region_a> <region_b> <positive_latency>
ROUTE <request_id> <origin_region>
```

Links are undirected. Both distinct regions must exist. A later valid `LINK` for
the same pair replaces its latency. An invalid replacement leaves the existing
link unchanged.

A destination is eligible when it is `UP`, has `load < capacity`, and is
reachable from the known origin. The origin itself is reachable at latency `0`.
Health restricts destinations, not traversal: paths may pass through a `DOWN`
region. Choose by:

1. smallest total latency;
2. destination ID lexicographically;
3. full path sequence lexicographically.

Return `<destination>,<latency>,<path>` where path nodes are joined by `>`.
Return `NONE` if no destination is eligible.

## Part 3 — Persistent capacity and idempotency

A successful route increments its destination load by one. The first valid
`ROUTE` response for a request ID—including `NONE`—is cached. A repeated request
ID returns its cached response and never changes load, even if the origin differs.
An `ERROR` does not reserve the ID.

Changing a region's health does not reset its load. Existing routed requests
continue occupying capacity until released.

## Part 4 — Release and tie handling

```text
RELEASE <request_id>
```

Release succeeds exactly once for a request that routed successfully, reducing
its destination load. It returns `OK`; unknown, `NONE`, or already released
requests return `ERROR`. Replaying the original route after release still
returns its cached result without reclaiming capacity.

Use Dijkstra's algorithm or an equivalent shortest-path method. A linear scan
over regions after computing distances is sufficient.
