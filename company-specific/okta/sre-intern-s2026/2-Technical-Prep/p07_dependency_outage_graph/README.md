# P07 — Dependency Outage Impact (Graph Traversal + Parsing)

Each non-empty line in the file has the format:

    <serviceA> -> <serviceB>

Meaning:
- `serviceA` depends on `serviceB`.
- If `serviceB` fails, `serviceA` is impacted.
- Impact propagates transitively (dependents of dependents, etc).

Example:

    api -> auth
    auth -> db

If `db` fails → impacted services are: `auth`, `api`

---

## Task 1 — Find Impacted Services

Implement:

```python
impacted_services(filepath: str, failed: str) -> list[str]
```

### Requirements

- Return all services impacted by `failed`
- Do NOT include `failed` itself
- Return results sorted lexicographically
- Ignore invalid lines (must exactly match: `<a> -> <b>` with spaces)
- Services are case-sensitive
- Graph may contain cycles (must not infinite-loop)

---

## Example Runthrough

**Input:**
```python
# file contents:
api -> auth
auth -> db
frontend -> api
invalid_line
auth->db   # invalid (no spaces)

failed = "db"
```

**Output:**
```python
["api", "auth", "frontend"]
# db fails
# auth depends on db
# api depends on auth
# frontend depends on api
# invalid lines ignored
# sorted lexicographically
```

---

## Task 2 — Detect Cycle

Implement:

```python
has_cycle(filepath: str) -> bool
```

Return:
- True if the dependency graph contains ANY cycle
- False otherwise

Must correctly handle:
- Multi-node cycles
- Self-dependency
- Disconnected components

---

## Example Runthrough (Cycle Detection)

**Input:**
```python
# file contents:
api -> auth
auth -> db
db -> api
```

**Output:**
```python
True
# api -> auth -> db -> api forms a cycle
```

---

## Notes

- Build graph as: dependency -> dependents (reverse edges) for impact propagation.
- Use BFS or DFS with a visited set to avoid infinite loops.
- For cycle detection, use:
  - DFS with recursion stack tracking, OR
  - Kahn’s algorithm (topological sort).
- Time complexity: O(V + E)