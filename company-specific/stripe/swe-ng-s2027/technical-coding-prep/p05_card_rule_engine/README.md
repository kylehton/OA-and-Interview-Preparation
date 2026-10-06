# P05 — Card Validation Router

**Difficulty:** Medium  
**Target:** 50 minutes  
**Entry point:** `validate_cards(cards, bin_ranges) -> list[str]`

Build this function in four cumulative parts. Each part introduces one new
decision layer. In particular, Parts 1 and 2 are validation-only: they do not
parse BIN ranges and do not produce a network.

Use Python's `csv` module (or equivalent CSV semantics), not a raw comma split.
Return one CSV-formatted response for every card row, preserving card input
order. Use normal CSV escaping for output fields containing commas or quotes.

Assume payment IDs are unique in well-formed input. This exercise does not ask
you to store payments, check duplicate IDs, or retain state between calls.

## Part 1 — Parse, normalize, and validate

For Part 1, call the function with `bin_ranges=[]`. Do not inspect or implement
range behavior yet.

Each card row describes one payment attempt using one card:

```text
<payment_id>,<card_number>,<country>
```

Trim surrounding whitespace from every CSV field. In `card_number`, also remove
every ASCII space and hyphen. For example:

```text
4242-4242 4242-4242  ->  4242424242424242
```

A normalized row is valid when:

- `payment_id` is non-empty;
- `card_number` contains only the ASCII digits `0` through `9` and has length
  from 12 through 19 inclusive; and
- `country` contains exactly two uppercase ASCII letters `A` through `Z`.

Country is an input check. Trim it, but do not uppercase, truncate, pad, or
otherwise repair it. `US` and ` US ` are valid shapes; `us`, `U`, `USA`, and
`ÉU` are invalid. You do not need a real country registry, so `ZZ` is valid.
Part 4 will use this already-validated field for routing.

Return exactly one of these rows:

| Condition | Response |
|---|---|
| Row does not have exactly three CSV fields | `ERROR` |
| Payment ID is empty after trimming | `ERROR` |
| Card number or country has an invalid format | `<payment_id>,NONE,INVALID_FORMAT` |
| All Part 1 checks pass | `<payment_id>,NONE,VALID` |

Part 1 does not return the normalized card number or country, and it does not
mention a network.

Example:

```python
validate_cards(
    ["pay_1,4242-4242-4242-4242,US", "pay_2,123,US"],
    [],
)
# ["pay_1,NONE,VALID", "pay_2,NONE,INVALID_FORMAT"]
```

## Part 2 — Luhn checksum

Continue calling the function with `bin_ranges=[]`. After a card passes Part 1,
apply the Luhn checksum to its normalized number:

1. Walk from the rightmost digit to the left.
2. Leave the rightmost digit unchanged, then double every second digit.
3. If a doubled value is greater than `9`, subtract `9`.
4. Add all resulting values.
5. The number passes when the sum is divisible by `10`.

Equivalently, while iterating over `reversed(number)`, double digits at odd
zero-based indexes. `4242424242424242` passes and `4242424242424241` fails.

Part 1 errors still take precedence. A format-valid card that fails Luhn
returns:

```text
<payment_id>,NONE,INVALID_LUHN
```

A card that passes Luhn keeps the Part 1 success response:

```text
<payment_id>,NONE,VALID
```

## Part 3 — BIN routing

Part 3 introduces `bin_ranges`. A **BIN** is the first six digits of the
normalized card number. In this exercise, a BIN range maps those leading digits
to a processing-network label.

A **card network** is the payment route used to carry a card transaction. Visa
and Mastercard are familiar examples, but this problem uses whatever label is
provided by the input rule; no external list of networks is required.

Part 3 range rows have exactly three CSV fields:

```text
<start_bin>,<end_bin>,<network>
```

A range is valid when both bounds contain exactly six ASCII digits,
`start_bin <= end_bin`, and the trimmed network is non-empty. Ignore invalid
range rows. For Part 3 inputs, assume valid ranges do not overlap.

When `bin_ranges` is non-empty, routing mode is enabled:

- a Luhn-valid card whose BIN falls within a valid range, including either
  boundary, returns `<payment_id>,<network>,VALID`;
- a Luhn-valid card with no matching valid range returns
  `<payment_id>,NONE,UNSUPPORTED`.

An empty `bin_ranges` list continues to mean validation-only mode and retains
the Part 2 behavior. A non-empty list containing only invalid rules is still
routing mode, so a valid card is `UNSUPPORTED`.

The selected network is the trimmed label from the matching rule. Preserve its
case and punctuation and apply normal CSV quoting in the response.

Example:

```python
validate_cards(
    ["pay_1,4242424242424242,US"],
    ["400000,499999,VISA"],
)
# ["pay_1,VISA,VALID"]
```

## Part 4 — Country restrictions and overlapping ranges

Part 4 adds an optional fourth range field:

```text
<start_bin>,<end_bin>,<network>,<countries>
```

Three-field Part 3 rules remain valid and apply to every valid country. For a
four-field rule, `countries` must be either:

- `*`, meaning every valid country; or
- a `|`-separated list such as `US|CA`.

Trim each country token. Every token must contain exactly two uppercase ASCII
letters. If any token is invalid, ignore the entire range. Matching uses exact
equality; never uppercase or truncate a value.

First filter rules by both BIN and country. If several eligible rules remain,
select the rule with the smallest numeric span:

```python
span = end_bin - start_bin
```

Break an equal-span tie by earlier range input order. A narrower rule that
excludes the card's country does not block a wider eligible rule.

Example:

```python
cards = ["pay_1,4242424242424242,US"]
ranges = [
    "400000,499999,GLOBAL",
    "424000,424999,DOMESTIC,US|CA",
]

validate_cards(cards, ranges)
# ["pay_1,DOMESTIC,VALID"]
```

## Final decision order

For every card row, stop at the first terminal result:

```text
bad row structure or empty payment ID -> ERROR
invalid card/country format           -> INVALID_FORMAT
failed Luhn checksum                  -> INVALID_LUHN
validation-only mode                  -> NONE,VALID
no eligible routing rule              -> NONE,UNSUPPORTED
eligible routing rule                 -> <network>,VALID
```
