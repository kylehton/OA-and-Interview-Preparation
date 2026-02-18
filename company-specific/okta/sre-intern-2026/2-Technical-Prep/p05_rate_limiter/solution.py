from __future__ import annotations


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Initialize limiter.

        max_requests: maximum allowed requests within window_seconds rolling window.
        window_seconds: size of window (>= 1).
        """
        raise NotImplementedError

    def allow(self, timestamp: int) -> bool:
        """
        Return True if request at timestamp is allowed, else False.
        Rejected requests do not count.
        """
        raise NotImplementedError
