from __future__ import annotations

from bisect import bisect_left
from collections import defaultdict

from .models import Rate


class RateBook:
    def __init__(self) -> None:
        self._rates: dict[tuple[str, str], list[Rate]] = defaultdict(list)
        self.revision = 0

    def add_rate(
        self,
        source: str,
        target: str,
        timestamp: int,
        numerator: int,
        denominator: int,
    ) -> None:
        if source == target or timestamp < 0 or numerator <= 0 or denominator <= 0:
            raise ValueError("invalid rate")
        rates = self._rates[(source, target)]
        rates.append(Rate(timestamp, numerator, denominator))
        rates.sort(key=lambda rate: rate.timestamp)
        self.revision += 1

    def latest(self, source: str, target: str, at: int) -> Rate | None:
        rates = self._rates.get((source, target), [])
        timestamps = [rate.timestamp for rate in rates]
        index = bisect_left(timestamps, at) - 1
        if index < 0:
            return None
        return rates[index]

