# D03 — Subscription State Synchronization

**Difficulty:** Medium  
**Target:** 35 minutes

A consumer applies versioned subscription events from an at-least-once stream.
Recent incidents show incorrect behavior after long-lived subscriptions reach
double-digit versions, after cancellation, and when isolated workers are tested
together.

## Contract

- Event dictionaries contain `event_id`, `subscription_id`, integer-string
  `version`, and `type`.
- Supported types are `CREATED`, `PAUSED`, `RESUMED`, and `CANCELED`.
- `CREATED` starts an absent subscription as `ACTIVE`.
- `PAUSED` is valid only from `ACTIVE`; `RESUMED` only from `PAUSED`.
- `CANCELED` is valid from `ACTIVE` or `PAUSED` and is terminal.
- A version applies only when it is numerically greater than the stored version.
- A well-formed event ID is processed at most once, including stale or ignored
  events. Malformed events do not reserve their IDs.
- Each repository instance is isolated.
- Return one of `APPLIED`, `IGNORED`, `STALE`, or `DUPLICATE`; malformed events
  raise `ValueError`.

Run `pytest -q`. Preserve the repository and processor interfaces.

