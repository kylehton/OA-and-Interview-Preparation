# P16 — Balance File Consolidator

**Difficulty:** Hard  
**Target:** 70 minutes  
**Entry point:** `build_balance_report(manifest_path, output_path=None) -> list[str]`

This problem uses real files. Use `pathlib`, `json`, and Python's `csv` module.
All text files are UTF-8. Paths may be passed as strings or `Path` objects.
Malformed input is ignored as described below; do not make network requests.

The manifest is a JSON object stored at `manifest_path`:

```json
{
  "files": ["batch_01.csv", "batch_02.csv"],
  "minimum_abs_net": 0
}
```

`files` is required and must be a list. `minimum_abs_net` is optional and
defaults to `0`; when present it must be a non-negative integer (not a Boolean).
An unreadable or malformed manifest returns `[]` and does not write an output
file. Non-string entries inside an otherwise valid `files` list are skipped.

Resolve listed files relative to the manifest's directory. Only regular `.csv`
files whose resolved paths remain inside that directory are eligible. Skip
missing, unreadable, unsafe, or incorrectly headed files.

Every eligible CSV must have this exact header:

```text
transaction_id,account_id,currency,kind,amount,related_id
```

Parse and format CSV with normal quoting rules. Trim every parsed field.

## Part 1 — Credits, debits, and aggregation

Base rows use `kind` equal to `CREDIT` or `DEBIT`:

- `transaction_id` and `account_id` must be non-empty;
- `currency` must be exactly three uppercase ASCII letters;
- `amount` must be a positive integer; and
- `related_id` must be empty.

Aggregate by `(account_id, currency)`. Credits increase the credit total and
debits increase the debit total:

```python
net = credit_total - debit_total
```

Return nonzero groups sorted by account ID and then currency as CSV-formatted
rows:

```text
<account_id>,<currency>,<credit_total>,<debit_total>,<net_amount>
```

## Part 2 — Files, schemas, and idempotency

Process files in manifest order and rows in file order. Successful transaction
IDs are globally unique across all files; only the first valid row using an ID
counts. Invalid rows do not reserve IDs. Listing a file more than once is
allowed, but the transaction-ID rule prevents its valid rows from applying
twice.

A bad header skips the complete file. A malformed data row only skips that row.
Every data row must have exactly six fields. CSV fields may contain commas or
quotes and returned rows must escape them. Reading and UTF-8 decoding are
file-atomic: an I/O or decode failure anywhere in a file skips that whole file,
including rows read before the failure.

## Part 3 — Reversals across files

A reversal row has:

```text
<new_transaction_id>,,,REVERSAL,,<original_transaction_id>
```

Its account, currency, and amount fields must be empty. It succeeds only when
the related ID names a successful `CREDIT` or `DEBIT` that has not already been
reversed. Reverse that original contribution in its original group. Reversal
IDs share the global transaction-ID namespace. Failed reversals do not reserve
their IDs, and reversals cannot themselves be reversed.

## Part 4 — Threshold and output file

Include a nonzero group only when:

```python
abs(net_amount) >= minimum_abs_net
```

The comparison is inclusive. Gross credit/debit totals in an output row reflect
successful reversals as well.

When `output_path` is provided, create its parent directories and write UTF-8
CSV with this header followed by exactly the returned rows:

```text
account_id,currency,credit_total,debit_total,net_amount
```

Use `newline=""` while reading and writing CSV files.
For a valid manifest that produces no report rows, still write the header-only
output file. Invalid manifests are the cases that produce no output file.

## Example

Given a manifest beside a batch containing a `100` credit and a `30` debit for
`acct,USD`, the function returns:

```python
["acct,USD,100,30,70"]
```

See `fixtures/basic/` for a complete local input bundle.
