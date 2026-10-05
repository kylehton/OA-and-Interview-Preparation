# P09 — Subscription Usage Billing

**Difficulty:** Medium  
**Target:** 55 minutes  
**Entry point:** `generate_invoices(plans, subscriptions, usage, period_start, period_end) -> list[str]`

All inputs are comma-separated with trimmed fields. Days and billing intervals
are integer and inclusive. Return `[]` when `period_end < period_start`.

## Part 1 — Base subscription charge

Plan rows:

```text
<plan_id>,<period_fee>,<included_units>,<overage_price_per_unit>
```

The ID must be non-empty and all numeric fields must be non-negative integers.
The first valid plan row for an ID wins.

Subscription rows:

```text
<subscription_id>,<customer_id>,<plan_id>,<start_day>,<end_day_or_dash>
```

IDs must be non-empty, the plan must exist, and a numeric end must be at least
the start. `-` means no end. The first valid subscription ID wins. Return a row
for every subscription that overlaps the billing period, sorted by subscription
ID:

```text
<subscription_id>,<customer_id>,<active_days>,<usage_units>,<amount>
```

## Part 2 — Metered overage

Usage rows:

```text
<day>,<event_id>,<subscription_id>,<positive_units>
```

Count usage only when its day is inside both the subscription lifetime and the
billing period. For a full-period subscription:

```python
amount = period_fee + max(0, usage - included_units) * overage_price_per_unit
```

## Part 3 — Idempotency and validity

Event IDs are globally unique among valid events. The first valid event reserves
its ID even when it falls outside the current billing period. A row is valid
when it is well formed, references a known subscription, and its day is inside
that subscription's lifetime. Invalid rows do not reserve IDs.

## Part 4 — Inclusive proration

Let `period_days = period_end - period_start + 1`, and let `active_days` be the
size of the subscription/period intersection. Prorate independently with floor
division:

```python
base = period_fee * active_days // period_days
included = included_units * active_days // period_days
amount = base + max(0, usage - included) * overage_price_per_unit
```

## Example

```python
plans = ["pro,3000,300,2"]
subscriptions = ["s1,c1,pro,11,20"]
usage = ["12,u1,s1,150"]

generate_invoices(plans, subscriptions, usage, 1, 30)
# ["s1,c1,10,150,1100"]
```

