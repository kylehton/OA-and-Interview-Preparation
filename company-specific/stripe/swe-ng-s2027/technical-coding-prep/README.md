# Stripe-Style HackerRank OA Practice

This set contains 15 **original** implementation problems modeled on the format
described in public reports about Stripe software-engineering online assessments.
It is not a collection of leaked or copied assessment questions.

## What the research suggests

Recent candidate reports consistently describe:

- one main problem in roughly 60 minutes;
- three to five cumulative parts rather than unrelated LeetCode questions;
- string parsing, dictionaries/sets, state machines, and simulation;
- later requirements that stress whether the Part 1 design is extensible;
- careful invalid-operation handling and deterministic output formatting; and
- code quality and edge cases mattering alongside test-case count.

The practice set therefore gives every problem one public entry point that must
continue to support all earlier behavior as later parts are added.

Research references:

- [New-grad report: one three-part parsing problem](https://leetcode.com/discuss/post/7285521/)
- [University recruiting report: state, transitions, and defensive handling](https://leetcode.com/discuss/post/7428741/stripe-university-recruiting-oa-online-a-iicb/)
- [Backend report: registry, routing, persistent capacity, and edge cases](https://www.reddit.com/r/leetcode/comments/1scjqoq/stripe_oa_backend/)
- [Intern report: fraud-monitoring simulation](https://leetcode.com/discuss/post/7344444/)
- [Candidate discussion of four/five cumulative parts](https://www.reddit.com/r/leetcode/comments/1qs7o3t/just_completed_stripe_oa_jesus_christ_it_was_hard/)

## Recommended order

| Order | Problem | Difficulty | Target | Main skills |
|---:|---|---|---:|---|
| 1 | [Checkout Quote](p01_checkout_quote/) | Easy | 35 min | parsing, aggregation, integer money math |
| 2 | [Wallet Commands](p02_wallet_commands/) | Easy | 40 min | command dispatch, idempotency, reversals |
| 3 | [Payout Batches](p03_payout_batches/) | Easy–Medium | 45 min | event joins, refunds, deterministic batching |
| 4 | [API-Key Limiter](p04_api_key_limiter/) | Easy–Medium | 45 min | rolling windows, mutable configuration |
| 5 | [Card Rule Engine](p05_card_rule_engine/) | Medium | 50 min | normalization, Luhn, interval selection |
| 6 | [Invoice Lifecycle](p06_invoice_lifecycle/) | Medium | 50 min | state machine, partial payments/refunds |
| 7 | [Webhook Retries](p07_webhook_retries/) | Medium | 50 min | grouping, backoff, terminal states |
| 8 | [Reconciliation Join](p08_reconciliation_join/) | Medium | 50 min | CSV parsing, matching, one-to-one joins |
| 9 | [Subscription Billing](p09_subscription_billing/) | Medium | 55 min | interval boundaries, dedupe, proration |
| 10 | [FX Ledger](p10_fx_ledger/) | Medium | 55 min | time-versioned data, exact rounding |
| 11 | [Risk Monitor](p11_risk_monitor/) | Medium–Hard | 60 min | policy modes, reversible events, ratios |
| 12 | [Regional Router](p12_regional_router/) | Hard | 60 min | graphs, shortest paths, persistent capacity |
| 13 | [Identity Clusters](p13_identity_clusters/) | Hard | 60 min | union-find, time-window relationships |
| 14 | [Reserve Settlements](p14_reserve_settlements/) | Hard | 70 min | scheduled state, refunds, reserves |
| 15 | [Marketplace Split Ledger](p15_marketplace_split_ledger/) | Hard | 70 min | atomic multi-entity transitions |

Problems 1–4 establish speed and reliable parsing. Problems 5–10 add richer
state and boundary conditions. Problems 11–15 are full mock assessments; do
them only after you can finish the earlier medium problems without rewriting
your core model between parts.

## Folder contract

Every problem folder contains:

- `README.md` — the complete, progressively revealed specification;
- `solution.py` — the only file you need to implement; and
- `tests/test_solution.py` — public tests grouped by part.

The starter functions deliberately raise `NotImplementedError`. A fully solved
problem passes every test in its folder.

## Strict practice mode

1. Open only the problem `README.md` and `solution.py`.
2. Set the listed timer.
3. Read all four parts before coding; reserve about 10 minutes for the final part.
4. Keep parsing, validation, state mutation, and output formatting separate.
5. From the selected problem folder, run one part at a time when you are ready:

   ```bash
   pytest -q -k part_1
   pytest -q -k part_2
   pytest -q -k part_3
   pytest -q -k part_4
   ```

6. Finish with the entire folder:

   ```bash
   pytest -q
   ```

For a realistic final week, do P11–P15 from a blank editor with a 60-minute
cap, even where the suggested learning-time target is longer.

## General assumptions

- Python 3.10+ and `pytest` are expected.
- Money values are integer minor units (for example, cents); never use floats.
- Input order matters unless a problem explicitly defines another ordering.
- Malformed input must not partially mutate state.
- Sorting and tie-break rules are part of correctness.
