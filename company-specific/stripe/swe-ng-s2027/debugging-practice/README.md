# Stripe-Style Bug Squash Practice

This track contains eight **original, intentionally broken** Python mini-projects.
Each one resembles a small production codebase: the implementation mostly
works, several tests pass, and a few independent regressions must be localized
and fixed without rewriting the system.

Do not treat these as algorithm questions. The objective is to demonstrate a
repeatable debugging process in unfamiliar code.

## Research basis

Public candidate reports describe a roughly 45–60 minute Bug Squash round using
a real, unfamiliar codebase and its unit tests. Reports emphasize reproducing a
failure, narrowing it with the debugger, making a targeted change, and explaining
the evidence and root cause. Python candidates have reported established
open-source libraries, including template engines; exact repositories and rules
vary by interview.

- [Backend candidate report describing a template-library debug round](https://leetcode.com/discuss/post/7595344/)
- [New-grad report describing a large unfamiliar codebase](https://leetcode.com/discuss/post/7566910/)
- [Candidate report describing a 45-minute real-project debugging round](https://leetcode.com/discuss/post/1340172/stripe-no-offer/)
- [MLE report describing two bugs and documentation access](https://leetcode.com/discuss/post/5984403/Stripe-Sr.-MLE-onsite-Sept-2024/)

These exercises reproduce the skills and working style, not any proprietary
interview repository or bug.

## Recommended order

| Order | Project | Difficulty | Target | System under test |
|---:|---|---|---:|---|
| 1 | [Webhook Delivery](d01_webhook_delivery/) | Easy | 25 min | retries and idempotency |
| 2 | [Checkout Pricing](d02_checkout_pricing/) | Easy–Medium | 30 min | discounts, tax, quote cache |
| 3 | [Subscription Sync](d03_subscription_sync/) | Medium | 35 min | versioned event state machine |
| 4 | [Reconciliation](d04_reconciliation/) | Medium | 40 min | CSV parsing and one-to-one matching |
| 5 | [Payment Client](d05_payment_client/) | Medium–Hard | 45 min | API retries and request safety |
| 6 | [FX Quotes](d06_fx_quotes/) | Medium–Hard | 45 min | historical rates and memoization |
| 7 | [Payout Scheduler](d07_payout_scheduler/) | Hard | 50 min | UTC cutoffs and business calendars |
| 8 | [Template Renderer](d08_template_renderer/) | Hard | 55 min | parsing, includes, escaping, caching |

## Interview mode

For each project:

1. Read only that project's `README.md`.
2. Start a timer and run `pytest -q` to reproduce the baseline.
3. Pick one failure and run only that test with `pytest -q path::test_name`.
4. Read outward from the failing assertion. State a hypothesis before editing.
5. Use breakpoints, stepping, watches, and focused test runs. Tests are meant to
   be read; do not edit them.
6. Make the smallest defensible production-code change.
7. Run the focused test, related module tests, then the whole suite.
8. Explain the root cause, why the fix is safe, and one regression test you
   would add if it were missing.

Use [DEBUGGING_NOTES_TEMPLATE.md](DEBUGGING_NOTES_TEMPLATE.md) to practice
thinking aloud in writing. Documentation lookup is encouraged; confirm the
rules for external tools with your recruiter for the real interview.

## Running the exercises

From one project folder:

```bash
pytest -q
```

From this directory, all projects can be collected or run together:

```bash
pytest --collect-only -q
pytest -q
```

The initial full run is expected to fail. There is deliberately no answer key
or fixed implementation in this directory.

## Ground rules

- Fix production code, not tests.
- Preserve public interfaces unless the issue explicitly permits a change.
- Avoid broad rewrites and new dependencies.
- A passing focused test is not completion; check for regressions.
- Keep a clean explanation of each change. Silent trial-and-error misses much of
  the skill this track is designed to build.

