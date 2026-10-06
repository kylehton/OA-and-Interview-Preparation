import csv
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p19_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


schedule_payout_files = _load().schedule_payout_files
FIXTURES = Path(__file__).parents[1] / "fixtures" / "basic"
ACCOUNT_HEADER = "merchant_id,currency,delay_business_days,cutoff_utc_hour\n"
CAPTURE_HEADER = "capture_id\tmerchant_id\tcurrency\tamount\tcaptured_at\n"


def _files(
    root: Path,
    accounts: str,
    captures: str,
    holidays: str = "",
) -> tuple[Path, Path, Path]:
    root.mkdir(parents=True, exist_ok=True)
    account_path = root / "accounts.csv"
    capture_path = root / "captures.tsv"
    holiday_path = root / "holidays.txt"
    account_path.write_text(accounts, encoding="utf-8")
    capture_path.write_text(captures, encoding="utf-8")
    holiday_path.write_text(holidays, encoding="utf-8")
    return account_path, capture_path, holiday_path


def test_part_1_reads_csv_tsv_and_text_fixture():
    assert schedule_payout_files(
        FIXTURES / "accounts.csv",
        FIXTURES / "captures.tsv",
        FIXTURES / "holidays.txt",
    ) == [
        "2026-01-06,m1,USD,1,100",
        "2026-01-07,m1,USD,1,50",
        '2026-01-13,"m,quoted",EUR,1,20',
    ]


def test_part_1_groups_same_settlement_merchant_and_currency(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,23\n"
    captures = (
        CAPTURE_HEADER
        + "a\tm\tUSD\t10\t2026-01-05T10:00:00Z\n"
        + "b\tm\tUSD\t20\t2026-01-05T11:00:00Z\n"
    )
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,m,USD,2,30"]


def test_part_1_first_valid_account_configuration_wins(tmp_path):
    accounts = (
        ACCOUNT_HEADER
        + "m,USD,-1,10\n"
        + "m,USD,0,10\n"
        + "m,USD,5,10\n"
    )
    captures = CAPTURE_HEADER + "a\tm\tUSD\t10\t2026-01-05T09:00:00Z\n"
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,m,USD,1,10"]


def test_part_2_offset_is_converted_to_utc_before_cutoff(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,10\n"
    captures = CAPTURE_HEADER + "a\tm\tUSD\t10\t2026-01-05T11:00:00+02:00\n"
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,m,USD,1,10"]


def test_part_2_timestamp_requires_seconds_and_an_explicit_offset(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,23\n"
    captures = (
        CAPTURE_HEADER
        + "retry\tm\tUSD\t10\t2026-01-05T10:00Z\n"
        + "retry\tm\tUSD\t10\t2026-01-05T10:00:00\n"
        + "retry\tm\tUSD\t10\t2026-01-05T10:00:00Z\n"
    )
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,m,USD,1,10"]


def test_part_2_exact_cutoff_moves_to_next_calendar_day_then_rolls(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,17\n"
    captures = CAPTURE_HEADER + "a\tm\tUSD\t10\t2026-01-09T17:00:00Z\n"
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-12,m,USD,1,10"]


def test_part_3_delay_skips_weekend_and_holiday(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,1,23\n"
    captures = CAPTURE_HEADER + "a\tm\tUSD\t10\t2026-01-09T10:00:00Z\n"
    paths = _files(
        tmp_path / "bundle",
        accounts,
        captures,
        "bad-date\n2026-01-12\n2026-01-12\n",
    )
    assert schedule_payout_files(*paths) == ["2026-01-13,m,USD,1,10"]


def test_part_3_zero_delay_rolls_weekend_and_holiday_base_date(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,23\n"
    captures = CAPTURE_HEADER + "a\tm\tUSD\t10\t2026-01-10T10:00:00Z\n"
    paths = _files(tmp_path / "bundle", accounts, captures, "2026-01-12\n")
    assert schedule_payout_files(*paths) == ["2026-01-13,m,USD,1,10"]


def test_part_4_invalid_capture_does_not_reserve_id(tmp_path):
    accounts = ACCOUNT_HEADER + "m,USD,0,23\n"
    captures = (
        CAPTURE_HEADER
        + "retry\tm\tUSD\t0\t2026-01-05T10:00:00Z\n"
        + "retry\tm\tUSD\t10\t2026-01-05T10:00:00\n"
        + "retry\tm\tUSD\t10\t2026-01-05T10:00:00Z\n"
    )
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,m,USD,1,10"]


def test_part_4_duplicate_capture_id_is_global(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,0,23\nb,USD,0,23\n"
    captures = (
        CAPTURE_HEADER
        + "same\ta\tUSD\t10\t2026-01-05T10:00:00Z\n"
        + "same\tb\tUSD\t20\t2026-01-05T10:00:00Z\n"
    )
    paths = _files(tmp_path / "bundle", accounts, captures)
    assert schedule_payout_files(*paths) == ["2026-01-05,a,USD,1,10"]


def test_part_4_bad_header_returns_empty_without_writing_output(tmp_path):
    paths = _files(
        tmp_path / "bundle",
        "wrong,header\na,b\n",
        CAPTURE_HEADER,
    )
    output = tmp_path / "report.csv"
    assert schedule_payout_files(*paths, output) == []
    assert not output.exists()


def test_part_4_missing_required_holiday_file_returns_empty(tmp_path):
    paths = _files(
        tmp_path / "bundle",
        ACCOUNT_HEADER + "m,USD,0,23\n",
        CAPTURE_HEADER,
    )
    paths[2].unlink()
    assert schedule_payout_files(*paths) == []


def test_part_4_writes_quoted_csv_output(tmp_path):
    output = tmp_path / "nested" / "report.csv"
    rows = schedule_payout_files(
        FIXTURES / "accounts.csv",
        FIXTURES / "captures.tsv",
        FIXTURES / "holidays.txt",
        output,
    )
    with output.open(newline="", encoding="utf-8") as handle:
        parsed = list(csv.reader(handle))
    assert parsed[0] == [
        "settlement_date", "merchant_id", "currency", "capture_count", "total_amount"
    ]
    assert parsed[-1] == ["2026-01-13", "m,quoted", "EUR", "1", "20"]
    assert len(rows) == 3
