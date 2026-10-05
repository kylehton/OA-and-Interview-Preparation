# P03 — Payout Batches

**Difficulty:** Easy–Medium  
**Target:** 45 minutes  
**Entry point:** `create_payout_batches(events, minimum_amount=0, max_batch_amount=0) -> list[str]`

Parse comma-separated event rows. Whitespace around fields is insignificant.

## Part 1 — Aggregate payments

```text
PAYMENT,<event_id>,<merchant_id>,<currency>,<positive_amount>
```

Aggregate payment amounts by `(merchant_id, currency)`. IDs must be non-empty.
A currency is valid only when it is exactly three uppercase ASCII letters.

Return payout rows in merchant-then-currency lexicographic order:

```text
<merchant_id>,<currency>,<batch_number>,<amount>
```

Batch numbers start at `1` independently for each merchant/currency group.

## Part 2 — Idempotency and malformed input

Event IDs are globally unique across all event types. Only the first successful
event using an ID is applied. Ignore malformed or invalid events; an ignored
event does not reserve its ID.

## Part 3 — Partial refunds

```text
REFUND,<event_id>,<payment_event_id>,<positive_amount>
```

A refund inherits the referenced payment's merchant and currency. It is valid
only if the payment exists and total successful refunds against that payment do
not exceed the original amount. Subtract valid refunds from the payout group.

## Part 4 — Thresholds and splitting

Include a positive net group only when its amount is at least
`minimum_amount`. Treat a negative minimum as `0`.

When `max_batch_amount > 0`, greedily split each included group into the fewest
batches no larger than the maximum: full-size batches first, then a remainder.
When the maximum is `0` or negative, return one batch per group.

## Example

```python
events = [
    "PAYMENT,p1,m1,USD,250",
    "PAYMENT,p2,m1,USD,75",
    "REFUND,r1,p1,25",
]

create_payout_batches(events, minimum_amount=100, max_batch_amount=125)
# ["m1,USD,1,125", "m1,USD,2,125", "m1,USD,3,50"]
```

