# P04 — REST Pagination + Deduplication (Practical SRE Coding)

You are given a function:

```python
fetch_page(page_token)
```

It returns:

```python
{
  "items": [ {"id": str}, ... ],
  "next": str | None
}
```

Notes:
- `"id"` is the unique identifier for each item.
- Items may repeat across pages.
- Pages are traversed using `"next"` tokens.

---

## Task 1 — Fetch All Items (Deduplicated)

Implement:

```python
fetch_all_items(fetch_page) -> list[dict]
```

### Rules

- Start with:

  ```
  fetch_page(None)
  ```

- Continue calling `fetch_page(next_token)` until `"next"` is `None`
- Deduplicate items by `"id"`
- Keep the **first occurrence**
- Preserve original encounter order across pages
- If a `"next"` token repeats (pagination cycle):
  - Stop and raise:

    ```
    ValueError("pagination cycle")
    ```

---

## Example Runthrough

**Input:**
```python
pages = {
    None: {
        "items": [{"id": "a"}, {"id": "b"}],
        "next": "t1"
    },
    "t1": {
        "items": [{"id": "b"}, {"id": "c"}],
        "next": None
    }
}
```

**Output:**
```python
[
    {"id": "a"},
    {"id": "b"},
    {"id": "c"}
]
# b appears twice, first occurrence kept
# traversal order preserved
```

---

## Task 2 — Fetch All IDs Only

Implement:

```python
fetch_all_ids(fetch_page) -> list[str]
```

### Rules

- Same traversal logic
- Deduplicate by id
- Return list of ids (first occurrence order)

---

## Example Runthrough (IDs Only)

**Input:**
```python
# same pages as above
```

**Output:**
```python
["a", "b", "c"]
```

---

## Notes

- Maintain:
  - `seen_ids = set()`
  - `seen_tokens = set()`
- For cycle detection:
  - If a token has already been used → raise ValueError
- Complexity:
  - O(total_items)
  - Memory O(unique_ids + visited_tokens)
- Order preservation achieved by appending only when id not seen.