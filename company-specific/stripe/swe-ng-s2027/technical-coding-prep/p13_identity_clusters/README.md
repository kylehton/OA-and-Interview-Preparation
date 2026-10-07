# P13 — Time-Bounded Identity Clusters

**Difficulty:** Hard  
**Target:** 60 minutes  
**Entry point:** `analyze_identities(events, risky_users=None, window_seconds=None) -> list[str]`

Use normal CSV parsing and formatting, including quoted fields, and trim parsed
input fields. Event rows are:

```text
<event_id>,<timestamp>,<user_id>,<device_id_or_dash>,<card_id_or_dash>
```

Timestamps are non-negative integers. Event and user IDs must be non-empty. `-`
means an absent identifier; otherwise device and card IDs must be non-empty.
At least one of device or card must be present, and every row must have exactly
five fields. Because `|` separates users in output, a user ID containing `|` is
invalid.

## Part 1 — Shared-device components

When `window_seconds is None`, directly link every pair of users that have ever
used the same non-dash device. Every user from a valid event appears in exactly
one component, including singletons.

Return each component as:

```text
SAFE,<user_1>|<user_2>|...
```

Sort users within a component. Sort component rows by their first user and then
by the complete user list. The joined user list is the second CSV field, so it
must be quoted normally when it contains a comma or quote.

## Part 2 — Cards and transitive closure

Users are also directly linked by a shared non-dash card. Device and card
namespaces are separate. Relationships are transitive across identifier types;
union-find is a natural fit.

## Part 3 — Event idempotency and malformed rows

Event IDs are global. Only the first valid row with an ID is included; invalid
rows do not reserve IDs. Resolve duplicates in event input order. Repeated
events from the same user are harmless.

## Part 4 — Time window and risky propagation

`window_seconds` is either `None` or a non-negative integer. When provided, two
events sharing an identifier create a direct link only if their timestamps
differ by at most the window. Efficiently, sort occurrences for each identifier
and join adjacent users whenever the adjacent gap is within the window.
Transitivity still applies, so a component can span more time than the window.

If any member occurs in `risky_users`, label the entire component `REVIEW`
instead of `SAFE`. Ignore risky users absent from valid events.
Risky-user matching is exact and case-sensitive.

## Example

```python
events = [
    "e1,0,alice,d1,-",
    "e2,5,bob,d1,c2",
    "e3,10,carol,d3,c2",
]

analyze_identities(events, ["carol"], 5)
# ["REVIEW,alice|bob|carol"]
```
