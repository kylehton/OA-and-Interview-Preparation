from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p14_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


process_settlements = _load().process_settlements


def test_part_1_charge_starts_pending():
    commands = ["ACCOUNT m 10 2000", "CHARGE 0 c1 m 100", "BALANCE 0 m"]
    assert process_settlements(commands) == ["OK", "OK", "100,0,0"]


def test_part_1_invalid_operation_id_can_be_retried():
    commands = ["CHARGE 0 x missing 10", "ACCOUNT m 1 0", "CHARGE 0 x m 10"]
    assert process_settlements(commands) == ["ERROR", "OK", "OK"]


def test_part_2_both_release_boundaries_are_inclusive():
    commands = [
        "ACCOUNT m 10 2000", "CHARGE 0 c1 m 101",
        "BALANCE 9 m", "BALANCE 10 m", "BALANCE 20 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "101,0,0", "0,21,80", "0,0,101"
    ]


def test_part_2_zero_hold_releases_immediately():
    commands = ["ACCOUNT m 0 2500", "CHARGE 5 c m 40", "BALANCE 5 m"]
    assert process_settlements(commands) == ["OK", "OK", "0,0,40"]


def test_part_3_payout_only_uses_available_money():
    commands = [
        "ACCOUNT m 10 2000", "CHARGE 0 c m 100",
        "PAYOUT 9 early m 1", "PAYOUT 10 p m 80", "BALANCE 10 m",
    ]
    assert process_settlements(commands) == ["OK", "OK", "ERROR", "OK", "0,20,0"]


def test_part_4_pending_refund_changes_later_split():
    commands = [
        "ACCOUNT m 10 2000", "CHARGE 0 c m 100", "REFUND 5 r c 30",
        "BALANCE 5 m", "BALANCE 10 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "70,0,0", "0,14,56"
    ]


def test_part_4_post_release_refund_uses_available_then_own_reserve():
    commands = [
        "ACCOUNT m 10 2000", "CHARGE 0 c m 100", "PAYOUT 10 p m 80",
        "REFUND 11 too_big c 30", "REFUND 12 exact c 20", "BALANCE 20 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "ERROR", "OK", "0,0,0"
    ]

