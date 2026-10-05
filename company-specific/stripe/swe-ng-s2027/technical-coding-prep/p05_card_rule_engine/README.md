# P05 — Card Rule Engine

**Difficulty:** Medium  
**Target:** 50 minutes  
**Entry point:** `validate_cards(cards, bin_ranges) -> list[str]`

Use Python's `csv` module (or equivalent CSV semantics), not a raw comma split.
Return one CSV-formatted result for every card row, preserving card input order.
Fields containing commas or quotes must be escaped using normal CSV rules.

## Part 1 — Normalize and validate format

Card rows are CSV records:

```text
<payment_id>,<card_number>,<country>
```

Trim fields. Remove ASCII spaces and hyphens from the card number. A formatted
number is valid when the result contains only digits and has length 12–19.
Payment IDs must be non-empty, and country must be exactly two uppercase ASCII
letters.

- A row that is not exactly three CSV fields, or has an empty payment ID,
  returns `ERROR`.
- Other format failures return `<payment_id>,NONE,INVALID_FORMAT`.

## Part 2 — Luhn checksum

Apply the standard Luhn checksum to the normalized number. A failure returns:

```text
<payment_id>,NONE,INVALID_LUHN
```

## Part 3 — BIN-range classification

Range rows are CSV records:

```text
<start_bin>,<end_bin>,<network>,<countries>
```

Both bounds must be six digits with `start_bin <= end_bin`; the network must be
non-empty. The card BIN is its first six digits. `countries` is either `*` or a
`|`-separated list of two-letter uppercase country codes. Ignore invalid ranges.

When a Luhn-valid card has no eligible range, return:

```text
<payment_id>,NONE,UNSUPPORTED
```

Otherwise return `<payment_id>,<network>,VALID`.

## Part 4 — Overlaps and country eligibility

Filter ranges by both BIN and country. If multiple ranges remain, choose the one
with the smallest inclusive numeric span (`end - start`); break an equal-span
tie by earlier input order. A narrower range that excludes the card's country
does not prevent a wider eligible range from matching.

## Example

```python
cards = ["p1,4242-4242-4242-4242,US"]
ranges = [
    "400000,499999,GLOBAL,*",
    "424000,424999,DOMESTIC,US|CA",
]

validate_cards(cards, ranges)
# ["p1,DOMESTIC,VALID"]
```
