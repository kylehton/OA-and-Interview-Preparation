# D06 — Historical FX Quote Cache

**Difficulty:** Medium–Hard  
**Target:** 45 minutes

The quote service stores versioned rational exchange rates. Customers report
wrong quotes exactly when a new rate becomes active, when converting through a
reverse pair, and after requesting more than one quote from the same service.

## Contract

- `RateBook.add_rate(source, target, timestamp, numerator, denominator)` stores
  a positive rational rate at a non-negative integer timestamp.
- Rates may be inserted out of timestamp order.
- A quote uses the rate with the greatest timestamp **at or before** `at`.
- A direct pair is preferred. When absent, invert the newest eligible reverse
  pair.
- Conversion uses integer floor arithmetic.
- `QuoteService.convert` raises `LookupError` when neither direction exists.
- Cached results must be specific to every input affecting the answer.
- Rates can be added after the service is constructed; subsequent calls must
  observe the current rate book.

Run `pytest -q`. Preserve exact rational arithmetic and public APIs.

