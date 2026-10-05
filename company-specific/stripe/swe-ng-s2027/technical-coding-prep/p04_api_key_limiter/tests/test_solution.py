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

