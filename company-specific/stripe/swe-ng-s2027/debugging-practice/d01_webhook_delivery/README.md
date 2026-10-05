# D01 — Webhook Delivery Regressions

**Difficulty:** Easy  
**Target:** 25 minutes

The webhook worker recently changed its retry behavior. Operations reports that:

- some endpoints acknowledge an event but the worker still reports failure;
- rate-limited deliveries are not retried as expected; and
- an event can become permanently suppressed even though every delivery failed.

The rest of the service is behaving normally.

## Contract

- Any HTTP status from `200` through `299` is success.
- `429` and `5xx` responses are retryable.
- Other `4xx` responses are terminal for that call.
- Exponential delays are `base_delay * 2**attempt_index`, starting at index `0`.
- A numeric `Retry-After` on `429` is a minimum delay.
- `max_attempts` is the total number of sender calls, not the number of retries.
- Only successful events enter the processed-event store.
- Re-delivering a successfully processed event returns `DUPLICATE` without a
  sender call.

Run:

```bash
pytest -q
```

Do not change the sender, store interface, result types, or tests.

