# P20 — Sharded Ledger Audit

**Difficulty:** Hard  
**Target:** 80 minutes  
**Entry point:** `audit_ledger_bundle(config_path, output_path=None) -> list[str]`

Audit an account ledger stored across several files. The bundle combines INI,
CSV, pipe-separated, and JSON formats, and each ledger shard is protected by a
SHA-256 digest. Use only the standard library and integer minor units.

Paths may be strings or `Path` objects. All text files are UTF-8. The digest is
calculated over the shard's raw bytes, before decoding it as text.

Every part uses the shard manifest named by the config. It has this exact CSV
header:

```text
sequence,path,sha256
```

Sequence is a positive integer. Path is a safe relative path ending in `.psv`,
and SHA-256 is 64 lowercase hexadecimal characters matching the shard's raw
bytes. Every manifest data row must have exactly three fields. Part 1 cases use
at most one well-formed, verified shard entry; Part 2 adds multiple-shard
ordering and failure behavior. A shard path is safe only when it is not
absolute and its resolved target remains inside the config file's directory;
this also rejects symlink escapes.

## Part 1 — Accounts and basic operations

`config_path` is an INI file with this required section and these keys:

```ini
[ledger]
accounts = accounts.csv
shards = shards.csv
checkpoints = checkpoints.json
```

Each value is a path relative to the config file's directory. Referenced paths
must resolve to regular files inside that directory: absolute paths and paths
that escape the directory are invalid. `accounts` must end in `.csv`, `shards`
in `.csv`, and `checkpoints` in `.json`.

The accounts file has this exact CSV header:

```text
account_id,currency,opening_balance
```

An account ID must be non-empty, currency must be exactly three uppercase ASCII
letters, and opening balance must be a non-negative integer. Account ID `-` is
invalid because that token represents the absent side of a ledger operation;
an account ID containing `|` is also invalid because shards use it as a field
delimiter.
The first valid row for an account ID wins; invalid rows do not reserve IDs.
Every account data row must have exactly three fields. Trim every parsed CSV and
pipe-separated data field.

Each ledger shard is pipe-separated and has this exact header:

```text
timestamp|event_id|operation|source|destination|amount
```

For Part 1, support these operations:

- `CREDIT`: `source` is `-`, `destination` is a known account, and `amount` is
  added to the destination.
- `DEBIT`: `source` is a known account, `destination` is `-`, and `amount` is
  subtracted from the source only when its balance is sufficient.

Timestamps are non-negative integers, event IDs are non-empty, and amounts are
positive integers. Rows must have exactly six fields and unknown operations are
invalid. Process rows in file order; timestamps are validated but do not reorder
events.

## Part 2 — Multiple-shard ordering and failure handling

The first syntactically valid manifest row for a sequence wins. Here,
"syntactically valid" means a positive sequence, a safe relative `.psv` path,
and a correctly shaped lowercase digest. Invalid rows do not reserve a
sequence. File existence and digest equality are checked only after selection.
Process selected rows in ascending sequence order, not manifest order. If a
selected shard is missing, unreadable, not UTF-8, has a bad header, or fails its
digest check, skip that whole shard. Do not process even its otherwise-valid
rows, and do not fall back to a later duplicate sequence.

If the config, accounts file, shard manifest, or checkpoints file is missing,
unreadable, unsafe, or structurally malformed, return `[]` and do not write an
output file. A bad individual shard is skipped as described above.

## Part 3 — Transfers and global idempotency

Add `TRANSFER`: source and destination must be distinct known accounts using the
same currency. Move the positive amount only when the source balance is
sufficient. A failed transfer changes neither account.

Successful event IDs are globally unique across every processed shard. Only the
first successful row for an ID counts. Invalid or unsuccessful rows do not
reserve the ID, so a corrected later row may use it.

## Part 4 — Checkpoints and JSON output

The checkpoints file must have a JSON array at its top level; another JSON type
makes the required file structurally malformed. A checkpoint has this form:

```json
{
  "after_sequence": 2,
  "balances": {
    "acct_a": 1250,
    "acct_b": 400
  }
}
```

`after_sequence` must be a positive JSON integer (not a boolean). `balances`
must be an object; every key must name a known account and every value must be a
non-negative JSON integer (not a boolean). The first valid checkpoint for a
sequence wins. Invalid checkpoints do not reserve a sequence.

Checkpoint validation is all-or-nothing: one unknown account or invalid balance
makes the complete checkpoint invalid. An empty `balances` object is valid and
simply produces no comparisons.

Immediately after processing a verified shard, compare any selected checkpoint
for that sequence with the current balances. Emit one row for every unequal
listed account. Checkpoints for skipped or unlisted shard sequences are ignored.

Return normal CSV-formatted rows in this order:

1. mismatches sorted by sequence, then account ID;
2. final balances sorted by account ID.

```text
MISMATCH,<sequence>,<account_id>,<expected>,<actual>
BALANCE,<account_id>,<currency>,<balance>
```

CSV quoting is part of the returned answer.

When `output_path` is provided, create its parent directories and write UTF-8
JSON containing the same result data:

```json
{
  "mismatches": [
    {"sequence": 2, "account_id": "acct_b", "expected": 400, "actual": 350}
  ],
  "balances": [
    {"account_id": "acct_a", "currency": "USD", "balance": 1250}
  ]
}
```

Keep both arrays in the same order as their corresponding returned rows. Write
no output file when a required bundle file is invalid.
For a valid bundle with no accounts or mismatches, still write both empty JSON
arrays when `output_path` is provided.

See `fixtures/basic/` for a complete bundle.
