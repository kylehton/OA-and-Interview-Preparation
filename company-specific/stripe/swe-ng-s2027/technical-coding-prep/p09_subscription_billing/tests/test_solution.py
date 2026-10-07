from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p09_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


generate_invoices = _load().generate_invoices


def test_part_1_full_period_base_fee_and_sorting():
    plans = ["basic,1000,100,2"]
    subscriptions = ["s2,c2,basic,1,-", "s1,c1,basic,1,30"]
    assert generate_invoices(plans, subscriptions, [], 1, 30) == [
        "s1,c1,30,0,1000", "s2,c2,30,0,1000"
    ]


def test_part_1_non_overlapping_and_invalid_subscriptions_are_ignored():
    plans = ["p,100,0,1"]
    subscriptions = ["past,c,p,1,5", "future,c,p,20,-", "bad,c,nope,1,-"]
    assert generate_invoices(plans, subscriptions, [], 10, 15) == []


def test_part_2_usage_overage():
    plans = ["p,1000,100,2"]
    subscriptions = ["s,c,p,1,30"]
    usage = ["1,u1,s,60", "30,u2,s,60"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == ["s,c,30,120,1040"]


def test_part_3_dedupes_valid_events_but_reuses_invalid_ids():
    plans = ["p,0,0,1"]
    subscriptions = ["s,c,p,1,30"]
    usage = [
        "10,same,unknown,99",  # invalid and does not reserve
        "10,same,s,5",
        "11,same,s,50",
        "31,outside,s,100",   # outside subscription lifetime, invalid
    ]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == ["s,c,30,5,5"]


def test_part_3_valid_event_outside_period_still_reserves_id():
    plans = ["p,0,0,1"]
    subscriptions = ["s,c,p,0,30"]
    usage = ["0,same,s,10", "10,same,s,99"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == ["s,c,30,0,0"]


def test_part_4_prorates_base_and_included_units():
    plans = ["pro,3000,300,2"]
    subscriptions = ["s1,c1,pro,11,20"]
    usage = ["12,u1,s1,150"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == [
        "s1,c1,10,150,1100"
    ]


def test_part_4_intersection_is_inclusive():
    plans = ["p,310,31,10"]
    subscriptions = ["s,c,p,31,31"]
    assert generate_invoices(plans, subscriptions, [], 1, 31) == ["s,c,1,0,10"]


def test_part_1_invalid_billing_interval_returns_no_invoices():
    assert generate_invoices(["p,100,0,0"], ["s,c,p,1,20"], [], 10, 9) == []


def test_part_1_first_valid_plan_wins_and_invalid_row_does_not_reserve_id():
    plans = ["p,-1,0,0", " p , 100 , 0 , 0 ", "p,999,0,0"]
    subscriptions = ["s,c,p,1,30"]
    assert generate_invoices(plans, subscriptions, [], 1, 30) == ["s,c,30,0,100"]


def test_part_1_first_valid_subscription_wins():
    plans = ["p,300,0,0"]
    subscriptions = [
        "s,c_bad,p,20,10", " s , c_1 , p , 1 , 30 ", "s,c_2,p,1,30"
    ]
    assert generate_invoices(plans, subscriptions, [], 1, 30) == ["s,c_1,30,0,300"]


def test_part_3_nonpositive_usage_does_not_reserve_event_id():
    plans = ["p,0,0,2"]
    subscriptions = ["s,c,p,1,30"]
    usage = ["10,u,s,0", "10,u,s,5"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == ["s,c,30,5,10"]


def test_part_3_usage_outside_subscription_does_not_reserve_event_id():
    plans = ["p,0,0,2"]
    subscriptions = ["s,c,p,10,20"]
    usage = ["9,u,s,5", "10,u,s,5"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == ["s,c,11,5,10"]


def test_part_3_event_ids_are_global_across_subscriptions():
    plans = ["p,0,0,2"]
    subscriptions = ["s1,c1,p,1,30", "s2,c2,p,1,30"]
    usage = ["10,shared,s1,5", "10,shared,s2,7"]
    assert generate_invoices(plans, subscriptions, usage, 1, 30) == [
        "s1,c1,30,5,10", "s2,c2,30,0,0"
    ]


def test_part_1_empty_customer_and_wrong_arity_subscriptions_are_ignored():
    plans = ["p,100,0,0"]
    subscriptions = ["empty,,p,1,30", "extra,c,p,1,30,x", "good,c,p,1,30"]
    assert generate_invoices(plans, subscriptions, [], 1, 30) == [
        "good,c,30,0,100"
    ]


def test_part_2_usage_boundaries_are_inclusive():
    plans = ["p,0,0,1"]
    subscriptions = ["s,c,p,10,20"]
    usage = ["10,start,s,2", "20,end,s,3"]
    assert generate_invoices(plans, subscriptions, usage, 10, 20) == [
        "s,c,11,5,5"
    ]


def test_part_4_base_and_included_units_are_floored_independently():
    plans = ["p,10,10,2"]
    subscriptions = ["s,c,p,2,3"]
    usage = ["2,u,s,7"]
    assert generate_invoices(plans, subscriptions, usage, 1, 3) == [
        "s,c,2,7,8"
    ]


def test_part_1_wrong_arity_plan_and_subscription_rows_do_not_reserve_ids():
    plans = ["p,10,0,0,extra", "p,10,0,0"]
    subscriptions = ["s,c,p,1,-,extra", "s,c,p,1,-"]
    assert generate_invoices(plans, subscriptions, [], 1, 1) == [
        "s,c,1,0,10"
    ]
