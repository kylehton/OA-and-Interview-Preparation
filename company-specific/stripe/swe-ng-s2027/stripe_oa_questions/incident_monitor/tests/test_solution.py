from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location(
        "incident_monitor_solution", Path(__file__).parents[1] / "solution.py"
    )
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


detectIncidents = _load().detectIncidents


def test_part_1_first_sample_accumulates_by_merchant_and_code():
    logs = [
        "10,merchant1,500,2",
        "10,merchant2,500,1",
        "15,merchant1,500,2",
        "20,merchant1,500,1",
        "20,merchant2,500,4",
    ]
    assert detectIncidents(logs) == [
        "20,TRIGGER,merchant1,500",
        "20,TRIGGER,merchant2,500",
    ]


def test_part_1_exactly_five_failures_in_one_row_triggers():
    assert detectIncidents(["7,merchant,500,5"]) == [
        "7,TRIGGER,merchant,500"
    ]


def test_part_1_four_failures_do_not_trigger():
    assert detectIncidents(["7,merchant,500,4"]) == []


def test_part_1_window_includes_timestamp_t_minus_29():
    logs = ["1,merchant,500,4", "30,merchant,500,1"]
    assert detectIncidents(logs) == ["30,TRIGGER,merchant,500"]


def test_part_1_window_excludes_timestamp_t_minus_30():
    logs = ["0,merchant,500,4", "30,merchant,500,1"]
    assert detectIncidents(logs) == []


def test_part_1_merchants_and_exact_error_codes_are_isolated():
    logs = [
        "1,m1,500,3",
        "2,m1,503,2",
        "3,m2,500,2",
        "4,m1,500,2",
    ]
    assert detectIncidents(logs) == ["4,TRIGGER,m1,500"]


def test_part_1_client_errors_are_failures_too():
    assert detectIncidents(["1,merchant,429,5"]) == [
        "1,TRIGGER,merchant,429"
    ]


def test_part_1_status_200_never_creates_an_alert_identity():
    assert detectIncidents(["1,merchant,200,10000"]) == []


def test_part_1_active_alert_is_not_triggered_twice():
    logs = ["1,merchant,500,5", "2,merchant,500,100"]
    assert detectIncidents(logs) == ["1,TRIGGER,merchant,500"]


def test_part_1_empty_input_has_no_events():
    assert detectIncidents([]) == []


def test_part_2_second_sample_uses_strict_one_percent_rule():
    logs = [
        "10,merchant1,200,600",
        "12,merchant1,500,6",
        "15,merchant2,200,599",
        "16,merchant2,500,6",
    ]
    assert detectIncidents(logs) == ["16,TRIGGER,merchant2,500"]


def test_part_2_exactly_one_percent_fails_but_just_over_triggers():
    logs = [
        "1,exact,200,500",
        "2,exact,500,5",
        "3,over,200,499",
        "4,over,500,5",
    ]
    assert detectIncidents(logs) == ["4,TRIGGER,over,500"]


def test_part_2_zero_success_volume_satisfies_impact_condition():
    assert detectIncidents(["1,merchant,500,5"]) == [
        "1,TRIGGER,merchant,500"
    ]


def test_part_2_success_counts_accumulate_across_the_window():
    logs = [
        "0,merchant,200,250",
        "10,merchant,200,250",
        "29,merchant,500,5",
    ]
    assert detectIncidents(logs) == []


def test_part_2_failure_counts_for_different_codes_do_not_combine():
    logs = [
        "0,merchant,200,1000",
        "1,merchant,500,5",
        "2,merchant,503,6",
    ]
    assert detectIncidents(logs) == []


def test_part_2_success_volume_is_scoped_to_merchant():
    logs = ["1,large,200,10000", "2,other,500,5"]
    assert detectIncidents(logs) == ["2,TRIGGER,other,500"]


