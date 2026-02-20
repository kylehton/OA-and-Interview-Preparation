# P07 — Dependency Outage Impact (Graph Traversal + Parsing)

File format: each non-empty line is:

    <serviceA> -> <serviceB>

Meaning: serviceA depends on serviceB.

If serviceB is down, serviceA is impacted (and any services that depend on serviceA, etc).

Example:

    api -> auth

    auth -> db

If db fails, impacted are: auth, api

## Task

Implement:

    impacted_services(filepath: str, failed: str) -> list[str]

Return all impacted services (excluding `failed`) sorted lexicographically.

Rules:
- Ignore invalid lines (must match pattern "<a> -> <b>" with tokens separated by spaces)
- Services are case-sensitive.
- Graph may contain cycles. Must not infinite-loop.

## Follow-up
Implement:

    has_cycle(filepath: str) -> bool

Return True if dependency graph contains any cycle.
