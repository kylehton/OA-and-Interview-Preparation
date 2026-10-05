# D02 — Checkout Pricing Drift

**Difficulty:** Easy–Medium  
**Target:** 30 minutes

Support reports that some repeated quotes change unexpectedly, and finance has
found occasional one-cent discrepancies when discounts and tax are combined.

## Contract

`QuoteEngine.quote` receives cart lines plus optional percentage and bulk rules.

- All values are integer cents or basis points.
- Combine repeated SKUs before pricing.
- For each SKU, compare the base line total, its percentage-discounted line
  total, and an applicable bulk-price line total; use the lowest.
- Percentage arithmetic occurs once on the complete line total.
- Tax is calculated on the discounted subtotal with floor division.
- A quote is pure: inputs are not mutated, and a previous quote must not affect
  a later quote.
- The returned `subtotal` is before discount; `discount` is the amount removed;
  `tax` is tax on the discounted subtotal; and `total = subtotal-discount+tax`.

Run `pytest -q`. Preserve the public dataclasses and method signature.

