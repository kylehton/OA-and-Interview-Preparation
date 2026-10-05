# D05 — Payment API Client Retry Safety

**Difficulty:** Medium–Hard  
**Target:** 45 minutes

An internal client occasionally creates unsafe retry traffic. Telemetry also
shows more network calls than its configured attempt limit, and a caller has
reported that its request dictionary changed after the call returned.

## Contract

`PaymentClient.create_payment(payload)` posts to `/payments` and returns the
response body's payment `id`.

- Any `2xx` response is success.
- `429`, `5xx`, and `TimeoutError` are retryable.
- Other responses immediately raise `PaymentError`.
- `max_attempts` is the total number of HTTP calls.
- One idempotency key is generated per logical `create_payment` invocation and
  reused for every retry.
- Every HTTP attempt receives equivalent payload data.
- The caller's payload must never be mutated.
- Retry delays use `base_delay * 2**attempt_index`; a numeric `Retry-After` on
  `429` is a minimum delay.
- Exhaustion raises `PaymentError`.

The injected transport, sleeper, and key factory make behavior deterministic.
Run `pytest -q`; do not replace them or change the public interface.

