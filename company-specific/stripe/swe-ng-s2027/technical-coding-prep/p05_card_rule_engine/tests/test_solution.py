from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p05_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_cards = _load().validate_cards


def test_part_1_returns_validation_status_without_routing():
    cards = [
        "pay_1,4242-4242 4242-4242,US",
        "pay_2, 5555555555554444 , GB ",
    ]
    assert validate_cards(cards, []) == [
        "pay_1,NONE,VALID",
        "pay_2,NONE,VALID",
    ]


def test_part_1_structural_errors_return_error():
    cards = ["", ",4242424242424242,US", "too,many,fields,here"]
    assert validate_cards(cards, []) == ["ERROR", "ERROR", "ERROR"]


def test_part_1_card_and_country_format_failures_are_explicit():
    cards = [
        "short,123,US",
        "symbol,4242x424242424242,US",
        "lower,4242424242424242,us",
        "long_country,4242424242424242,USA",
        "non_ascii,4242424242424242,ÉU",
        "unicode_digits,４２４２４２４２４２４２４２４２,US",
    ]
    assert validate_cards(cards, []) == [
        "short,NONE,INVALID_FORMAT",
        "symbol,NONE,INVALID_FORMAT",
        "lower,NONE,INVALID_FORMAT",
        "long_country,NONE,INVALID_FORMAT",
        "non_ascii,NONE,INVALID_FORMAT",
        "unicode_digits,NONE,INVALID_FORMAT",
    ]


def test_part_2_luhn_pass_keeps_validation_success_and_failure_is_explicit():
    cards = [
        "good,4242424242424242,US",
        "bad,4242424242424241,US",
    ]
    assert validate_cards(cards, []) == [
        "good,NONE,VALID",
        "bad,NONE,INVALID_LUHN",
    ]


def test_part_2_format_failure_precedes_luhn():
    cards = ["bad_format,424242424242424x,US"]
    assert validate_cards(cards, []) == ["bad_format,NONE,INVALID_FORMAT"]


def test_part_2_luhn_is_not_equivalent_to_an_even_last_digit():
    cards = [
        "invalid_even,4242424242424240,US",
        "valid_odd,4000000000000051,US",
    ]
    assert validate_cards(cards, []) == [
        "invalid_even,NONE,INVALID_LUHN",
        "valid_odd,NONE,VALID",
    ]


def test_part_3_routes_by_six_digit_bin_and_inclusive_boundaries():
    cards = [
        "visa,4242424242424242,US",
        "mastercard,5555555555554444,GB",
        "boundary,4000000000000002,CA",
    ]
    ranges = [
        "400000,400000,BOUNDARY",
        "420000,429999,VISA",
        "555555,555555,MASTERCARD",
    ]
    assert validate_cards(cards, ranges) == [
        "visa,VISA,VALID",
        "mastercard,MASTERCARD,VALID",
        "boundary,BOUNDARY,VALID",
    ]


def test_part_3_nonempty_rules_enable_routing_and_invalid_rules_are_ignored():
    cards = ["card,4242424242424242,US"]
    ranges = [
        "broken",
        "42424,424242,SHORT",
        "999999,000000,BACKWARDS",
        "424242,424242,",
    ]
    assert validate_cards(cards, ranges) == ["card,NONE,UNSUPPORTED"]


def test_part_3_no_matching_range_is_unsupported():
    cards = ["card,4242424242424242,US"]
    ranges = ["500000,599999,OTHER"]
    assert validate_cards(cards, ranges) == ["card,NONE,UNSUPPORTED"]


def test_part_3_range_may_cross_a_leading_digit_boundary():
    cards = ["card,4000000000000002,US"]
    ranges = ["399999,400000,CROSS_BOUNDARY"]
    assert validate_cards(cards, ranges) == ["card,CROSS_BOUNDARY,VALID"]


def test_part_3_network_is_the_selected_trimmed_label():
    cards = ["card,4242424242424242,US"]
    ranges = ["424242,424242,  DOMESTIC_ROUTE  "]
    assert validate_cards(cards, ranges) == ["card,DOMESTIC_ROUTE,VALID"]


def test_part_4_country_restrictions_and_unrestricted_three_field_rules():
    cards = [
        "us,4242424242424242,US",
        "gb,4242424242424242,GB",
    ]
    ranges = [
        "400000,499999,FALLBACK_ROUTE",
        "424000,424999,NORTH_AMERICA,US|CA",
    ]
    assert validate_cards(cards, ranges) == [
        "us,NORTH_AMERICA,VALID",
        "gb,FALLBACK_ROUTE,VALID",
    ]


def test_part_4_smallest_eligible_span_then_input_order_wins():
    cards = ["card,4242424242424242,US"]
    ranges = [
        "400000,499999,GLOBAL,*",
        "424000,424999,REGIONAL,US",
        "424200,424299,FIRST,US|CA",
        "424200,424299,LATER,US",
    ]
    assert validate_cards(cards, ranges) == ["card,FIRST,VALID"]


def test_part_4_ineligible_narrow_rule_does_not_block_wider_rule():
    cards = ["card,4242424242424242,GB"]
    ranges = [
        "400000,499999,FALLBACK_ROUTE,*",
        "424200,424299,US_ONLY,US",
    ]
    assert validate_cards(cards, ranges) == ["card,FALLBACK_ROUTE,VALID"]


def test_part_4_one_bad_country_token_invalidates_the_complete_rule():
    cards = ["card,4242424242424242,US"]
    ranges = [
        "424242,424242,BAD,US|USA",
        "400000,499999,FALLBACK,*",
    ]
    assert validate_cards(cards, ranges) == ["card,FALLBACK,VALID"]


def test_part_4_invalid_country_fields_do_not_become_unrestricted():
    cards = ["card,4242424242424242,US"]
    ranges = [
        "424242,424242,LOWERCASE,us",
        "424242,424242,EMPTY_COUNTRIES,",
        "424242,424242,MIXED_WILDCARD,US|*",
        "400000,499999,FALLBACK_ROUTE",
    ]
    assert validate_cards(cards, ranges) == ["card,FALLBACK_ROUTE,VALID"]


def test_part_4_wrong_range_arity_is_ignored():
    cards = ["card,4242424242424242,US"]
    ranges = [
        "424242,424242,TOO_MANY,US,EXTRA",
        "400000,499999,FALLBACK_ROUTE",
    ]
    assert validate_cards(cards, ranges) == ["card,FALLBACK_ROUTE,VALID"]
