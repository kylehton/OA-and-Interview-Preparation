from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p15_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


process_marketplace = _load().process_marketplace


def test_part_1_capture_requires_exact_splits():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 100",
        "SPLIT p a 60", "CAPTURE p", "SPLIT p b 40", "CAPTURE p",
        "BALANCE a", "BALANCE b",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OK", "OK", "60", "40"
    ]


def test_part_1_rejects_duplicate_recipient_and_overallocation():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 10",
        "SPLIT p a 6", "SPLIT p a 1", "SPLIT p b 5", "SPLIT p b 4",
        "CAPTURE p",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "ERROR", "OK", "OK"
    ]


def test_part_2_payout_idempotency_and_failed_id_retry():
    commands = [
        "ACCOUNT a", "CREATE p 50", "SPLIT p a 50", "CAPTURE p",
        "PAYOUT out a 60", "PAYOUT out a 20", "PAYOUT out a 1", "BALANCE a",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OK", "ERROR", "30"
    ]


def test_part_3_refund_allocates_in_reverse_split_order():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 100",
        "SPLIT p a 60", "SPLIT p b 40", "CAPTURE p",
        "REFUND r1 p 50", "BALANCE a", "BALANCE b", "STATUS p",
        "REFUND r2 p 50", "STATUS p",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "OK", "OK", "OK",
        "50", "0", "PARTIAL,100,50", "OK", "REFUNDED,100,0",
    ]


def test_part_3_failed_multi_account_refund_is_fully_atomic():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 100",
        "SPLIT p a 60", "SPLIT p b 40", "CAPTURE p",
        "PAYOUT out a 60", "REFUND r p 50", "BALANCE a", "BALANCE b", "STATUS p",
    ]
    assert process_marketplace(commands)[-4:] == [
        "ERROR", "0", "40", "CAPTURED,100,100"
    ]


def test_part_4_dispute_can_make_balances_negative():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 100",
        "SPLIT p a 60", "SPLIT p b 40", "CAPTURE p",
        "PAYOUT oa a 60", "PAYOUT ob b 40",
        "DISPUTE d p 50", "BALANCE a", "BALANCE b", "STATUS p",
    ]
    assert process_marketplace(commands)[-4:] == [
        "OK", "-10", "-40", "PARTIAL,100,50"
    ]


def test_part_4_any_dispute_makes_zero_state_disputed():
    commands = [
        "ACCOUNT a", "CREATE p 20", "SPLIT p a 20", "CAPTURE p",
        "REFUND r p 5", "DISPUTE d p 15", "STATUS p",
    ]
    assert process_marketplace(commands)[-1] == "DISPUTED,20,0"

