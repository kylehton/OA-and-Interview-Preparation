# P02 — Wallet Command Processor

**Difficulty:** Easy  
**Target:** 40 minutes  
**Entry point:** `process_commands(commands) -> list[str]`

Process whitespace-separated commands in order. Return exactly one response for
every input command. A malformed or invalid command returns `ERROR` and must not
change state.

## Part 1 — Create and credit

```text
CREATE <wallet_id>
CREDIT <transaction_id> <wallet_id> <positive_amount>
BALANCE <wallet_id>
```

- `CREATE` returns `OK` unless the non-empty wallet ID already exists.
- `CREDIT` adds funds and returns `OK` when the wallet exists and the globally
  unique transaction ID has not been used successfully.
- `BALANCE` returns the decimal balance, or `ERROR` for an unknown wallet.

## Part 2 — Debit

```text
DEBIT <transaction_id> <wallet_id> <positive_amount>
```

A debit succeeds only when the wallet has sufficient funds. A failed mutation
does **not** reserve its transaction ID, so that ID may be retried later.

## Part 3 — Reverse a transaction

```text
REVERSE <reversal_id> <original_transaction_id>
```

A successful credit or debit can be reversed exactly once. Reversing a credit
requires the wallet to still contain the credited amount; reversing a debit
adds its amount back. On success, reserve the reversal ID and mark the original
transaction reversed. Reversals cannot themselves be reversed.

## Part 4 — Atomic transfer

```text
TRANSFER <transaction_id> <source_wallet> <destination_wallet> <positive_amount>
```

Both distinct wallets must exist and the source must have enough money. Apply
both balance changes atomically. A transfer is reversible under Part 3, but the
destination must still have enough money to move the amount back.

## Example

```python
process_commands([
    "CREATE alice",
    "CREATE bob",
    "CREDIT c1 alice 500",
    "TRANSFER t1 alice bob 125",
    "BALANCE alice",
    "REVERSE r1 t1",
    "BALANCE bob",
])
# ["OK", "OK", "OK", "OK", "375", "OK", "0"]
```

Identifiers are case-sensitive. Amounts are integer minor units; Python `bool`
parsing is irrelevant because all input begins as text.

