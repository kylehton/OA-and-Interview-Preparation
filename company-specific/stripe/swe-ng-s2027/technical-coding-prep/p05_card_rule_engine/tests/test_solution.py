from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p05_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


validate_cards = _load().validate_cards


def test_part_1_format_errors_and_normalization():
    cards = ["", "p1,123,US", "p2,4242-4242 4242-4242,us"]
    assert validate_cards(cards, []) == [
        "ERROR",
        "p1,NONE,INVALID_FORMAT",
        "p2,NONE,INVALID_FORMAT",
    ]


def test_part_1_normalizes_spaces_and_hyphens_before_validation():
    cards = ["p1, 4242-4242 4242-4242 ,US"]
    ranges = ["424242,424242,VISA,US"]
    assert validate_cards(cards, ranges) == ["p1,VISA,VALID"]


def test_part_1_distinguishes_structural_errors_from_field_format_errors():
    cards = [
        ",4242424242424242,US",
        "too,many,fields,here",
        "p1,4242x424242424242,US",
        "p2,4242424242424242,U",
    ]
    assert validate_cards(cards, []) == [
        "ERROR", "ERROR", "p1,NONE,INVALID_FORMAT", "p2,NONE,INVALID_FORMAT"
    ]


def test_part_2_luhn_failure_precedes_range_lookup():
    cards = ["bad,4242424242424241,US", "good,4242424242424242,US"]
    assert validate_cards(cards, []) == [
        "bad,NONE,INVALID_LUHN",
        "good,NONE,UNSUPPORTED",
    ]


def test_part_3_classifies_valid_cards_and_ignores_bad_ranges():
    cards = ["v,4242424242424242,US", "m,5555555555554444,GB"]
    ranges = [
        "400000,499999,VISA,*",
        "555555,555555,MASTERCARD,*",
        "999999,000000,BROKEN,*",
    ]
    assert validate_cards(cards, ranges) == ["v,VISA,VALID", "m,MASTERCARD,VALID"]


def test_part_3_bin_range_boundaries_are_inclusive():
    cards = ["p,4000000000000002,US"]
    ranges = ["400000,400000,EXACT,US"]
    assert validate_cards(cards, ranges) == ["p,EXACT,VALID"]


def test_part_3_all_invalid_ranges_result_in_unsupported():
    cards = ["p,4242424242424242,US"]
    ranges = [
        "424242,424242,,US",
        "42424,424242,SHORT,*",
        "424242,424242,BAD_COUNTRY,U|USA",
        "broken",
    ]
    assert validate_cards(cards, ranges) == ["p,NONE,UNSUPPORTED"]


def test_part_4_narrowest_country_eligible_range_wins():
    cards = [
        "us,4242424242424242,US",
        "gb,4242424242424242,GB",
        "ca,4000000000000002,CA",
    ]
    ranges = [
        "400000,499999,GLOBAL,*",
        "424000,424999,US_ONLY,US",
        "424200,424299,NORTH_AMERICA,US|CA",
        "424200,424299,TIE_LATER,US",
    ]
    assert validate_cards(cards, ranges) == [
        "us,NORTH_AMERICA,VALID",
        "gb,GLOBAL,VALID",
        "ca,GLOBAL,VALID",
    ]


def test_part_4_csv_quoted_payment_id_is_parsed_and_formatted():
    cards = ['"order,one",4242424242424242,US']
    ranges = ["424242,424242,VISA,US"]
    assert validate_cards(cards, ranges) == ['"order,one",VISA,VALID']
