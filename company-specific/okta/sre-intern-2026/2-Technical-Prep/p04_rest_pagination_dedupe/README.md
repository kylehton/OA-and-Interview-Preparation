# P04 — REST Pagination + Deduplication (Practical SRE Coding)

You are given a `fetch_page(page_token)` function (provided by tests) that returns:

    {
      "items": [ { "id": str, ... }, ... ],
      "next": str | None
    }

    NOTE: "id" does not denote the field for a unique id. It directly corresponds to the item id.
    No item value/content is provided, only a dictionary of the ids of items for the page.

Rules:
- Start by calling `fetch_page(None)` (first page).
- Continue calling with the returned `"next"` token until it is None.
- The API may return duplicate items across pages (same "id").

## Task

Implement:

    fetch_all_items(fetch_page) -> list[dict]

Return **deduplicated** items by id, keeping the **first occurrence** of each id,
preserving original encounter order across pages.

## Follow-up
Implement:

    fetch_all_ids(fetch_page) -> list[str]

Same traversal but return ids only (deduped, first occurrence order).

## Constraints
- Must not loop forever if API returns a previously seen token (cycle).

  If a token repeats, stop and raise ValueError("pagination cycle").
