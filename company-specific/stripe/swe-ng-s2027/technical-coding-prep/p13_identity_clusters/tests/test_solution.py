from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p13_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


analyze_identities = _load().analyze_identities


def test_part_1_shared_devices_and_singletons():
    events = [
        "e1,1,bob,d1,-", "e2,2,alice,d1,-", "e3,3,zoe,d9,-"
    ]
    assert analyze_identities(events) == ["SAFE,alice|bob", "SAFE,zoe"]


def test_part_2_cards_join_device_components_transitively():
    events = [
        "e1,1,a,d1,-",
        "e2,2,b,d1,c1",
        "e3,3,c,d2,c1",
    ]
    assert analyze_identities(events) == ["SAFE,a|b|c"]


def test_part_2_device_and_card_namespaces_do_not_collide():
    events = ["e1,1,a,same,-", "e2,2,b,different,same"]
    assert analyze_identities(events) == ["SAFE,a", "SAFE,b"]


def test_part_3_invalid_duplicate_does_not_reserve_event_id():
    events = ["x,bad,a,d,-", "x,1,a,d,-", "y,2,b,d,-", "y,3,c,d,-"]
    assert analyze_identities(events) == ["SAFE,a|b"]


def test_part_4_time_window_uses_adjacent_links_and_transitivity():
    events = [
        "e1,0,a,d,-", "e2,5,b,d,-", "e3,10,c,d,-", "e4,30,z,d,-"
    ]
    assert analyze_identities(events, None, 5) == ["SAFE,a|b|c", "SAFE,z"]


def test_part_4_zero_window_and_risk_propagation():
    events = [
        "e1,1,a,d,-", "e2,1,b,d,-", "e3,2,c,d,-", "e4,3,z,q,-"
    ]
    assert analyze_identities(events, ["b", "absent"], 0) == [
        "REVIEW,a|b", "SAFE,c", "SAFE,z"
    ]


def test_part_3_invalid_rows_do_not_reserve_event_ids():
    events = [
        "x,-1,a,d,-", "x,1,a,d,-",
        "y,2,b,-,-", "y,2,b,d,-",
    ]
    assert analyze_identities(events) == ["SAFE,a|b"]


def test_part_3_empty_event_and_user_ids_are_invalid():
    events = [",1,a,d,-", "e,1,,d,-", "good,1,z,d,-"]
    assert analyze_identities(events) == ["SAFE,z"]


def test_part_4_occurrences_are_sorted_before_window_links_are_built():
    events = [
        "late,10,a,d,-", "early,0,b,d,-", "middle,5,c,d,-"
    ]
    assert analyze_identities(events, None, 5) == ["SAFE,a|b|c"]


def test_part_4_card_window_boundary_is_inclusive():
    events = [
        "e1,0,a,-,card", "e2,5,b,-,card", "e3,11,c,-,card"
    ]
    assert analyze_identities(events, None, 5) == ["SAFE,a|b", "SAFE,c"]


def test_part_4_risky_valid_singleton_is_reviewed():
    assert analyze_identities(["e,1,z,d,-"], ["z", "absent"], 10) == [
        "REVIEW,z"
    ]


def test_part_3_empty_present_identifier_and_wrong_arity_do_not_reserve_id():
    events = [
        "same,1,a,,card",
        "same,1,a,device,-,extra",
        "same,1,a,device,-",
    ]
    assert analyze_identities(events) == ["SAFE,a"]


def test_part_3_output_delimiter_is_not_allowed_inside_user_id():
    events = ["bad,1,a|b,device,-", "good,2,z,device,-"]
    assert analyze_identities(events) == ["SAFE,z"]


def test_part_4_risky_user_matching_is_case_sensitive():
    events = ["e,1,A,device,-"]
    assert analyze_identities(events, ["a"], 0) == ["SAFE,A"]


def test_part_1_csv_quoted_user_id_is_escaped_in_output():
    events = ['e1,1,"alice,inc",device,-', "e2,2,bob,device,-"]
    assert analyze_identities(events) == ['SAFE,"alice,inc|bob"']
