import csv
import hashlib
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p20_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


audit_ledger_bundle = _load().audit_ledger_bundle
FIXTURES = Path(__file__).parents[1] / "fixtures" / "basic"
ACCOUNT_HEADER = "account_id,currency,opening_balance\n"
SHARD_HEADER = "timestamp|event_id|operation|source|destination|amount\n"


def _bundle(
    root: Path,
    accounts: str,
    shards: list[tuple[int, str, str]],
    checkpoints=None,
    *,
    manifest_rows: list[tuple[object, object, object]] | None = None,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "accounts.csv").write_text(accounts, encoding="utf-8")

    calculated_rows = []
    for sequence, name, body in shards:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
        calculated_rows.append((sequence, name, hashlib.sha256(path.read_bytes()).hexdigest()))

    rows = calculated_rows if manifest_rows is None else manifest_rows
    with (root / "shards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sequence", "path", "sha256"])
        writer.writerows(rows)

    (root / "checkpoints.json").write_text(
        json.dumps([] if checkpoints is None else checkpoints), encoding="utf-8"
    )
    (root / "config.ini").write_text(
        "[ledger]\naccounts = accounts.csv\nshards = shards.csv\n"
        "checkpoints = checkpoints.json\n",
        encoding="utf-8",
    )
    return root / "config.ini"


def _row(*values: object) -> str:
    from io import StringIO

    handle = StringIO(newline="")
    csv.writer(handle, lineterminator="").writerow(values)
    return handle.getvalue()


def test_part_1_reads_complete_static_bundle():
    assert audit_ledger_bundle(FIXTURES / "config.ini") == [
        "MISMATCH,1,acct_b,25,20",
        "BALANCE,acct_a,USD,50",
        "BALANCE,acct_b,USD,20",
    ]


def test_part_1_first_valid_account_wins_and_invalid_does_not_reserve(tmp_path):
    accounts = (
        ACCOUNT_HEADER
        + "retry,USD,-1\n"
        + "retry,USD,10\n"
        + "retry,EUR,999\n"
        + "bad,Usd,5\n"
    )
    config = _bundle(tmp_path / "bundle", accounts, [])
    assert audit_ledger_bundle(config) == ["BALANCE,retry,USD,10"]


