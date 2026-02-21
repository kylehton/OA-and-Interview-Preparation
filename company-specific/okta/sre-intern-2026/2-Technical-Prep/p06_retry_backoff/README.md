# P06 — Retry with Exponential Backoff (Practical + Testing)

Implement a retry helper that retries a failing operation using exponential backoff.

---

## Part 1 — Basic Exponential Backoff

Implement:

```python
retry(operation, retries: int, base_delay: float, sleep_fn=time.sleep)
```

### Behavior

- Call `operation()`.
- If it succeeds, immediately return its value.
- If it raises an `Exception`:
  - If no retries remain, re-raise the last exception.
  - Otherwise:
    - Sleep for:

      ```
      base_delay * (2 ** attempt_index)
      ```

    - Then retry the operation.

### Important Details

- `attempt_index` starts at **0 for the first failure**.
- `retries=3` means:
  - 1 initial attempt
  - up to 3 additional retries
  - **maximum 4 total attempts**
- You **must use `sleep_fn`** (tests may pass a fake sleep function).

---

## Example Runthrough (Basic)

**Input:**
```python
# operation fails twice, then succeeds
attempts = 0
def operation():
    global attempts
    attempts += 1
    if attempts < 3:
        raise Exception("fail")
    return "success"

retries = 3
base_delay = 1.0
```

**Output:**
```python
"success"
# attempt 1 -> fail (sleep 1.0)
# attempt 2 -> fail (sleep 2.0)
# attempt 3 -> success
```

---

## Part 2 — Exponential Backoff with Jitter

To reduce retry storms in distributed systems, we add jitter.

Implement:

```python
retry_with_jitter(operation, retries, base_delay, jitter_fn, sleep_fn)
```

### Delay Formula

```
base_delay * (2 ** attempt_index) + jitter_fn()
```

Where:
- `jitter_fn()` returns a float (can be 0).
- Jitter is added **after** exponential calculation.
- Still must use `sleep_fn`.

---

## Example Runthrough (With Jitter)

**Input:**
```python
# operation fails twice, then succeeds
attempts = 0
def operation():
    global attempts
    attempts += 1
    if attempts < 3:
        raise Exception("fail")
    return "success"

def jitter_fn():
    return 0.5  # constant jitter for example

retries = 3
base_delay = 1.0
```

**Output:**
```python
"success"
# attempt 1 -> fail (sleep 1.0 + 0.5 = 1.5)
# attempt 2 -> fail (sleep 2.0 + 0.5 = 2.5)
# attempt 3 -> success
```

---

## Notes

- Backoff grows exponentially: 1x, 2x, 4x, 8x, ...
- Jitter helps prevent synchronized retries across many clients.
- Always re-raise the *last* exception if retries are exhausted.
- Amortized complexity is O(retries).