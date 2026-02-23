from __future__ import annotations

from typing import List, Tuple


class ServiceMonitor:
    def __init__(self):
        # we should store services in a dict, where the value is a list of size 2
        # index 0 -> error count, index 1 -> total count
        self.services = {}

    def record(self, service: str, status_code: int) -> None:
        if service not in self.services:
            self.services[service] = (0, 0)
        if isinstance(status_code, int) and status_code >= 500:
            self.services[service] = (self.services[service][0] + 1, self.services[service][1] + 1)
        else:
            self.services[service] = (self.services[service][0], self.services[service][1] + 1)

    def error_rate(self, service: str) -> float:
        if service in self.services:
            return round(self.services[service][0]/self.services[service][1], 4)
        else:
            return 0.0

    def top_unhealthy(self, n: int) -> List[Tuple[str, float]]:
        import heapq

        top_unhealthy = heapq.nsmallest(n, self.services.items(), key=lambda x: (-(self.error_rate(x[0])), -x[1][1], x[1][0]))
        result = []
        for item in top_unhealthy:
            result.append((item[0], self.error_rate(item[0])))
        return result
        

