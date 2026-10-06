import csv
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p16_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


build_balance_report = _load().build_balance_report
FIXTURES = Path(__file__).parents[1] / "fixtures" / "basic"
HEADER = "transaction_id,account_id,currency,kind,amount,related_id\n"


def _bundle(
    root: Path,
    files: dict[str, str],
    *,
    listed: list[str] | None = None,
    minimum_abs_net: int = 0,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    for name, content in files.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = {
        "files": listed if listed is not None else list(files),
        "minimum_abs_net": minimum_abs_net,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    return manifest_path


def test_part_1_reads_multiple_files_and_sorts_csv_output():
    assert build_balance_report(FIXTURES / "manifest.json") == [
        '"acct,quoted",EUR,50,0,50',
        "acct_a,USD,100,30,70",
        "acct_b,USD,30,0,30",
    ]


def test_part_1_debits_can_produce_a_negative_net(tmp_path):
    manifest = _bundle(
        tmp_path / "bundle",
        {"batch.csv": HEADER + "d1,a,USD,DEBIT,25,\n"},
    )
    assert build_balance_report(manifest) == ["a,USD,0,25,-25"]


def test_part_1_currency_is_uppercase_ascii_and_fields_are_trimmed(tmp_path):
    rows = (
        HEADER
        + "retry,a,ÉUR,CREDIT,10,\n"
        + "retry, a , USD , CREDIT , 10 , \n"
        + "lower,b,usd,CREDIT,20,\n"
    )
    manifest = _bundle(tmp_path / "bundle", {"batch.csv": rows})
    assert build_balance_report(manifest) == ["a,USD,10,0,10"]


def test_part_2_bad_header_skips_whole_file_without_reserving_ids(tmp_path):
    manifest = _bundle(
        tmp_path / "bundle",
        {
            "bad.csv": "transaction_id,account_id\nshared,a\n",
            "good.csv": HEADER + "shared,a,USD,CREDIT,10,\n",
        },
    )
    assert build_balance_report(manifest) == ["a,USD,10,0,10"]


def test_part_2_invalid_row_does_not_reserve_id_and_duplicate_file_is_idempotent(tmp_path):
    manifest = _bundle(
        tmp_path / "bundle",
        {
            "batch.csv": (
                HEADER
                + "retry,a,U$D,CREDIT,10,\n"
                + "retry,a,USD,CREDIT,10,\n"
                + "zero,a,USD,CREDIT,0,\n"
            )
        },
        listed=["batch.csv", "batch.csv"],
    )
    assert build_balance_report(manifest) == ["a,USD,10,0,10"]


def test_part_2_unsafe_path_and_malformed_manifest_are_ignored(tmp_path):
    outside = tmp_path / "outside.csv"
    outside.write_text(HEADER + "x,a,USD,CREDIT,10,\n", encoding="utf-8")
    bundle = tmp_path / "bundle"
    unsafe = _bundle(bundle, {}, listed=["../outside.csv"])
    assert build_balance_report(unsafe) == []

    malformed = bundle / "broken.json"
    malformed.write_text("{not json", encoding="utf-8")
    output = tmp_path / "should_not_exist.csv"
    assert build_balance_report(malformed, output) == []
    assert not output.exists()


def test_part_2_boolean_threshold_makes_manifest_invalid(tmp_path):
    manifest = _bundle(
        tmp_path / "bundle",
        {"batch.csv": HEADER + "c,a,USD,CREDIT,10,\n"},
    )
    manifest.write_text(
        json.dumps({"files": ["batch.csv"], "minimum_abs_net": True}),
        encoding="utf-8",
    )
    assert build_balance_report(manifest) == []


def test_part_3_reverses_credit_and_debit_gross_totals(tmp_path):
    rows = (
        HEADER
        + "c,a,USD,CREDIT,100,\n"
        + "d,a,USD,DEBIT,30,\n"
        + "rd,,,REVERSAL,,d\n"
        + "rc,,,REVERSAL,,c\n"
        + "other,a,USD,CREDIT,5,\n"
    )
    manifest = _bundle(tmp_path / "bundle", {"batch.csv": rows})
    assert build_balance_report(manifest) == ["a,USD,5,0,5"]


def test_part_3_reversal_can_reference_an_earlier_file(tmp_path):
    manifest = _bundle(
        tmp_path / "bundle",
        {
            "first.csv": HEADER + "c,a,USD,CREDIT,10,\n",
            "second.csv": HEADER + "r,,,REVERSAL,,c\n",
        },
    )
    assert build_balance_report(manifest) == []


def test_part_3_failed_reversal_id_is_reusable(tmp_path):
    rows = (
        HEADER
        + "retry,,,REVERSAL,,missing\n"
        + "c,a,USD,CREDIT,10,\n"
        + "retry,,,REVERSAL,,c\n"
    )
    manifest = _bundle(tmp_path / "bundle", {"batch.csv": rows})
    assert build_balance_report(manifest) == []


def test_part_3_reversal_cannot_be_reversed(tmp_path):
    rows = (
        HEADER
        + "c,a,USD,CREDIT,10,\n"
        + "r1,,,REVERSAL,,c\n"
        + "r2,,,REVERSAL,,r1\n"
        + "remaining,a,USD,CREDIT,1,\n"
    )
    manifest = _bundle(tmp_path / "bundle", {"batch.csv": rows})
    assert build_balance_report(manifest) == ["a,USD,1,0,1"]


def test_part_4_absolute_threshold_is_inclusive(tmp_path):
    rows = (
        HEADER
        + "d,a,USD,DEBIT,50,\n"
        + "c,b,USD,CREDIT,49,\n"
    )
    manifest = _bundle(
        tmp_path / "bundle",
        {"batch.csv": rows},
        minimum_abs_net=50,
    )
    assert build_balance_report(manifest) == ["a,USD,0,50,-50"]


def test_part_4_writes_header_and_exact_returned_rows(tmp_path):
    output = tmp_path / "nested" / "report.csv"
    rows = build_balance_report(FIXTURES / "manifest.json", output)

    with output.open(newline="", encoding="utf-8") as handle:
        parsed = list(csv.reader(handle))

    assert parsed[0] == [
        "account_id", "currency", "credit_total", "debit_total", "net_amount"
    ]
    assert parsed[1:] == [
        ["acct,quoted", "EUR", "50", "0", "50"],
        ["acct_a", "USD", "100", "30", "70"],
        ["acct_b", "USD", "30", "0", "30"],
    ]
    assert len(rows) == 3
