from __future__ import annotations

from typing import Optional


def first_slo_breach(
    filepath: str,
    service: str,
    window_seconds: int,
    max_error_rate: float,
) -> Optional[str]:
    """
    Return timestamp of first request that causes rolling window error rate
    for `service` to exceed max_error_rate. See README for details.

    We want timestamp in sec to check against window_seconds, so we can use .total_seconds() after datetime obj delta
    list is sorted by time in file (nondecreasing)
    we can use a queue to store the window
    """
    from datetime import datetime
    from collections import deque
    window_len = 0
    error_sum = 0
    window = deque()
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3 and parts[2].isnumeric():
                curr_timestamp = parts[0].strip()
                curr_service = parts[1].strip()
                curr_status = int(parts[2].strip())
                if curr_service == service:
                    curr_datetime = datetime.fromisoformat(curr_timestamp)
                    while window and (curr_datetime - window[0][2]).total_seconds() > window_seconds:
                        removed = window.popleft()
                        if removed[1] >= 500:
                            error_sum -= 1
                        window_len -= 1
                        # add more logic here for other counters
                    window.append((curr_timestamp, curr_status, curr_datetime))
                    window_len += 1
                    if curr_status >= 500:
                        error_sum += 1
                    if window_len > 1 and (error_sum/window_len) > max_error_rate:
                            return window[-1][0]
    return None



