# D07 — Payout Calendar Scheduler

**Difficulty:** Hard  
**Target:** 50 minutes

A daily job groups captured transactions into scheduled payouts. Incidents occur
around cutoff boundaries, holidays, offset timestamps, and merchants processing
multiple currencies.

## Contract

Transaction CSV records:

```text
<captured_at_iso8601>,<transaction_id>,<merchant_id>,<currency>,<positive_amount>,<status>
```

- Only `CAPTURED` rows count. Ignore malformed rows.
- Timestamps must include an offset and are evaluated in UTC.
- The first valid occurrence of a transaction ID wins.
- The UTC cutoff is 17:00. A capture at or after the cutoff starts on the next
  calendar date; an earlier capture starts on its UTC date.
- Normalize the starting date forward to a business day, then advance exactly
  `delay_business_days` additional business days.
- Business days exclude Saturday, Sunday, and the supplied ISO-date holidays.
- Group by payout date, merchant, **and currency**.
- Output `date,merchant,currency,amount`, sorted by those first three fields.

`delay_business_days` is non-negative. Use only the standard library. Run
`pytest -q` and preserve `schedule_payouts`.

