from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p11_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


flagged_merchants = _load().flagged_merchants


def test_part_1_count_policy_and_minimum_attempts():
    policies = ["retail,COUNT,2,3"]
    merchants = ["m1,retail", "m2,retail"]
    events = [
        "ATTEMPT,a1,m1,10,bad", "ATTEMPT,a2,m1,10,bad", "ATTEMPT,a3,m1,10,ok",
        "ATTEMPT,b1,m2,10,bad", "ATTEMPT,b2,m2,10,bad",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m1"]


def test_part_1_invalid_events_do_not_reserve_ids():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,x,missing,10,bad", "ATTEMPT,x,m,10,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_2_ratio_uses_inclusive_threshold():
    policies = ["retail,RATIO,5000,2"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,a,m,1,bad", "ATTEMPT,b,m,1,ok"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_3_clear_changes_numerator_not_denominator():
    policies = ["retail,RATIO,4000,2"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,a,m,10,bad", "ATTEMPT,b,m,10,bad", "ATTEMPT,c,m,10,ok",
        "CLEAR,clear1,a",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == []


def test_part_3_only_risky_attempt_can_be_cleared_and_ids_are_global():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,a,m,10,ok",
        "CLEAR,x,a",              # invalid, so x remains available
        "ATTEMPT,x,m,10,bad",
        "CLEAR,c,x",
        "CLEAR,d,x",              # already cleared
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == []


def test_part_4_amount_ratio_differs_from_count_ratio():
    policies = ["retail,AMOUNT_RATIO,5000,2"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,a,m,100,bad",
        "ATTEMPT,b,m,10,ok",
        "ATTEMPT,c,m,90,ok",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_4_clear_removes_risky_amount():
    policies = ["retail,AMOUNT_RATIO,3000,2"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,a,m,100,bad", "ATTEMPT,b,m,40,bad",
        "ATTEMPT,c,m,60,ok", "CLEAR,clear,a",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == []


def test_part_1_first_valid_policy_and_merchant_rows_win():
    policies = [
        "retail,COUNT,0,1", "retail,COUNT,1,1", "retail,COUNT,99,1",
        "other,COUNT,2,1",
    ]
    merchants = ["m,missing", " m , retail ", "m,other"]
    events = ["ATTEMPT,a,m,1,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_1_invalid_attempt_amount_does_not_reserve_event_id():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,same,m,0,bad", "ATTEMPT,same,m,1,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_2_zero_ratio_threshold_is_inclusive_after_minimum():
    policies = ["retail,RATIO,0,2"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,a,m,1,ok", "ATTEMPT,b,m,1,ok"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_3_successful_clear_id_blocks_later_attempt_with_same_id():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,a,m,1,bad", "CLEAR,shared,a", "ATTEMPT,shared,m,1,bad"
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == []


def test_part_1_outcomes_are_case_sensitive_and_results_are_sorted():
    policies = ["retail,COUNT,1,1"]
    merchants = ["z,retail", "a,retail", "safe,retail"]
    events = [
        "ATTEMPT,z1,z,1,bad", "ATTEMPT,a1,a,1,bad",
        "ATTEMPT,s1,safe,1,BAD",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["a", "z"]


def test_part_1_invalid_policy_bounds_do_not_reserve_category():
    policies = [
        "retail,COUNT,1,0",
        "retail,COUNT,0,1",
        "retail,COUNT,1,1",
    ]
    merchants = ["m,retail"]
    events = ["ATTEMPT,a,m,1,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_1_empty_policy_category_is_invalid():
    policies = [",COUNT,1,1", "retail,COUNT,1,1"]
    merchants = ["bad,", "good,retail"]
    events = ["ATTEMPT,a,bad,1,bad", "ATTEMPT,b,good,1,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["good"]


def test_part_2_invalid_ratio_policy_does_not_reserve_category():
    policies = ["retail,RATIO,10001,1", "retail,RATIO,5000,2"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,a,m,1,bad", "ATTEMPT,b,m,1,ok"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_1_empty_outcome_and_wrong_arity_do_not_reserve_event_id():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail"]
    events = [
        "ATTEMPT,same,m,1,",
        "ATTEMPT,same,m,1,bad,extra",
        "ATTEMPT,same,m,1,bad",
    ]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_4_amount_ratio_boundary_is_inclusive():
    policies = ["retail,AMOUNT_RATIO,2500,2"]
    merchants = ["m,retail"]
    events = ["ATTEMPT,a,m,1,bad", "ATTEMPT,b,m,3,ok"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]


def test_part_1_wrong_arity_merchant_row_does_not_reserve_id():
    policies = ["retail,COUNT,1,1"]
    merchants = ["m,retail,extra", "m,retail"]
    events = ["ATTEMPT,a,m,1,bad"]
    assert flagged_merchants(["bad"], policies, merchants, events) == ["m"]
