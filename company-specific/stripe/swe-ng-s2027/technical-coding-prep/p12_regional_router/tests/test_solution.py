from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p12_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


route_requests = _load().route_requests


def test_part_1_registry_and_health_validation():
    commands = ["ADD a 2", "ADD a 1", "ADD b 0", "HEALTH a DOWN", "HEALTH x UP"]
    assert route_requests(commands) == ["OK", "ERROR", "ERROR", "OK", "ERROR"]


def test_part_1_wrong_arity_and_health_value_are_atomic():
    commands = [
        "ADD a 1 extra", "ADD a 1", "HEALTH a MAYBE", "HEALTH a DOWN extra",
        "HEALTH a DOWN",
    ]
    assert route_requests(commands) == ["ERROR", "OK", "ERROR", "ERROR", "OK"]


def test_part_1_region_ids_cannot_contain_output_delimiters():
    commands = ["ADD a>b 1", "ADD a,b 1", "ADD safe 1"]
    assert route_requests(commands) == ["ERROR", "ERROR", "OK"]


def test_part_2_routes_to_shortest_eligible_region():
    commands = [
        "ADD a 1", "ADD b 1", "ADD c 1",
        "LINK a b 10", "LINK a c 3", "HEALTH a DOWN",
        "ROUTE r1 a",
    ]
    assert route_requests(commands)[-1] == "c,3,a>c"


def test_part_2_down_regions_can_be_transit_nodes():
    commands = [
        "ADD a 1", "ADD mid 1", "ADD z 1",
        "LINK a mid 2", "LINK mid z 2",
        "HEALTH a DOWN", "HEALTH mid DOWN", "ROUTE r a",
    ]
    assert route_requests(commands)[-1] == "z,4,a>mid>z"


def test_part_3_capacity_and_idempotent_routes():
    commands = [
        "ADD a 1", "ADD b 1", "LINK a b 2",
        "ROUTE r1 a", "ROUTE r2 a", "ROUTE r3 a", "ROUTE r1 b",
    ]
    assert route_requests(commands)[-4:] == ["a,0,a", "b,2,a>b", "NONE", "a,0,a"]


def test_part_4_release_restores_capacity_once():
    commands = [
        "ADD a 1", "ROUTE r1 a", "ROUTE full a",
        "RELEASE r1", "RELEASE r1", "ROUTE r2 a", "ROUTE r1 a",
    ]
    assert route_requests(commands) == [
        "OK", "a,0,a", "NONE", "OK", "ERROR", "a,0,a", "a,0,a"
    ]


def test_part_4_destination_and_path_ties_are_lexicographic():
    commands = [
        "ADD o 1", "ADD a 1", "ADD b 1", "ADD x 1", "ADD d 1",
        "HEALTH o DOWN", "HEALTH x DOWN", "HEALTH b DOWN",
        "LINK o a 5", "LINK o b 1", "LINK b d 4", "LINK o x 1", "LINK x d 4",
        "ROUTE first o",   # a and d both at 5; destination a wins
        "HEALTH a DOWN", "ROUTE second o",  # d has equal paths via b and x; b path wins
    ]
    result = route_requests(commands)
    assert result[-3] == "a,5,o>a"
    assert result[-1] == "d,5,o>b>d"


def test_part_2_links_are_undirected_and_later_link_replaces_latency():
    commands = [
        "ADD a 1", "ADD b 1", "HEALTH a DOWN",
        "LINK a b 10", "LINK b a 2", "ROUTE r a",
    ]
    assert route_requests(commands)[-1] == "b,2,a>b"


def test_part_3_error_does_not_reserve_request_id():
    commands = [
        "ROUTE retry missing", "ADD missing 1", "ROUTE retry missing"
    ]
    assert route_requests(commands) == ["ERROR", "OK", "missing,0,missing"]


def test_part_3_none_response_is_cached_after_capacity_changes():
    commands = [
        "ADD a 1", "ROUTE used a", "ROUTE empty a", "RELEASE used",
        "ROUTE empty a", "ROUTE new a",
    ]
    assert route_requests(commands) == [
        "OK", "a,0,a", "NONE", "OK", "NONE", "a,0,a"
    ]


def test_part_4_none_and_unknown_requests_cannot_be_released():
    commands = [
        "ADD a 1", "ROUTE used a", "ROUTE none a",
        "RELEASE none", "RELEASE missing", "RELEASE used",
    ]
    assert route_requests(commands) == [
        "OK", "a,0,a", "NONE", "ERROR", "ERROR", "OK"
    ]


def test_part_2_invalid_link_replacement_preserves_previous_latency():
    commands = [
        "ADD a 1", "ADD b 1", "HEALTH a DOWN",
        "LINK a b 4", "LINK a b 0", "LINK a a 1", "ROUTE r a",
    ]
    assert route_requests(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "ERROR", "b,4,a>b"
    ]


def test_part_4_health_changes_preserve_load_until_release():
    commands = [
        "ADD a 1", "ROUTE first a", "HEALTH a DOWN", "HEALTH a UP",
        "ROUTE full a", "RELEASE first", "ROUTE next a",
    ]
    assert route_requests(commands) == [
        "OK", "a,0,a", "OK", "OK", "NONE", "OK", "a,0,a"
    ]
