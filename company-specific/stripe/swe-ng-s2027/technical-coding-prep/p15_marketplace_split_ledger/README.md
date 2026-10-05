# P15 — Marketplace Split Ledger

**Difficulty:** Hard  
**Target:** 70 minutes  
**Entry point:** `process_marketplace(commands) -> list[str]`

Process whitespace-separated commands in order and return one response per
command. Amounts are positive integer minor units. Invalid operations return
`ERROR` and must be atomic.

## Part 1 — Draft, split, and capture

```text
ACCOUNT <account_id>
CREATE <payment_id> <positive_amount>
SPLIT <payment_id> <account_id> <positive_amount>
CAPTURE <payment_id>
BALANCE <account_id>
```

Account and payment IDs are unique within their own namespaces. A new payment is
`DRAFT`. Each account may have at most one split on a payment, and the running
split total may not exceed the payment amount. Capture succeeds exactly once
when splits total the full payment amount, credits each recipient, and changes
the payment to `CAPTURED`.

## Part 2 — Payouts

```text
PAYOUT <operation_id> <account_id> <positive_amount>
```

A payout debits an account only when funds are sufficient. Successful payout,
refund, and dispute operation IDs share a global namespace. Failed operations
do not reserve IDs.

## Part 3 — Atomic refunds

```text
REFUND <operation_id> <payment_id> <positive_amount>
```

The amount may not exceed the payment's remaining captured amount. Allocate the
debit across that payment's remaining splits in **reverse SPLIT input order**,
exhausting each allocation before moving backward. Every affected account must
have enough current balance for its allocated debit. Validate all accounts
first, then apply the refund atomically.

## Part 4 — Disputes and status

```text
DISPUTE <operation_id> <payment_id> <positive_amount>
STATUS <payment_id>
```

A dispute uses the same reverse-order allocation and remaining-amount rules, but
it may drive recipient balances negative. Refunds and disputes both permanently
reduce the remaining allocation.

Status returns `<state>,<original_amount>,<remaining_amount>`, where state is:

- `DRAFT` before capture;
- `CAPTURED` immediately after capture;
- `PARTIAL` after any non-total refund or dispute;
- `REFUNDED` at zero when every deduction was a refund; or
- `DISPUTED` at zero when at least one deduction was a dispute.

## Example

```python
process_marketplace([
    "ACCOUNT seller", "ACCOUNT platform", "CREATE p 100",
    "SPLIT p seller 90", "SPLIT p platform 10", "CAPTURE p",
    "REFUND r p 25", "BALANCE seller", "BALANCE platform", "STATUS p",
])
# ["OK", "OK", "OK", "OK", "OK", "OK", "OK", "75", "0", "PARTIAL,100,75"]
```

