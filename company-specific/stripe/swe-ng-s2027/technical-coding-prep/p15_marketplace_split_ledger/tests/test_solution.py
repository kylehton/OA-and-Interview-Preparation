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
        "REFUND r1 p 50", "BALANCE a", "BALANCE b",
        "REFUND r2 p 50", "BALANCE a", "BALANCE b",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "OK", "OK", "OK",
        "50", "0", "OK", "0", "0",
    ]


def test_part_3_failed_multi_account_refund_is_fully_atomic():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 100",
        "SPLIT p a 60", "SPLIT p b 40", "CAPTURE p",
        "PAYOUT out a 60", "REFUND r p 50", "BALANCE a", "BALANCE b",
    ]
    assert process_marketplace(commands)[-3:] == ["ERROR", "0", "40"]


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


def test_part_1_account_and_payment_ids_use_separate_namespaces():
    commands = [
        "ACCOUNT shared", "CREATE shared 10", "ACCOUNT shared", "CREATE shared 10",
        "SPLIT shared shared 10", "CAPTURE shared", "BALANCE shared",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "ERROR", "ERROR", "OK", "OK", "10"
    ]


def test_part_1_captured_payment_rejects_more_splits_and_second_capture():
    commands = [
        "ACCOUNT a", "ACCOUNT b", "CREATE p 10", "SPLIT p a 10", "CAPTURE p",
        "SPLIT p b 1", "CAPTURE p", "BALANCE a", "BALANCE b",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "OK", "ERROR", "ERROR",
        "10", "0",
    ]


def test_part_4_operation_ids_are_global_across_payout_refund_and_dispute():
    commands = [
        "ACCOUNT a", "CREATE p 100", "SPLIT p a 100", "CAPTURE p",
        "PAYOUT shared a 10", "REFUND shared p 10", "DISPUTE shared p 10",
        "BALANCE a", "STATUS p",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "OK", "ERROR", "ERROR",
        "90", "CAPTURED,100,100",
    ]


def test_part_2_nonpositive_payout_does_not_reserve_operation_id():
    commands = [
        "ACCOUNT a", "CREATE p 10", "SPLIT p a 10", "CAPTURE p",
        "PAYOUT payout a 0", "PAYOUT payout a 10", "BALANCE a",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OK", "0"
    ]


def test_part_3_over_refund_is_atomic_and_failed_id_is_reusable():
    commands = [
        "ACCOUNT a", "CREATE p 10", "SPLIT p a 10", "CAPTURE p",
        "REFUND refund p 11", "BALANCE a",
        "REFUND refund p 10", "BALANCE a",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "10", "OK", "0",
    ]


def test_part_4_failed_dispute_id_is_reusable():
    commands = [
        "ACCOUNT a", "CREATE p 20", "SPLIT p a 20", "CAPTURE p",
        "DISPUTE dispute p 21", "DISPUTE dispute p 20", "STATUS p",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "OK", "OK", "ERROR", "OK", "DISPUTED,20,0"
    ]


def test_part_1_wrong_arity_and_nonpositive_amounts_are_atomic():
    commands = [
        "ACCOUNT a extra", "ACCOUNT a", "CREATE p 0", "CREATE p 10",
        "SPLIT p a 0", "SPLIT p a 10", "CAPTURE p", "BALANCE a",
    ]
    assert process_marketplace(commands) == [
        "ERROR", "OK", "ERROR", "OK", "ERROR", "OK", "OK", "10"
    ]


def test_part_4_status_tracks_draft_captured_and_refunded_states():
    commands = [
        "ACCOUNT a", "CREATE p 10", "STATUS p", "SPLIT p a 10",
        "CAPTURE p", "STATUS p", "REFUND r p 10", "STATUS p",
    ]
    assert process_marketplace(commands) == [
        "OK", "OK", "DRAFT,10,10", "OK", "OK",
        "CAPTURED,10,10", "OK", "REFUNDED,10,0",
    ]
