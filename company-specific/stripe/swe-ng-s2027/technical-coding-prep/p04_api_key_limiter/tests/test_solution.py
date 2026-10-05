from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p04_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


evaluate_requests = _load().evaluate_requests


def test_part_1_registration_validation():
    commands = ["REGISTER a 2 10", "REGISTER a 3 5", "REGISTER b 0 5", "bad"]
    assert evaluate_requests(commands) == ["OK", "ERROR", "ERROR", "ERROR"]


def test_part_1_rejects_negative_nonnumeric_and_wrong_arity_without_reserving_key():
    commands = [
        "REGISTER k -1 5", "REGISTER k 1 nope", "REGISTER k 1 5 extra",
        "REGISTER k 1 5",
    ]
    assert evaluate_requests(commands) == ["ERROR", "ERROR", "ERROR", "OK"]


def test_part_2_inclusive_sliding_window():
    commands = [
        "REGISTER live 2 3",
        "REQUEST 10 r1 live",
        "REQUEST 11 r2 live",
        "REQUEST 12 r3 live",
        "REQUEST 13 r4 live",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "ALLOW", "DENY", "ALLOW"]


def test_part_2_rejections_do_not_consume_capacity():
    commands = [
        "REGISTER k 1 2",
        "REQUEST 5 a k",
        "REQUEST 6 b k",
        "REQUEST 7 c k",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "DENY", "ALLOW"]


def test_part_2_error_does_not_cache_request_id():
    commands = [
        "REQUEST 0 retry missing",
        "REGISTER missing 1 5",
        "REQUEST 0 retry missing",
        "REQUEST -1 negative missing",
        "REQUEST 1 negative missing",
    ]
    assert evaluate_requests(commands) == ["ERROR", "OK", "ALLOW", "ERROR", "DENY"]


def test_part_3_request_ids_are_idempotent_and_status_is_read_only():
    commands = [
        "REGISTER k 2 5",
        "REQUEST 10 r1 k",
        "REQUEST 10 r2 k",
        "REQUEST 11 r3 k",
        "REQUEST 20 r1 k",  # cached ALLOW, but no accepted request at t=20
        "STATUS 20 k",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "ALLOW", "DENY", "ALLOW", "0/2"]


def test_part_3_denied_request_id_keeps_cached_denial_after_capacity_expires():
    commands = [
        "REGISTER k 1 2", "REQUEST 1 allowed k", "REQUEST 2 denied k",
        "REQUEST 4 denied k", "STATUS 4 k",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "DENY", "DENY", "0/1"]


def test_part_3_invalid_status_is_read_only():
    commands = ["REGISTER k 1 5", "STATUS -1 k", "STATUS 0 missing", "STATUS 0 k"]
    assert evaluate_requests(commands) == ["OK", "ERROR", "ERROR", "0/1"]


def test_part_3_request_ids_are_global_across_keys():
    commands = [
        "REGISTER a 1 5", "REGISTER b 1 5",
        "REQUEST 0 shared a", "REQUEST 0 shared b", "STATUS 0 b",
        "REQUEST 0 fresh b",
    ]
    assert evaluate_requests(commands) == [
        "OK", "OK", "ALLOW", "ALLOW", "0/1", "ALLOW"
    ]


def test_part_4_set_preserves_history_for_larger_window():
    commands = [
        "REGISTER k 3 2",
        "REQUEST 1 r1 k",
        "REQUEST 4 r2 k",
        "SET k 1 10",
        "STATUS 4 k",
        "REQUEST 5 r3 k",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "ALLOW", "OK", "2/1", "DENY"]


def test_part_4_invalid_set_does_not_mutate():
    commands = ["REGISTER k 1 10", "SET k 0 1", "REQUEST 1 r k", "REQUEST 2 s k"]
    assert evaluate_requests(commands) == ["OK", "ERROR", "ALLOW", "DENY"]


def test_part_4_shorter_window_uses_new_configuration_immediately():
    commands = [
        "REGISTER k 2 10", "REQUEST 1 a k", "REQUEST 2 b k",
        "SET k 2 1", "STATUS 2 k", "REQUEST 3 c k",
    ]
    assert evaluate_requests(commands) == ["OK", "ALLOW", "ALLOW", "OK", "1/2", "ALLOW"]


def test_part_4_set_unknown_key_is_error():
    assert evaluate_requests(["SET missing 1 1"]) == ["ERROR"]
