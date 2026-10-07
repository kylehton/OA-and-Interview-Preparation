# P10 — Time-Versioned FX Ledger

**Difficulty:** Medium  
**Target:** 55 minutes  
**Entry point:** `process_ledger(commands) -> list[str]`

Process whitespace-separated commands in order and return one response per
command. Currency codes are exactly three uppercase ASCII letters. All amounts
are integer minor units. Commands must have exactly the shown arity and all IDs
must be non-empty. Invalid commands return `ERROR` atomically.

## Part 1 — Accounts and balances

```text
OPEN <account_id> <base_currency>
DEPOSIT <transaction_id> <account_id> <currency> <positive_amount>
BALANCE <account_id> <currency>
```

Account IDs are unique. Accounts may hold any valid currency, not only their
base. Successful transaction IDs are globally unique. `BALANCE` returns `0` for
a currency the known account has never held.

## Part 2 — Direct rates and conversion

```text
RATE <timestamp> <from_currency> <to_currency> <numerator> <denominator>
CONVERT <transaction_id> <timestamp> <account_id> <from> <to> <amount>
```

Rate timestamps are non-negative; currencies must differ; numerator and
denominator are positive. Conversion and transfer timestamps must also be
non-negative. Store every valid rate version. A conversion uses the registered
direct rate with the greatest timestamp not exceeding the conversion timestamp.
If multiple eligible versions in the same direction have the same timestamp,
the one registered later in command order wins:

```python
converted = amount * numerator // denominator
```

It succeeds only when the two currencies differ, the source balance is
sufficient, and the converted value is positive.

## Part 3 — Historical lookup and inverse rates

Commands may register rates out of timestamp order. If no eligible direct rate
exists, use the newest eligible reverse rate and invert it:

```python
converted = amount * reverse_denominator // reverse_numerator
```

If both directions are available, the direct direction always wins. Rounding is
always down and mutations are atomic.

## Part 4 — Cross-account transfer

```text
TRANSFER <transaction_id> <timestamp> <source_account> <destination_account> <amount>
```

Transfer from the source account's base currency into the destination account's
base currency, using the same rate lookup. Distinct known accounts, sufficient
source balance, and a positive output are required. If the base currencies are
equal, transfer 1:1 without a rate. Credit the destination only after every
validation succeeds.

## Example

```python
process_ledger([
    "OPEN a USD", "OPEN b EUR", "DEPOSIT d1 a USD 100",
    "RATE 1 USD EUR 9 10", "TRANSFER t1 1 a b 100",
    "BALANCE a USD", "BALANCE b EUR",
])
# ["OK", "OK", "OK", "OK", "OK", "0", "90"]
```
