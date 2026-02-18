from __future__ import annotations

from typing import List, Tuple


class ServiceMonitor:
    def __init__(self):
        raise NotImplementedError

    def record(self, service: str, status_code: int) -> None:
        raise NotImplementedError

    def error_rate(self, service: str) -> float:
        raise NotImplementedError

    def top_unhealthy(self, n: int) -> List[Tuple[str, float]]:
        raise NotImplementedError


class ThreadSafeServiceMonitor(ServiceMonitor):
    def __init__(self):
        super().__init__()
        raise NotImplementedError
