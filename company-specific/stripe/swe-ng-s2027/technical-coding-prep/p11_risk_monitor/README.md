# P11 — Configurable Merchant Risk Monitor

**Difficulty:** Medium–Hard  
**Target:** 60 minutes  
**Entry point:** `flagged_merchants(risky_outcomes, policies, merchants, events) -> list[str]`

This is an original risk-policy simulation. Inputs other than `risky_outcomes`
are comma-separated with trimmed fields. Return flagged merchant IDs sorted
lexicographically after all events are processed.

`risky_outcomes` is a list of case-sensitive, non-empty outcome strings.

## Part 1 — Count policies

Policy rows:

```text
<category>,COUNT,<risky_count_threshold>,<minimum_attempts>
```

Threshold and minimum must be positive integers. The first valid policy for a
category wins.

Merchant rows:

```text
<merchant_id>,<category>
```

IDs must be non-empty and the category must have a valid policy. The first valid
merchant row for an ID wins.

Attempt events:

```text
ATTEMPT,<event_id>,<merchant_id>,<positive_amount>,<outcome>
```

An outcome is risky exactly when it occurs in `risky_outcomes`. Under `COUNT`,
a merchant is flagged when it has at least `minimum_attempts` attempts and its
risky-attempt count is at least the threshold.

## Part 2 — Ratio policies

```text
<category>,RATIO,<threshold_basis_points>,<minimum_attempts>
```

The threshold must be from `0` through `10000`. Once the minimum is met, flag
when:

```python
risky_attempt_count * 10000 >= threshold_basis_points * total_attempt_count
```

Use integer cross-multiplication, not floating point.

## Part 3 — Clearing a risky classification

```text
CLEAR,<event_id>,<attempt_event_id>
```

A clear event succeeds only when it references an existing risky attempt that
has not already been cleared. The attempt remains in the total denominator but
no longer contributes risky count or amount.

All successful attempt and clear event IDs share one global namespace. The first
successful event reserves an ID. Invalid events do not reserve IDs.

## Part 4 — Amount-ratio policies

```text
<category>,AMOUNT_RATIO,<threshold_basis_points>,<minimum_attempts>
```

After the minimum attempt count is met, flag when:

```python
risky_amount * 10000 >= threshold_basis_points * total_attempt_amount
```

Cleared attempts still contribute their amount to the denominator.

## Example

```python
risky = ["blocked", "stolen"]
policies = ["retail,RATIO,5000,2"]
merchants = ["m1,retail"]
events = [
    "ATTEMPT,a1,m1,100,blocked",
    "ATTEMPT,a2,m1,100,approved",
]

flagged_merchants(risky, policies, merchants, events)  # ["m1"]
```

