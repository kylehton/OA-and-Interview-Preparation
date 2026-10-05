# P04 — Mutable API-Key Rate Limiter

**Difficulty:** Easy–Medium  
**Target:** 45 minutes  
**Entry point:** `evaluate_requests(commands) -> list[str]`

Process whitespace-separated commands in order and return one response for each
command. All time-bearing commands are guaranteed to have non-decreasing
timestamps globally. Invalid commands return `ERROR` without changing state.

## Part 1 — Register keys

```text
REGISTER <key_id> <limit> <window_seconds>
```

Both numeric values must be positive integers, and key IDs must be unique.
Return `OK` or `ERROR`.

## Part 2 — Sliding-window requests

```text
REQUEST <timestamp> <request_id> <key_id>
```

For a key with limit `L` and window `W`, a request at `T` is allowed when fewer
than `L` accepted requests fall in the inclusive window `[T-W+1, T]`.

- Return `ALLOW` and record an accepted request.
- Return `DENY` without recording a rejected request.
- Unknown keys and negative timestamps return `ERROR`.

## Part 3 — Idempotency and status

The first `ALLOW` or `DENY` for a request ID is cached globally. A later
syntactically valid `REQUEST` using that ID returns the cached decision and does
not add a timestamp, even if other fields differ. An `ERROR` is not cached.

```text
STATUS <timestamp> <key_id>
```

Return `<accepted_in_current_window>/<limit>`. Status queries do not consume
capacity.

## Part 4 — Live configuration

```text
SET <key_id> <new_limit> <new_window_seconds>
```

Positive values replace the key's configuration and return `OK`. Preserve the
complete accepted-request history: requests falling inside the new window count
even if they were outside the old one. This means a status may temporarily show
usage above the new limit.

## Example

```python
evaluate_requests([
    "REGISTER live 2 3",
    "REQUEST 10 r1 live",
    "REQUEST 11 r2 live",
    "REQUEST 12 r3 live",
    "STATUS 12 live",
    "REQUEST 13 r4 live",
])
# ["OK", "ALLOW", "ALLOW", "DENY", "2/2", "ALLOW"]
```

