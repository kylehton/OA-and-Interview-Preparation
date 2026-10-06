from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p03_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


create_payout_batches = _load().create_payout_batches


def test_part_1_aggregates_and_sorts_groups():
    events = [
        "PAYMENT,p1,z_shop,USD,50",
        "PAYMENT,p2,a_shop,EUR,20",
        "PAYMENT,p3,z_shop,USD,25",
    ]
    assert create_payout_batches(events) == ["a_shop,EUR,1,20", "z_shop,USD,1,75"]


def test_part_1_trims_fields_and_keeps_currency_groups_separate():
    events = [
        " PAYMENT , p1 , merchant , USD , 10 ",
        "PAYMENT,p2,merchant,EUR,20",
    ]
    assert create_payout_batches(events) == [
        "merchant,EUR,1,20", "merchant,USD,1,10"
    ]


def test_part_2_idempotency_and_invalid_events():
    events = [
        "PAYMENT,x,m,usd,100",       # invalid currency; x remains available
        "PAYMENT,x,m,USD,40",
        "PAYMENT,x,m,USD,900",
        "PAYMENT,y,m,USD,-1",
        "broken",
    ]
    assert create_payout_batches(events) == ["m,USD,1,40"]


def test_part_2_rejects_empty_ids_and_merchants():
    events = [
        "PAYMENT,,m,USD,100",
        "PAYMENT,p1,,USD,100",
        "PAYMENT,p2,m,US,100",
        "PAYMENT,p3,m,USD,10",
    ]
    assert create_payout_batches(events) == ["m,USD,1,10"]


def test_part_2_zero_payment_is_invalid_and_does_not_reserve_event_id():
    events = [
        "PAYMENT,retry,m,USD,0",
        "PAYMENT,retry,m,USD,10",
    ]
    assert create_payout_batches(events) == ["m,USD,1,10"]


def test_part_2_currency_must_contain_only_uppercase_ascii_letters():
    events = [
        "PAYMENT,retry,m,U$D,10",
        "PAYMENT,retry,m,USD,10",
    ]
    assert create_payout_batches(events) == ["m,USD,1,10"]


def test_part_3_partial_refunds_and_over_refunds():
    events = [
        "PAYMENT,p1,m,USD,100",
        "REFUND,r1,p1,30",
        "REFUND,r2,p1,70",
        "REFUND,r3,p1,1",       # exceeds the payment and is ignored
        "PAYMENT,p2,m,USD,25",
        "REFUND,r4,missing,10",
    ]
    assert create_payout_batches(events) == ["m,USD,1,25"]


def test_part_3_ids_are_global_across_types():
    events = [
        "PAYMENT,p1,m,USD,100",
        "REFUND,same,p1,20",
        "PAYMENT,same,m,USD,999",
    ]
    assert create_payout_batches(events) == ["m,USD,1,80"]


def test_part_3_invalid_refund_does_not_reserve_its_event_id():
    events = [
        "PAYMENT,p1,m,USD,100",
        "REFUND,r1,p1,101",
        "REFUND,r1,p1,20",
    ]
    assert create_payout_batches(events) == ["m,USD,1,80"]


def test_part_3_zero_refund_is_invalid_and_does_not_reserve_event_id():
    events = [
        "PAYMENT,p1,m,USD,10",
        "REFUND,retry,p1,0",
        "REFUND,retry,p1,5",
    ]
    assert create_payout_batches(events) == ["m,USD,1,5"]


def test_part_3_refund_limit_is_scoped_to_the_referenced_payment():
    events = [
        "PAYMENT,small,m,USD,10",
        "PAYMENT,other,m,USD,100",
        "REFUND,r1,small,11",
    ]
    assert create_payout_batches(events) == ["m,USD,1,110"]


def test_part_3_fully_refunded_group_is_not_emitted():
    events = ["PAYMENT,p1,m,USD,100", "REFUND,r1,p1,100"]
    assert create_payout_batches(events) == []


def test_part_4_threshold_and_batch_splitting():
    events = [
        "PAYMENT,p1,m1,USD,250",
        "PAYMENT,p2,m1,USD,75",
        "REFUND,r1,p1,25",
        "PAYMENT,p3,m2,USD,99",
    ]
    assert create_payout_batches(events, 100, 125) == [
        "m1,USD,1,125",
        "m1,USD,2,125",
        "m1,USD,3,50",
    ]


def test_part_4_exact_multiple_has_no_empty_batch():
    assert create_payout_batches(["PAYMENT,p,m,USD,200"], 0, 100) == [
        "m,USD,1,100",
        "m,USD,2,100",
    ]


def test_part_4_threshold_is_inclusive():
    assert create_payout_batches(["PAYMENT,p,m,USD,100"], 100, 0) == [
        "m,USD,1,100"
    ]


def test_part_4_non_positive_options_mean_no_threshold_or_splitting():
    assert create_payout_batches(["PAYMENT,p,m,USD,250"], -10, -1) == [
        "m,USD,1,250"
    ]
