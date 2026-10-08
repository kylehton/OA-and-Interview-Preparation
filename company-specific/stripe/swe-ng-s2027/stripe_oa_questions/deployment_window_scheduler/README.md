# Deployment Window Scheduler

**Company:** Stripe  
**Difficulty:** Hard  
**Stage:** Intern, New Grad, Full-time OA  
**Last reported:** October 5, 2026

## Problem statement

Source note: 🐿️ This practice version is about a 90% match to the available
source. The minute-of-week model, half-open windows, allowed-minus-freeze logic,
UTC offset conversion, lead time, minimum continuous duration, and next-`k`
window objective come directly from the source. The original callable
signature, complete Part 2 CSV example, exact numeric bounds, and week-boundary
behavior were not shown, so FastPrep filled those details in consistently
without changing what the original question asks you to build.

At Stripe, teams ship changes to services all the time. To keep production
stable, the Service Deployments team runs a scheduler that decides when
deployments are allowed.

## Time Format and Window Representation

Time is represented as an integer `minute_of_week` in the range `[0, 10079]`,
meaning minutes since Monday 00:00. For example:

- `0` is Monday 00:00;
- `60` is Monday 01:00;
- `1440` is Tuesday 00:00; and
- `10079` is Sunday 23:59.

Every window is represented as `start_minute,end_minute` and is half-open: it
includes `start_minute` and excludes `end_minute`. For example, `10,12` covers
minutes 10 and 11.

Implement `scheduleDeploymentWindows`. The value of `part` selects one of the
following stages, and `inputCsv` contains the corresponding CSV rows. Return the
resulting deployment windows as `[[start, end], ...]`, sorted by start time.

## Part 1: Allowed Windows (Tests 1–4)

A team defines the times of the week when deployments are allowed. During an
incident, the Service Deployments team can also define freeze windows that
prevent deployments.

A minute is deployable only when it is inside at least one allowed window and
inside no freeze window. Compute the week's sorted, continuously deployable
windows.

For Part 1, `part` is `"part1"`, and every row in `inputCsv` has this format:

```text
start,end,type
```

The type is either `allowed` or `freeze`. Allowed windows may overlap, freeze
windows may overlap, and adjacent deployable intervals are returned as one
continuous window.

### Part 1 Source Example

```text
part1
540,600,allowed
570,585,freeze
```

The deployable output is:

```python
[[540, 570], [585, 600]]
```

## Part 2: Time Zones and Minimum Duration (Tests 5–11)

The scheduler now aggregates windows from teams around the world. Each window
may use a different local time zone, but all rows contribute to one global
calendar and the result must be returned in UTC.

For Part 2, `part` is `"part2"`. The first row of `inputCsv` contains:

```text
utc_now,lead_time_minutes,min_continuous_minutes,k
```

Each remaining row has this format:

```text
start,end,type,timezone_offset_minutes
```

The window endpoints are local `minute_of_week` values for that row's time
zone, where:

```text
local = UTC + timezone_offset_minutes
```

Convert every window to UTC, normalizing over the 10080-minute week. If a
converted interval crosses the weekly boundary, split it at the boundary.

After conversion, a minute is deployable when it is inside at least one allowed
window and inside no freeze window. A returned UTC window must:

- start no earlier than `utc_now + lead_time_minutes`;
- remain continuously deployable for at least `min_continuous_minutes`; and
- end no later than minute `10080`.

Clip deployable intervals to the earliest permitted start, discard any remaining
interval that is too short, sort the surviving UTC intervals by start time, and
return at most the first `k`. Return fewer than `k` windows when fewer valid
windows exist.

## Function

FastPrep signature:

```text
scheduleDeploymentWindows(part: String, inputCsv: String[]) → int[][]
```

Python workspace signature:

```python
def scheduleDeploymentWindows(part: str, inputCsv: list[str]) -> list[list[int]]:
    ...
```

## Examples

### Example 1

```python
part = "part1"
inputCsv = ["540,600,allowed", "570,585,freeze"]

scheduleDeploymentWindows(part, inputCsv)
# [[540, 570], [585, 600]]
```

The freeze interval removes `[570,585)` from the allowed interval `[540,600)`.

### Example 2

```python
part = "part2"
inputCsv = [
    "1020,0,10,5",
    "540,600,allowed,-480",
    "550,565,freeze,-480",
]

scheduleDeploymentWindows(part, inputCsv)
# [[1020, 1030], [1045, 1080]]
```

The offset converts the allowed interval to `[1020,1080)` and the freeze
interval to `[1030,1045)`. Both remaining windows are at least 10 minutes long.

## Constraints

- Weekly minute values are normalized over a 10080-minute week.
- All intervals are half-open.
- Window rows use type `allowed` or `freeze`.

## Deterministic week-boundary interpretation used by the tests

Input window rows describe non-wrapping local intervals with
`0 <= start < end <= 10080`. The endpoint `10080` is permitted so a window can
include minute `10079`.

Convert a Part 2 interval by subtracting its offset from both local endpoints.
Normalization preserves the interval's duration. When that duration crosses
the UTC week boundary, represent it as one interval ending at `10080` and one
starting at `0`. A full-week interval remains `[0,10080)` after conversion.

After conversion, merge overlapping and adjacent allowed intervals and merge
overlapping and adjacent freeze intervals before subtracting freezes. Pieces at
the opposite ends of the week are not merged into a circular result: all
returned intervals satisfy `0 <= start < end <= 10080` and remain sorted in the
linear UTC week.

For Part 2, apply operations in this order:

1. convert and split every input interval into UTC;
2. compute merged allowed time minus merged freeze time;
3. clip each resulting interval to `utc_now + lead_time_minutes`;
4. discard intervals shorter than `min_continuous_minutes` after clipping;
5. sort by start; and
6. return the first `k`.