def test_part_1_credit_debit_validation_and_exact_balance(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,10\nb,USD,0\n"
    body = (
        SHARD_HEADER
        + "0|credit|CREDIT|-|b|7\n"
        + "1|too_much|DEBIT|a|-|11\n"
        + "2|exact|DEBIT|a|-|10\n"
        + "3|bad_shape|CREDIT|a|b|5\n"
    )
    config = _bundle(tmp_path / "bundle", accounts, [(1, "one.psv", body)])
    assert audit_ledger_bundle(config) == [
        "BALANCE,a,USD,0",
        "BALANCE,b,USD,7",
    ]


def test_part_2_manifest_sequence_controls_processing_order(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,0\n"
    later_sequence = SHARD_HEADER + "1|spend|DEBIT|a|-|5\n"
    earlier_sequence = SHARD_HEADER + "2|fund|CREDIT|-|a|5\n"
    config = _bundle(
        tmp_path / "bundle",
        accounts,
        [(2, "second.psv", later_sequence), (1, "first.psv", earlier_sequence)],
    )
    assert audit_ledger_bundle(config) == ["BALANCE,a,USD,0"]


def test_part_2_bad_digest_skips_whole_shard_and_does_not_reserve_event_ids(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,0\n"
    bad = SHARD_HEADER + "1|same|CREDIT|-|a|100\n"
    good = SHARD_HEADER + "2|same|CREDIT|-|a|7\n"
    root = tmp_path / "bundle"
    config = _bundle(root, accounts, [(1, "bad.psv", bad), (2, "good.psv", good)])
    rows = list(csv.reader((root / "shards.csv").read_text(encoding="utf-8").splitlines()))
    rows[1][2] = "0" * 64
    with (root / "shards.csv").open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)
    assert audit_ledger_bundle(config) == ["BALANCE,a,USD,7"]


def test_part_2_first_syntactically_valid_sequence_wins_even_if_digest_fails(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,0\n"
    first = SHARD_HEADER + "1|first|CREDIT|-|a|100\n"
    fallback = SHARD_HEADER + "2|fallback|CREDIT|-|a|7\n"
    root = tmp_path / "bundle"
    config = _bundle(root, accounts, [(1, "first.psv", first), (9, "fallback.psv", fallback)])
    digest = hashlib.sha256((root / "fallback.psv").read_bytes()).hexdigest()
    manifest_rows = [
        ("not-an-int", "ignored.psv", "bad"),
        (1, "first.psv", "0" * 64),
        (1, "fallback.psv", digest),
    ]
    with (root / "shards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sequence", "path", "sha256"])
        writer.writerows(manifest_rows)
    assert audit_ledger_bundle(config) == ["BALANCE,a,USD,0"]


def test_part_2_unsafe_core_path_returns_empty_without_output(tmp_path):
    config = _bundle(tmp_path / "bundle", ACCOUNT_HEADER + "a,USD,0\n", [])
    config.write_text(
        "[ledger]\naccounts = ../outside.csv\nshards = shards.csv\n"
        "checkpoints = checkpoints.json\n",
        encoding="utf-8",
    )
    output = tmp_path / "should-not-exist.json"
    assert audit_ledger_bundle(config, output) == []
    assert not output.exists()


def test_part_2_bad_manifest_header_returns_empty(tmp_path):
    config = _bundle(tmp_path / "bundle", ACCOUNT_HEADER + "a,USD,0\n", [])
    (config.parent / "shards.csv").write_text("path,digest\none.psv,nope\n", encoding="utf-8")
    assert audit_ledger_bundle(config) == []


def test_part_2_unsafe_shard_path_is_skipped_but_later_sequence_runs(tmp_path):
    outside = tmp_path / "outside.psv"
    outside.write_text(SHARD_HEADER + "1|x|CREDIT|-|a|100\n", encoding="utf-8")
    good = SHARD_HEADER + "2|y|CREDIT|-|a|4\n"
    root = tmp_path / "bundle"
    config = _bundle(root, ACCOUNT_HEADER + "a,USD,0\n", [(2, "good.psv", good)])
    good_digest = hashlib.sha256((root / "good.psv").read_bytes()).hexdigest()
    outside_digest = hashlib.sha256(outside.read_bytes()).hexdigest()
    with (root / "shards.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sequence", "path", "sha256"])
        writer.writerow([1, "../outside.psv", outside_digest])
        writer.writerow([2, "good.psv", good_digest])
    assert audit_ledger_bundle(config) == ["BALANCE,a,USD,4"]


def test_part_3_transfer_is_atomic_and_failed_id_can_be_retried(tmp_path):
    accounts = ACCOUNT_HEADER + "usd_a,USD,5\nusd_b,USD,0\neur,EUR,0\n"
    body = (
        SHARD_HEADER
        + "1|retry|TRANSFER|usd_a|eur|3\n"
        + "2|retry|TRANSFER|usd_a|usd_b|6\n"
        + "3|retry|TRANSFER|usd_a|usd_b|5\n"
    )
    config = _bundle(tmp_path / "bundle", accounts, [(1, "one.psv", body)])
    assert audit_ledger_bundle(config) == [
        "BALANCE,eur,EUR,0",
        "BALANCE,usd_a,USD,0",
        "BALANCE,usd_b,USD,5",
    ]


def test_part_3_successful_event_id_is_global_across_shards(tmp_path):
    accounts = ACCOUNT_HEADER + "a,USD,0\n"
    one = SHARD_HEADER + "1|same|CREDIT|-|a|4\n"
    two = SHARD_HEADER + "2|same|CREDIT|-|a|9\n"
    config = _bundle(
        tmp_path / "bundle", accounts, [(1, "one.psv", one), (2, "two.psv", two)]
    )
    assert audit_ledger_bundle(config) == ["BALANCE,a,USD,4"]


def test_part_4_checkpoints_validate_sort_and_only_follow_processed_shards(tmp_path):
    accounts = ACCOUNT_HEADER + '"acct,quoted",USD,0\nz,USD,0\n'
    one = SHARD_HEADER + "1|a|CREDIT|-|acct,quoted|5\n"
    three = SHARD_HEADER + "2|b|CREDIT|-|z|2\n"
    checkpoints = [
        {"after_sequence": True, "balances": {"z": 99}},
        {"after_sequence": 3, "balances": {"z": 99, "acct,quoted": 6}},
        {"after_sequence": 1, "balances": {"z": 1, "acct,quoted": 5}},
        {"after_sequence": 1, "balances": {"z": 999}},
        {"after_sequence": 2, "balances": {"missing": 0}},
    ]
    config = _bundle(
        tmp_path / "bundle",
        accounts,
        [(3, "three.psv", three), (1, "one.psv", one)],
        checkpoints,
    )
    assert audit_ledger_bundle(config) == [
        _row("MISMATCH", 1, "z", 1, 0),
        _row("MISMATCH", 3, "acct,quoted", 6, 5),
        _row("MISMATCH", 3, "z", 99, 2),
        _row("BALANCE", "acct,quoted", "USD", 5),
        "BALANCE,z,USD,2",
    ]


def test_part_4_writes_ordered_json_report(tmp_path):
    output = tmp_path / "nested" / "audit.json"
    rows = audit_ledger_bundle(FIXTURES / "config.ini", output)
    assert len(rows) == 3
    assert json.loads(output.read_text(encoding="utf-8")) == {
        "mismatches": [
            {
                "sequence": 1,
                "account_id": "acct_b",
                "expected": 25,
                "actual": 20,
            }
        ],
        "balances": [
            {"account_id": "acct_a", "currency": "USD", "balance": 50},
            {"account_id": "acct_b", "currency": "USD", "balance": 20},
        ],
    }


def test_part_4_malformed_checkpoints_is_a_required_bundle_failure(tmp_path):
    config = _bundle(tmp_path / "bundle", ACCOUNT_HEADER + "a,USD,0\n", [])
    (config.parent / "checkpoints.json").write_text("not json", encoding="utf-8")
    assert audit_ledger_bundle(config) == []
