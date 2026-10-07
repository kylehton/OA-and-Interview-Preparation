# P19 — Payout Calendar Files

**Difficulty:** Hard  
**Target:** 75 minutes  
**Entry point:** `schedule_payout_files(accounts_path, captures_path, holidays_path, output_path=None) -> list[str]`

Read account configuration from CSV, captures from a tab-separated file, and a
plain-text holiday calendar. Use the standard library and integer minor units.
Paths may be strings or `Path` objects. All files are UTF-8.

If a required file is missing, unreadable, or has a bad required header, return
`[]` and do not write an output file.

## Part 1 — Configuration and basic grouping

The account CSV has the exact header:

```text
merchant_id,currency,delay_business_days,cutoff_utc_hour
```

IDs must be non-empty, currency exactly three uppercase ASCII letters, delay a
non-negative integer, and cutoff an integer from `0` through `23`. Configuration
is keyed by `(merchant_id, currency)`; the first valid row for a key wins.
Trim every parsed account and capture field. Account rows must have exactly four
fields and capture rows exactly five.

The capture file uses tabs and has this exact header:

```text
capture_id	merchant_id	currency	amount	captured_at
```

Capture IDs and merchant IDs must be non-empty, amounts positive integers, and
the merchant/currency configuration must exist.

Group accepted captures by settlement date, merchant, and currency. Return
normal CSV-formatted rows sorted in that order:

```text
<settlement_date>,<merchant_id>,<currency>,<capture_count>,<total_amount>
```

Part 1 cases use `Z` timestamps before the cutoff, a zero delay, business-day
capture dates, and no holidays; for those baseline cases the settlement date is
the UTC capture date. Parts 2 and 3 extend that calculation without changing
the output shape.

## Part 2 — UTC conversion and cutoff

`captured_at` must be an ISO timestamp with seconds and either `Z` or a numeric
UTC offset, for example:

```text
2026-01-05T16:30:00Z
2026-01-05T18:30:00+02:00
```

The accepted forms are exactly `YYYY-MM-DDTHH:MM:SSZ` and
`YYYY-MM-DDTHH:MM:SS+HH:MM` (or `-HH:MM`). Fractional seconds, missing seconds,
missing offsets, lowercase `z`, and invalid calendar or offset values are
rejected.

Convert it to UTC before applying the account cutoff. When the UTC time is
strictly before `cutoff_utc_hour:00:00`, the base date is its UTC date. At or
after the cutoff, the base date is the next calendar date.

## Part 3 — Weekends, holidays, and delay

The holiday file contains one exact `YYYY-MM-DD` date per line. Ignore blank
lines, lines beginning with `#` after trimming, malformed dates, and duplicates.

A business day is Monday through Friday and not a holiday. Compute settlement:

1. roll the base date forward to the first business day on or after it;
2. advance by `delay_business_days` additional business days.

Thus a zero delay settles on the rolled base day, while a delay of one settles
on the following business day.

## Part 4 — Idempotency, validation, and output

Process captures in file order. Successful capture IDs are globally unique;
only the first valid row using an ID counts. Invalid rows do not reserve IDs.

When `output_path` is provided, create parent directories and write UTF-8 CSV
with this header followed by exactly the returned rows:

```text
settlement_date,merchant_id,currency,capture_count,total_amount
```

Use `newline=""` for CSV/TSV reading and writing. CSV quoting is part of the
returned answer.

For valid required inputs that produce no schedule rows, still write the
header-only output file. A required-file failure produces no output file.

See `fixtures/basic/` for a bundle containing CSV, TSV, and text inputs.
