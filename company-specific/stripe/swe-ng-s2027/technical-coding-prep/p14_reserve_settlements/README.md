# P14 — Reserve Settlement Engine

**Difficulty:** Hard  
**Target:** 70 minutes  
**Entry point:** `process_settlements(commands) -> list[str]`

Return one response per whitespace-separated command. Time-bearing commands are
guaranteed to arrive with globally non-decreasing timestamps. Before executing
one, apply all scheduled releases due at or before its timestamp. Invalid
commands return `ERROR` atomically. Commands must have exactly the shown arity,
merchant and mutation IDs must be non-empty, and timestamps must be
non-negative integers. Due releases occur before validating the rest of a
time-bearing command, so they still occur when that command returns `ERROR`.

## Part 1 — Pending charges

```text
ACCOUNT <merchant_id> <hold_seconds> <reserve_basis_points>
CHARGE <timestamp> <charge_id> <merchant_id> <positive_amount>
BALANCE <timestamp> <merchant_id>
```

Accounts are unique. Hold time is non-negative and reserve basis points are from
`0` through `10000`. A charge starts as pending. Balance returns:

```text
<pending>,<reserved>,<available>
```

## Part 2 — Scheduled reserve release

At `charge_timestamp + hold_seconds`, split the charge's remaining amount:

```python
available_share = remaining * (10000 - reserve_basis_points) // 10000
reserved_share = remaining - available_share
```

At `charge_timestamp + 2 * hold_seconds`, move its remaining reserved share to
available. With a zero hold, both transitions occur immediately as part of the
successful `CHARGE` command.

The releases happen before a command at the same timestamp. Thus a `REFUND` at
the first release timestamp follows the post-release rule, not the pending rule;
a refund at the second release timestamp must be funded entirely from available.

## Part 3 — Payouts

```text
PAYOUT <timestamp> <payout_id> <merchant_id> <positive_amount>
```

A payout succeeds only when the account has enough available balance, then
subtracts it. Successful mutation IDs (`charge_id`, `payout_id`, and later
`refund_id`) share one global namespace. Failed operations do not reserve IDs.

## Part 4 — Partial refunds

```text
REFUND <timestamp> <refund_id> <charge_id> <positive_amount>
```

Total refunds may not exceed the charge's unrefunded amount.

- While the charge is pending, reduce that charge and the account's pending
  balance directly; its later split uses the reduced amount.
- After the first release, fund the refund from the merchant's aggregate
  available balance first, then from that charge's own remaining reserve share.
- After the second release, fund it from available balance.

The refund succeeds only if all required funds exist; otherwise make no changes.
If reserve is used, reduce both the account reserve balance and that charge's
future reserve release.

## Example

```python
process_settlements([
    "ACCOUNT m 10 2000",
    "CHARGE 0 c1 m 100",
    "BALANCE 10 m",
    "BALANCE 20 m",
])
# ["OK", "OK", "0,20,80", "0,0,100"]
```
