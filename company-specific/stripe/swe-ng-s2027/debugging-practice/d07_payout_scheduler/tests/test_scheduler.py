import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from payout_scheduler import schedule_payouts


def tx(timestamp, transaction_id, merchant="m1", currency="USD", amount=100):
    return f"{timestamp},{transaction_id},{merchant},{currency},{amount},CAPTURED"


def test_basic_business_day_delay():
    lines = [tx("2026-01-05T10:00:00Z", "t1")]  # Monday
    assert schedule_payouts(lines, 1) == ["2026-01-06,m1,USD,100"]


def test_after_cutoff_crossing_weekend():
    lines = [tx("2026-01-09T18:00:00Z", "t1")]  # Friday after cutoff
    assert schedule_payouts(lines, 1) == ["2026-01-13,m1,USD,100"]


def test_capture_exactly_at_cutoff_moves_to_next_day():
    lines = [tx("2026-01-05T17:00:00Z", "t1")]
    assert schedule_payouts(lines, 0) == ["2026-01-06,m1,USD,100"]


def test_holidays_are_not_business_days():
    lines = [tx("2026-01-05T10:00:00Z", "t1")]
    assert schedule_payouts(lines, 1, ["2026-01-06"]) == [
        "2026-01-07,m1,USD,100"
    ]


def test_offset_timestamp_is_converted_to_utc_before_cutoff_logic():
    # Monday 16:30 Pacific is Tuesday 00:30 UTC.
    lines = [tx("2026-01-05T16:30:00-08:00", "t1")]
    assert schedule_payouts(lines, 0) == ["2026-01-06,m1,USD,100"]


def test_currency_is_part_of_grouping_key():
    lines = [
        tx("2026-01-05T10:00:00Z", "t1", currency="USD", amount=100),
        tx("2026-01-05T11:00:00Z", "t2", currency="EUR", amount=200),
    ]
    assert schedule_payouts(lines, 0) == [
        "2026-01-05,m1,EUR,200",
        "2026-01-05,m1,USD,100",
    ]


def test_duplicate_and_non_captured_rows_are_ignored():
    lines = [
        tx("2026-01-05T10:00:00Z", "same", amount=100),
        tx("2026-01-05T11:00:00Z", "same", amount=900),
        "2026-01-05T12:00:00Z,x,m1,USD,500,FAILED",
    ]
    assert schedule_payouts(lines, 0) == ["2026-01-05,m1,USD,100"]

