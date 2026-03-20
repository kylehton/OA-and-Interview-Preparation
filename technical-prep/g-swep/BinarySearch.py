'''
Question 1:
A user is missing an item and has 30 days of security camera footage. To find
when the item disappeared, you must search through footage stored in a specific
hierarchy:
    Folders: Organized by Date (e.g., /2026-01-01/)
    Files: 24 MP4 files per folder, each representing 1 hour (00.mp4 to 23.mp4).
    Content: Each file is exactly 60 minutes long.

You have access to an expensive API call checkObject(day, hour, minute)
which returns True if the item is present at that specific time, and False if
it is gone.

Calling this API incurs latency based on the following storage system costs:
    Change Directory: 2.0 seconds (to move between date folders).
    File Open: 500ms (to open an hourly MP4 file within a folder).
    Frame Check: 100ms (to check a minute within an already open file).

How do you find the exact minute the item disappeared, while minimizing the
total latency?
'''

# ---------------------------------------------------------------------------
# Mock checkObject — simulates the real API with cost tracking
# ---------------------------------------------------------------------------

_disappearance: tuple[int, int, int] | None = None  # set by setup_test()
_last_day = None
_last_hour = None
total_cost = 0.0        # accumulated latency in seconds


def setup_test(day, hour, minute):
    """Configure the hidden disappearance time before running a test."""
    global _disappearance, _last_day, _last_hour, total_cost
    _disappearance = (day, hour, minute)
    _last_day = None
    _last_hour = None
    total_cost = 0.0


def checkObject(day, hour, minute) -> bool:
    """
    Returns True  if the item is still present at (day, hour, minute).
    Returns False if the item is already gone.

    Cost model:
        +2.0 s  — moving to a different date folder
        +0.5 s  — opening a different hour file within the same folder
        +0.1 s  — reading a frame (always charged)
    """
    global _last_day, _last_hour, total_cost

    cost = 0.1                          # frame check is always charged
    if day != _last_day:
        cost += 2.0
        _last_hour = None               # new directory = file must be re-opened
    if hour != _last_hour:
        cost += 0.5

    _last_day = day
    _last_hour = hour
    total_cost += cost

    d, h, m = _disappearance if _disappearance is not None else (0, 0, 0)
    gone_at = d * 24 * 60 + h * 60 + m
    queried = day * 24 * 60 + hour * 60 + minute
    return queried < gone_at            # True = present, False = gone


# ---------------------------------------------------------------------------
# Solution
# ---------------------------------------------------------------------------

def findDisappearance():
    """
    Find the exact minute the item first disappeared using hierarchical binary
    search, minimising total latency.

    Returns (day, hour, minute) — the first moment checkObject returns False.
    Days  : 0–29   Hours : 0–23   Minutes : 0–59
    """
    pass  # TODO: implement


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------

def run_test(label, day, hour, minute):
    setup_test(day, hour, minute)
    result = findDisappearance()
    expected = (day, hour, minute)
    status = "PASS" if result == expected else "FAIL"
    print(f"[{status}] {label}")
    print(f"       expected={expected}  got={result}  cost={total_cost:.1f}s")


if __name__ == "__main__":
    run_test("First possible minute  (day=0,  h=0,  m=0)",   0,  0,  0)
    run_test("Last possible minute   (day=29, h=23, m=59)", 29, 23, 59)
    run_test("Middle of the footage  (day=15, h=12, m=30)", 15, 12, 30)
    run_test("Early same-day hour    (day=0,  h=5,  m=10)",  0,  5, 10)
    run_test("Last minute of a day   (day=7,  h=23, m=59)",  7, 23, 59)
    run_test("First minute of a day  (day=20, h=0,  m=0)",  20,  0,  0)
