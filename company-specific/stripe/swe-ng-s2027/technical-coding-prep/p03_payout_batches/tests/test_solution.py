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


def test_part_2_idempotency_and_invalid_events():
    events = [
        "PAYMENT,x,m,usd,100",       # invalid currency; x remains available
        "PAYMENT,x,m,USD,40",
        "PAYMENT,x,m,USD,900",
        "PAYMENT,y,m,USD,-1",
        "broken",
    ]
    assert create_payout_batches(events) == ["m,USD,1,40"]


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