def test_part_2_integer_comparison_handles_large_exact_boundary():
    logs = [
        "1,exact,200,1000000000",
        "2,exact,500,10000000",
        "3,over,200,999999999",
        "4,over,500,10000000",
    ]
    assert detectIncidents(logs) == ["4,TRIGGER,over,500"]


def test_part_3_failure_expiry_resolves_after_but_not_at_inclusive_boundary():
    logs = [
        "1,merchant,500,5",
        "30,merchant,200,1",
        "31,merchant,200,1",
    ]
    assert detectIncidents(logs) == [
        "1,TRIGGER,merchant,500",
        "31,RESOLVE,merchant,500",
    ]


def test_part_3_dropping_from_five_failures_to_four_resolves():
    logs = [
        "0,merchant,500,1",
        "1,merchant,500,4",
        "30,merchant,200,1",
    ]
    assert detectIncidents(logs) == [
        "1,TRIGGER,merchant,500",
        "30,RESOLVE,merchant,500",
    ]


def test_part_3_unrelated_merchant_does_not_cause_resolution():
    logs = ["0,merchant,500,5", "30,other,200,1"]
    assert detectIncidents(logs) == ["0,TRIGGER,merchant,500"]


def test_part_3_different_error_code_for_same_merchant_can_resolve_alert():
    logs = ["0,merchant,500,5", "30,merchant,503,1"]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "30,RESOLVE,merchant,500",
    ]


def test_part_3_success_volume_can_resolve_an_active_alert():
    logs = ["0,merchant,500,5", "1,merchant,200,500"]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "1,RESOLVE,merchant,500",
    ]


def test_part_3_resolution_is_not_emitted_twice():
    logs = [
        "0,merchant,500,5",
        "30,merchant,200,1",
        "31,merchant,200,1",
    ]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "30,RESOLVE,merchant,500",
    ]


def test_part_3_resolved_alert_can_trigger_again():
    logs = [
        "0,merchant,500,5",
        "30,merchant,200,1",
        "31,merchant,500,5",
    ]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "30,RESOLVE,merchant,500",
        "31,TRIGGER,merchant,500",
    ]


def test_part_3_alerts_for_two_error_codes_resolve_independently():
    logs = [
        "0,merchant,500,5",
        "1,merchant,503,5",
        "30,merchant,200,1",
        "31,merchant,200,1",
    ]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "1,TRIGGER,merchant,503",
        "30,RESOLVE,merchant,500",
        "31,RESOLVE,merchant,503",
    ]


def test_part_3_same_timestamp_rows_are_evaluated_in_input_order():
    logs = ["10,merchant,500,5", "10,merchant,200,500"]
    assert detectIncidents(logs) == [
        "10,RESOLVE,merchant,500",
        "10,TRIGGER,merchant,500",
    ]


def test_part_3_reversing_same_timestamp_rows_changes_transitions():
    logs = ["10,merchant,200,500", "10,merchant,500,5"]
    assert detectIncidents(logs) == []


def test_part_3_resolve_sorts_before_retrigger_for_same_pair_and_timestamp():
    logs = [
        "0,merchant,500,5",
        "30,merchant,200,1",
        "30,merchant,500,5",
    ]
    assert detectIncidents(logs) == [
        "0,TRIGGER,merchant,500",
        "30,RESOLVE,merchant,500",
        "30,TRIGGER,merchant,500",
    ]


def test_part_3_output_is_sorted_independently_of_emission_order():
    logs = [
        "10,z_merchant,503,5",
        "10,a_merchant,500,5",
        "10,a_merchant,400,5",
    ]
    assert detectIncidents(logs) == [
        "10,TRIGGER,a_merchant,400",
        "10,TRIGGER,a_merchant,500",
        "10,TRIGGER,z_merchant,503",
    ]


def test_part_3_expired_success_volume_can_trigger_on_a_later_success_row():
    logs = [
        "0,merchant,200,500",
        "1,merchant,500,5",
        "30,merchant,200,1",
    ]
    assert detectIncidents(logs) == ["30,TRIGGER,merchant,500"]
