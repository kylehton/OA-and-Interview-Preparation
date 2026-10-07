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


def test_part_1_invalid_account_does_not_reserve_id_and_duplicate_fails():
    commands = [
        "ACCOUNT m -1 0", "ACCOUNT m 0 10001", "ACCOUNT m 0 10000",
        "ACCOUNT m 0 0",
        "CHARGE 0 c m 10", "BALANCE 0 m",
    ]
    assert process_settlements(commands) == [
        "ERROR", "ERROR", "OK", "ERROR", "OK", "0,0,10"
    ]


def test_part_1_exact_command_arity_is_required_without_reserving_ids():
    commands = [
        "ACCOUNT m 10 0 extra", "ACCOUNT m 10 0",
        "CHARGE 0 c m 10 extra", "CHARGE 0 c m 10",
        "BALANCE 0 m extra", "BALANCE 0 m",
    ]
    assert process_settlements(commands) == [
        "ERROR", "OK", "ERROR", "OK", "ERROR", "10,0,0"
    ]


def test_part_3_failed_payout_id_is_reusable_after_release():
    commands = [
        "ACCOUNT m 10 0", "PAYOUT 0 payout m 10", "CHARGE 0 charge m 10",
        "PAYOUT 10 payout m 10", "BALANCE 10 m",
    ]
    assert process_settlements(commands) == [
        "OK", "ERROR", "OK", "OK", "0,0,0"
    ]


def test_part_4_mutation_ids_share_one_global_namespace():
    commands = [
        "ACCOUNT m 0 0", "CHARGE 0 shared m 100",
        "PAYOUT 0 shared m 1", "PAYOUT 0 operation m 10",
        "REFUND 0 operation shared 1", "BALANCE 0 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "ERROR", "OK", "ERROR", "0,0,90"
    ]


def test_part_4_refund_cap_is_per_charge_and_failed_id_is_reusable():
    commands = [
        "ACCOUNT m 0 0", "CHARGE 0 target m 10", "CHARGE 0 other m 100",
        "REFUND 0 refund target 11", "BALANCE 0 m",
        "REFUND 0 refund target 10", "BALANCE 0 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "ERROR", "0,0,110", "OK", "0,0,100"
    ]


def test_part_4_post_release_refund_uses_available_before_own_reserve():
    commands = [
        "ACCOUNT m 10 5000", "CHARGE 0 c m 100", "PAYOUT 10 p m 30",
        "REFUND 11 r c 60", "BALANCE 11 m", "BALANCE 20 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "OK", "0,10,0", "0,0,10"
    ]


def test_part_4_refund_at_first_release_boundary_is_not_pending():
    commands = [
        "ACCOUNT m 10 5000", "CHARGE 0 c m 100",
        "REFUND 10 r c 60", "BALANCE 10 m", "BALANCE 20 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "0,40,0", "0,0,40"
    ]


def test_part_4_refund_at_second_release_uses_only_available():
    commands = [
        "ACCOUNT m 10 5000", "CHARGE 0 c m 100", "PAYOUT 20 p m 60",
        "REFUND 20 too_much c 50", "REFUND 20 exact c 40", "BALANCE 20 m",
    ]
    assert process_settlements(commands) == [
        "OK", "OK", "OK", "ERROR", "OK", "0,0,0"
    ]


def test_part_1_negative_timestamp_is_invalid_and_does_not_reserve_id():
    commands = [
        "ACCOUNT m 10 0", "CHARGE -1 same m 10", "CHARGE 0 same m 10"
    ]
    assert process_settlements(commands) == ["OK", "ERROR", "OK"]


def test_part_3_due_releases_happen_before_an_invalid_time_command():
    commands = [
        "ACCOUNT m 10 2000", "CHARGE 0 c m 100",
        "PAYOUT 10 invalid m 0", "BALANCE 10 m",
    ]
    assert process_settlements(commands) == ["OK", "OK", "ERROR", "0,20,80"]
