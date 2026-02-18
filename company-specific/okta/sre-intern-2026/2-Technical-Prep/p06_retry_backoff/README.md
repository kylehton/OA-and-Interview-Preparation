# P06 — Retry with Exponential Backoff (Practical + Testing)

Implement:

    retry(operation, retries: int, base_delay: float, sleep_fn=time.sleep)

Behavior:
- Call operation().
- If it succeeds, return its value.
- If it raises an Exception:
  - if no retries left, re-raise the last exception
  - otherwise sleep for base_delay * (2 ** attempt_index)
    where attempt_index starts at 0 for the first failure
  - then try again

Example: retries=3
- Up to 1 initial try + 3 retries = 4 total attempts.

## Follow-up: Jitter

Implement:

    retry_with_jitter(operation, retries, base_delay, jitter_fn, sleep_fn)

Where delay is:
    base_delay * (2 ** attempt_index) + jitter_fn()
jitter_fn returns a float (can be 0).

## Notes
- Tests will pass a fake sleep_fn so you must use it.
