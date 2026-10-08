# Incident Monitor

**Company:** Stripe  
**Difficulty:** Hard  
**Stage:** Full-time, New Grad OA  
**Last reported:** October 1, 2026

## Problem statement

Source note: The judged core task is about a 98% match to the available
sources. The 30-second window, alert identity and de-duplication, five-failure
threshold, strictly-greater-than-1% impact rule, resolution behavior, output
ordering, and both examples are source-backed. Only a few lifecycle edge
details required clarification to keep the task deterministic.

Special thanks: („• ֊ •„) 🌷 A super big thank you to a fren who shared that
this question was asked again on 09/07/2026! 🌷

### Background & Definitions

At Stripe, we monitor millions of transactions hourly to ensure API health.
Your goal is to analyze a list of transaction logs, detect error spikes, and
trigger alerts when an incident is likely in progress.

### Task

Implement the `detectIncidents(logs)` function. It analyzes a list of
transactions (that can be successful or erroneous), and emits alert trigger and
resolve events if certain conditions are met.

### Sliding Window

For every entry in the transaction log, evaluate whether an alert needs to be
triggered or resolved. All evaluations use a 30-second sliding window.

For example, for a log at timestamp `T`, the window includes all logs with
timestamps in the range `[T-29, T]`, inclusive on both ends.

### Alert

Each alert is tied to a specific `(merchant_id, status_code)` pair.

A merchant may therefore have multiple active alerts at once, one per distinct
error status code.

### De-duplication

If an alert has been triggered for a particular `(merchant_id, status_code)`
pair and is still active (has not been resolved in the meantime), do not
trigger a duplicate alert, even if the conditions for the alert continue to
manifest.

## Input Format

The input `logs` is an array of strings. Each entry has this format:

```text
timestamp,merchant_id,status_code,count
```

- `timestamp`: an integer representing seconds;
- `merchant_id`: the ID of the merchant these transactions belong to;
- `status_code`: an HTTP status code, always either `200`, a `4xx` client-error
  code such as `400`, `404`, or `429`, or a `5xx` server-error code such as
  `500` or `503`; and
- `count`: an integer representing how many times that outcome was observed for
  that merchant in that second.

Assumptions:

- The input is always valid and corresponds to the format above.
- Logs are guaranteed to be sorted by timestamp.
- The input contains no duplicate `(timestamp, merchant_id, status_code)`
  entries.
- Timestamps and counts are nonnegative integers. A count of zero is valid: its
  row still advances that merchant's evaluation time and can trigger or resolve
  alerts as older records leave the window.
- Merchant IDs are nonempty ASCII strings that contain no commas. Sort merchant
  IDs lexicographically by ASCII code point, so uppercase letters precede
  lowercase letters.

## Output Format

Return all alert events produced by the logs. Each output string has this
format:

```text
timestamp,event_type,merchant_id,status_code
```

- `timestamp`: the second when the event was triggered or resolved;
- `event_type`: `TRIGGER` or `RESOLVE`;
- `merchant_id`: the merchant associated with the alert; and
- `status_code`: the error status code associated with the alert.

The output must be sorted by:

```text
(timestamp ASC, merchant_id ASC, status_code ASC, event_type ASC)
```

For `event_type`, alphabetical order means `RESOLVE` comes before `TRIGGER`.

## Part 1: Basic Incident Detection

Trigger an alert when there are at least five failures with the exact same
error code for the same merchant within the last 30 seconds.

After finishing Part 1, source test cases 0–3 should pass.

### Part 1 Sample Test Case

Input:

```text
10,merchant1,500,2
10,merchant2,500,1
15,merchant1,500,2
20,merchant1,500,1
20,merchant2,500,4
```

Output:

```text
20,TRIGGER,merchant1,500
20,TRIGGER,merchant2,500
```

## Part 2: Impact Rate Filtering (The 1% Rule)

Large merchants naturally have more errors due to high volume. To reduce
noise, only alert when the error rate is significant relative to the merchant's
successful transaction volume.

An alert is now triggered only when both criteria are met for a specific error
code within the last 30 seconds:

- **Volume:** at least five failures for that specific error code; and
- **Impact:** those failures represent more than 1% of the merchant's
  successful transaction volume—the total count with status code `200` for that
  merchant—in the same window.

The impact comparison is strict. Equivalently, use exact integer arithmetic:

```python
failure_count * 100 > successful_count
```

Consequently, five or more failures meet the impact condition when the window
contains zero successful transactions.

After finishing Part 2, source test cases 0–8 should pass.

### Part 2 Sample Test Case

Input:

```text
10,merchant1,200,600
12,merchant1,500,6
15,merchant2,200,599
16,merchant2,500,6
```

Output:

```text
16,TRIGGER,merchant2,500
```

At timestamp 12, merchant1 has six errors, but they are exactly 1% of the
merchant's successful volume of 600, not more than 1%.

At timestamp 16, merchant2 has six errors, which is more than 1% of its
successful volume of 599, so an alert is triggered for merchant2.

## Part 3: Incident Resolution

An active alert for a `(merchant_id, status_code)` pair transitions to resolved
when a log arrives and the previous 30 seconds of logs no longer meet the Part 2
trigger criteria.

### Rules

- An alert is resolved at timestamp `T` only if a log arrives for that merchant
  at `T` and the inclusive window `[T-29, T]` no longer meets both trigger
  conditions.
- Emit `RESOLVE` only when that alert is currently active.
- After a resolve event, the alert becomes inactive and may trigger again if
  both conditions become true later.
- Process entries in their given order. After each entry at timestamp `T`,
  evaluate the alert states relevant to that entry's merchant using the window
  `[T-29, T]`.

### Deterministic lifecycle interpretation used by the tests

For each input entry, add that entry first and then evaluate every non-`200`
status code previously seen for the entry's merchant. This allows a success row,
a different error-code row, or the passage of time represented by any row for
that merchant to trigger or resolve the appropriate alert pair. Do not evaluate
or resolve a merchant merely because a row for another merchant arrives, and do
not perform an end-of-input resolution sweep.

Rows sharing a timestamp are still processed one at a time in their given
order. It is therefore possible for state transitions produced by two rows at
the same timestamp to differ when those rows are reversed. Sort the accumulated
event records only after all input rows have been processed.

## Function

FastPrep signature:

```text
detectIncidents(logs: String[]) → String[]
```

Python workspace signature:

```python
def detectIncidents(logs: list[str]) -> list[str]: ...
```

## Examples

### Example 1

```python
logs = [
    "10,merchant1,500,2",
    "10,merchant2,500,1",
    "15,merchant1,500,2",
    "20,merchant1,500,1",
    "20,merchant2,500,4",
]

detectIncidents(logs)
# [
#     "20,TRIGGER,merchant1,500",
#     "20,TRIGGER,merchant2,500",
# ]
```

### Example 2

```python
logs = [
    "10,merchant1,200,600",
    "12,merchant1,500,6",
    "15,merchant2,200,599",
    "16,merchant2,500,6",
]

detectIncidents(logs)
# ["16,TRIGGER,merchant2,500"]
```
