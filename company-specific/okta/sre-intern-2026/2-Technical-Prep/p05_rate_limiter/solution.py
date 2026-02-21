from __future__ import annotations

from typing import Any

class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize limiter.

        max_requests: maximum allowed requests within window_seconds rolling window.
        window_seconds: size of window (>= 1).
        """
        self.requests = []
        self.max_req = max_requests
        self.window_sec = window_seconds

    def allow(self, timestamp: int) -> bool:
        """
        Return True if request at timestamp is allowed, else False.
        Rejected requests do not count.

        Notes:
        we can use a sorted array. we need to create a storage system that persists despite individ. calls
        we would have to have an O(n) insertion, but we could search using binary search, bringing it down
        to O(log n) search. for the bounds, we would go backward from the current timestamp in the array
        and return True if: len(count of elems [timestamp-window_sec, timestamp] <= max_req)
        """
        print("timestamp:", timestamp)
        print("req len:", len(self.requests), self.requests)
        curr_index = 0
        # keep going until curr is less than next
        if len(self.requests) == 0:
            self.requests.append(timestamp)
        else:
            while curr_index < len(self.requests) and timestamp >= self.requests[curr_index]:
                curr_index += 1
            
            if curr_index == len(self.requests):
                self.requests.append(timestamp)
            else:
                self.requests.insert(curr_index, timestamp)
        
        print(self.requests)

        count = 0
        while len(self.requests) > 0 and curr_index >= 0 and (timestamp - self.requests[curr_index] + 1) <= self.window_sec:
            count += 1
            curr_index -= 1
        
        return (count <= self.max_req)
        
