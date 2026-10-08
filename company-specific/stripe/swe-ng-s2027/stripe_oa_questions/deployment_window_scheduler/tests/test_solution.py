from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location(
        "deployment_window_scheduler_solution",
        Path(__file__).parents[1] / "solution.py",
    )
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


scheduleDeploymentWindows = _load().scheduleDeploymentWindows


def test_part_1_source_example_subtracts_freeze():
    rows = ["540,600,allowed", "570,585,freeze"]
    assert scheduleDeploymentWindows("part1", rows) == [
        [540, 570],
        [585, 600],
    ]


def test_part_1_empty_input_has_no_deployable_windows():
    assert scheduleDeploymentWindows("part1", []) == []


def test_part_1_allowed_window_without_freeze_is_returned():
    assert scheduleDeploymentWindows("part1", ["10,20,allowed"]) == [[10, 20]]


def test_part_1_overlapping_and_adjacent_allowed_windows_merge():
    rows = [
        "30,40,allowed",
        "10,20,allowed",
        "18,30,allowed",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [[10, 40]]


def test_part_1_disjoint_freezes_split_an_allowed_window():
    rows = [
        "0,100,allowed",
        "20,30,freeze",
        "40,50,freeze",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [
        [0, 20],
        [30, 40],
        [50, 100],
    ]


def test_part_1_overlapping_and_adjacent_freezes_act_as_one_union():
    rows = [
        "0,100,allowed",
        "20,60,freeze",
        "40,70,freeze",
        "70,80,freeze",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [[0, 20], [80, 100]]


def test_part_1_freezes_are_clipped_to_allowed_time():
    rows = [
        "20,30,allowed",
        "0,25,freeze",
        "28,40,freeze",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [[25, 28]]


def test_part_1_freeze_can_fully_cover_all_allowed_time():
    rows = ["10,20,allowed", "0,30,freeze"]
    assert scheduleDeploymentWindows("part1", rows) == []


def test_part_1_freeze_only_input_has_no_deployable_time():
    assert scheduleDeploymentWindows("part1", ["10,20,freeze"]) == []


def test_part_1_half_open_freeze_touching_allowed_end_does_not_remove_time():
    rows = ["10,20,allowed", "20,30,freeze"]
    assert scheduleDeploymentWindows("part1", rows) == [[10, 20]]


def test_part_1_freeze_splits_merged_adjacent_allowed_windows():
    rows = [
        "10,20,allowed",
        "20,30,allowed",
        "15,25,freeze",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [[10, 15], [25, 30]]


def test_part_1_week_start_and_end_boundaries_are_supported():
    rows = [
        "0,10080,allowed",
        "0,1,freeze",
        "10079,10080,freeze",
    ]
    assert scheduleDeploymentWindows("part1", rows) == [[1, 10079]]


def test_part_2_source_example_converts_offset_and_filters_duration():
    rows = [
        "1020,0,10,5",
        "540,600,allowed,-480",
        "550,565,freeze,-480",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [
        [1020, 1030],
        [1045, 1080],
    ]


def test_part_2_header_without_windows_returns_empty():
    assert scheduleDeploymentWindows("part2", ["0,0,1,5"]) == []


def test_part_2_positive_and_negative_offsets_convert_to_utc():
    rows = [
        "0,0,1,5",
        "600,660,allowed,60",
        "120,180,allowed,-480",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[540, 660]]


def test_part_2_converted_allowed_window_splits_at_week_boundary():
    rows = ["0,0,1,5", "60,180,allowed,120"]
    assert scheduleDeploymentWindows("part2", rows) == [
        [0, 60],
        [10020, 10080],
    ]


def test_part_2_positive_offset_normalizes_interval_into_end_of_week():
    rows = ["0,0,1,5", "0,60,allowed,120"]
    assert scheduleDeploymentWindows("part2", rows) == [[9960, 10020]]


def test_part_2_negative_offset_can_also_cross_week_boundary():
    rows = ["0,0,1,5", "9900,10000,allowed,-120"]
    assert scheduleDeploymentWindows("part2", rows) == [
        [0, 40],
        [10020, 10080],
    ]


def test_part_2_negative_offset_normalizes_interval_into_start_of_week():
    rows = ["0,0,1,5", "10000,10080,allowed,-120"]
    assert scheduleDeploymentWindows("part2", rows) == [[40, 120]]


def test_part_2_converted_freeze_can_cross_both_week_edges():
    rows = [
        "0,0,1,5",
        "0,10080,allowed,0",
        "60,180,freeze,120",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[60, 10020]]


def test_part_2_full_week_window_remains_full_week_after_offset():
    rows = ["0,0,1,5", "0,10080,allowed,60"]
    assert scheduleDeploymentWindows("part2", rows) == [[0, 10080]]


def test_part_2_lead_time_clips_inside_a_deployable_window():
    rows = ["100,20,10,5", "100,150,allowed,0"]
    assert scheduleDeploymentWindows("part2", rows) == [[120, 150]]


def test_part_2_lead_time_at_interval_end_discards_interval():
    rows = ["100,50,1,5", "100,150,allowed,0"]
    assert scheduleDeploymentWindows("part2", rows) == []


def test_part_2_minimum_duration_is_inclusive():
    rows = [
        "0,0,10,5",
        "10,20,allowed,0",
        "30,39,allowed,0",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[10, 20]]


def test_part_2_minimum_duration_is_checked_after_lead_time_clipping():
    rows = ["100,21,10,5", "100,130,allowed,0"]
    assert scheduleDeploymentWindows("part2", rows) == []


def test_part_2_split_boundary_pieces_must_each_meet_minimum_duration():
    rows = ["0,0,21,5", "0,40,allowed,20"]
    assert scheduleDeploymentWindows("part2", rows) == []


def test_part_2_short_fragments_created_by_freeze_are_discarded():
    rows = [
        "0,0,10,5",
        "0,100,allowed,0",
        "20,91,freeze,0",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[0, 20]]


def test_part_2_k_selects_earliest_windows_after_sorting():
    rows = [
        "0,0,1,2",
        "100,110,allowed,0",
        "0,10,allowed,0",
        "50,60,allowed,0",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[0, 10], [50, 60]]


def test_part_2_duration_filtering_happens_before_k_limit():
    rows = [
        "0,0,10,1",
        "0,5,allowed,0",
        "10,20,allowed,0",
        "30,40,allowed,0",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[10, 20]]


def test_part_2_zero_k_returns_no_windows():
    rows = ["0,0,1,0", "10,20,allowed,0"]
    assert scheduleDeploymentWindows("part2", rows) == []


def test_part_2_lead_time_at_or_beyond_week_end_returns_empty():
    at_end = ["10000,80,1,5", "0,10080,allowed,0"]
    beyond = ["10000,81,1,5", "0,10080,allowed,0"]
    assert scheduleDeploymentWindows("part2", at_end) == []
    assert scheduleDeploymentWindows("part2", beyond) == []


def test_part_2_lead_time_clips_each_split_week_boundary_piece_linearly():
    rows = ["30,0,20,5", "60,180,allowed,120"]
    assert scheduleDeploymentWindows("part2", rows) == [
        [30, 60],
        [10020, 10080],
    ]


def test_part_2_late_utc_now_discards_early_boundary_piece():
    rows = ["10050,0,20,5", "60,180,allowed,120"]
    assert scheduleDeploymentWindows("part2", rows) == [[10050, 10080]]


def test_part_2_freeze_from_one_timezone_applies_to_global_allowed_time():
    rows = [
        "0,0,1,5",
        "100,200,allowed,0",
        "160,180,freeze,60",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[120, 200]]


def test_part_2_adjacent_converted_allowed_intervals_merge_before_filtering():
    rows = [
        "0,0,100,5",
        "600,660,allowed,60",
        "120,180,allowed,-480",
    ]
    assert scheduleDeploymentWindows("part2", rows) == [[540, 660]]
