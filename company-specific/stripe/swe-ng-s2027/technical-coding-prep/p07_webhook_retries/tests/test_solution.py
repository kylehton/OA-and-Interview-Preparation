from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p07_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


plan_deliveries = _load().plan_deliveries


def test_part_1_successful_pair_needs_no_retry():
    endpoints = ["ep,5,60"]
    attempts = ["10,a1,e1,ep,500", "20,a2,e1,ep,204"]
    assert plan_deliveries(endpoints, attempts, 5) == []


def test_part_1_invalid_attempts_and_endpoints_are_ignored():
    endpoints = ["ep,0,10", "ep,2,10"]
    attempts = ["x,a,e,ep,500", "1,b,e,missing,500", "2,c,e,ep,700"]
    assert plan_deliveries(endpoints, attempts, 3) == []


def test_part_2_exponential_backoff_uses_chronological_latest():
    endpoints = ["ep,5,12"]
    attempts = ["20,a2,e,ep,500", "10,a1,e,ep,503"]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,e,ep,30,2"]


def test_part_2_retry_sorting():
    endpoints = ["x,3,10", "y,1,10"]
    attempts = ["5,a,z,x,500", "6,b,a,y,500"]
    assert plan_deliveries(endpoints, attempts, 5) == [
        "RETRY,a,y,7,1", "RETRY,z,x,8,1"
    ]


def test_part_3_retry_after_can_extend_but_not_shorten_backoff():
    endpoints = ["ep,5,100"]
    attempts = [
        "10,a1,long,ep,429,30",
        "10,a2,short,ep,429,2",
    ]
    assert plan_deliveries(endpoints, attempts, 5) == [
        "RETRY,short,ep,15,1",
        "RETRY,long,ep,40,1",
    ]


def test_part_4_duplicate_attempt_ids_and_dead_letters():
    endpoints = ["ep,2,10"]
    attempts = [
        "1,same,e1,ep,500",
        "2,same,e1,ep,500",  # duplicate does not count
        "3,a2,e1,ep,500",
        "4,a3,e1,ep,500",
        "5,b1,e2,ep,500",
    ]
    assert plan_deliveries(endpoints, attempts, 3) == [
        "RETRY,e2,ep,7,1",
        "DEAD,e1,ep,3",
    ]


def test_part_4_invalid_duplicate_does_not_reserve_id():
    endpoints = ["ep,2,10"]
    attempts = ["bad,x,e,ep,500", "3,x,e,ep,500"]
    assert plan_deliveries(endpoints, attempts, 3) == ["RETRY,e,ep,5,1"]


def test_part_1_first_valid_endpoint_wins_and_fields_are_trimmed():
    endpoints = [" ep , 0 , 8 ", " ep , 1 , 8 ", "ep,4,8"]
    attempts = [" 10 , a , event , ep , 500 "]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,event,ep,11,1"]


def test_part_2_exponential_delay_is_capped():
    endpoints = ["ep,3,10"]
    attempts = [
        "1,a1,event,ep,500",
        "2,a2,event,ep,500",
        "3,a3,event,ep,500",
    ]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,event,ep,13,3"]


def test_part_2_equal_timestamps_use_later_input_row():
    endpoints = ["ep,2,20"]
    attempts = [
        "10,a1,event,ep,500",
        "10,a2,event,ep,429,15",
    ]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,event,ep,25,2"]


def test_part_3_sixth_field_only_valid_for_429_and_invalid_row_does_not_reserve_id():
    endpoints = ["ep,2,20"]
    attempts = ["10,a,event,ep,500,7", "11,a,event,ep,500"]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,event,ep,13,1"]


def test_part_4_any_success_completes_even_if_a_later_attempt_failed():
    endpoints = ["ep,2,20"]
    attempts = ["10,a1,event,ep,204", "20,a2,event,ep,500"]
    assert plan_deliveries(endpoints, attempts, 5) == []


def test_part_4_attempt_ids_are_global_across_event_endpoint_pairs():
    endpoints = ["ep,2,20"]
    attempts = ["10,shared,e1,ep,500", "100,shared,e2,ep,500"]
    assert plan_deliveries(endpoints, attempts, 5) == ["RETRY,e1,ep,12,1"]
