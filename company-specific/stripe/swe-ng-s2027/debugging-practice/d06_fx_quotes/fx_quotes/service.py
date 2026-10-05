from __future__ import annotations

from .book import RateBook


class QuoteService:
    def __init__(self, rate_book: RateBook) -> None:
        self._rate_book = rate_book
        self._cache: dict[tuple[str, str], int] = {}

    def convert(self, amount: int, source: str, target: str, *, at: int) -> int:
        if amount <= 0 or at < 0:
            raise ValueError("invalid quote request")
        if source == target:
            return amount

        cache_key = (source, target)
        if cache_key in self._cache:
            return self._cache[cache_key]

        direct = self._rate_book.latest(source, target, at)
        if direct is not None:
            result = amount * direct.numerator // direct.denominator
        else:
            reverse = self._rate_book.latest(target, source, at)
            if reverse is None:
                raise LookupError("no rate available")
            result = amount * reverse.numerator // reverse.denominator

        self._cache[cache_key] = result
        return result

