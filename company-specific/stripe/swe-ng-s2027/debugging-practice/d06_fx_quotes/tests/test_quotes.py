import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from fx_quotes import QuoteService, RateBook


def test_historical_direct_rate_between_versions():
    book = RateBook()
    book.add_rate("USD", "EUR", 1, 1, 2)
    book.add_rate("USD", "EUR", 10, 3, 4)
    assert QuoteService(book).convert(100, "USD", "EUR", at=5) == 50


def test_rate_is_active_at_exact_timestamp():
    book = RateBook()
    book.add_rate("USD", "EUR", 1, 1, 2)
    book.add_rate("USD", "EUR", 10, 3, 4)
    assert QuoteService(book).convert(100, "USD", "EUR", at=10) == 75


def test_out_of_order_insertion_still_selects_latest_eligible_rate():
    book = RateBook()
    book.add_rate("USD", "EUR", 10, 3, 4)
    book.add_rate("USD", "EUR", 1, 1, 2)
    assert QuoteService(book).convert(100, "USD", "EUR", at=8) == 50


def test_cache_distinguishes_amount_and_timestamp():
    book = RateBook()
    book.add_rate("USD", "EUR", 1, 1, 2)
    book.add_rate("USD", "EUR", 10, 3, 4)
    service = QuoteService(book)
    assert service.convert(100, "USD", "EUR", at=5) == 50
    assert service.convert(200, "USD", "EUR", at=10) == 150


def test_reverse_rate_is_inverted():
    book = RateBook()
    book.add_rate("USD", "EUR", 1, 1, 2)
    assert QuoteService(book).convert(50, "EUR", "USD", at=2) == 100


def test_cache_observes_newly_added_rates():
    book = RateBook()
    book.add_rate("USD", "EUR", 1, 1, 2)
    service = QuoteService(book)
    assert service.convert(100, "USD", "EUR", at=5) == 50
    book.add_rate("USD", "EUR", 5, 4, 5)
    assert service.convert(100, "USD", "EUR", at=5) == 80


def test_missing_rate_raises_lookup_error():
    with pytest.raises(LookupError):
        QuoteService(RateBook()).convert(10, "USD", "JPY", at=1)

