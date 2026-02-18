# P10 — Unique Users (Streaming + Memory Awareness)

File contains one event per line:

    <timestamp> <user_id> <event>

Example:
    2026-02-17T10:00:00 u1 login

## Task

Implement:

    count_unique_users(filepath: str) -> int

Return number of unique user_ids in valid lines.

Validity:
- exactly 3 tokens
- user_id token non-empty

Constraints:
- stream line-by-line
- O(unique_users) memory is OK
- ignore invalid lines

## Follow-up (harder)
Implement:

    top_active_users(filepath: str, k: int) -> list[tuple[str,int]]

Count events per user_id and return top k users sorted by:
- count desc
- user_id asc
