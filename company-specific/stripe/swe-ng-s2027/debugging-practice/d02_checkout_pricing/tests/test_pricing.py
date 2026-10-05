import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from checkout_pricing import CartLine, Product, Quote, QuoteEngine


def test_basic_quote_without_rules():
    engine = QuoteEngine([Product("book", 500), Product("pen", 125)])
    assert engine.quote([CartLine("book", 2), CartLine("pen", 1)]) == Quote(
        1125, 0, 0, 1125
    )


def test_repeated_skus_are_combined_for_bulk_pricing():
    engine = QuoteEngine([Product("pen", 125)])
    quote = engine.quote(
        [CartLine("pen", 2), CartLine("pen", 3)],
        bulk_prices={"pen": (5, 100)},
    )
    assert quote == Quote(625, 125, 0, 500)


def test_percentage_rounds_once_per_complete_line():
    engine = QuoteEngine([Product("metered", 101)])
    quote = engine.quote(
        [CartLine("metered", 3)], percentage_off={"metered": 3333}
    )
    assert quote == Quote(303, 100, 0, 203)


def test_tax_is_computed_after_discount():
    engine = QuoteEngine([Product("plan", 1000)])
    quote = engine.quote(
        [CartLine("plan", 1)], tax_bps=1000, percentage_off={"plan": 2000}
    )
    assert quote == Quote(1000, 200, 80, 880)


def test_cache_distinguishes_quantities_and_rules():
    engine = QuoteEngine([Product("x", 100)])
    first = engine.quote([CartLine("x", 1)])
    second = engine.quote([CartLine("x", 2)], percentage_off={"x": 5000})
    assert first == Quote(100, 0, 0, 100)
    assert second == Quote(200, 100, 0, 100)


def test_invalid_line_does_not_modify_cart():
    engine = QuoteEngine([Product("x", 100)])
    cart = [CartLine("missing", 1)]
    try:
        engine.quote(cart)
    except ValueError:
        pass
    assert cart == [CartLine("missing", 1)]

