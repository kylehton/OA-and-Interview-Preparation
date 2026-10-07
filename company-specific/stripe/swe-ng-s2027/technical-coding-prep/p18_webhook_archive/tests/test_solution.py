import csv
import gzip
import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


def _load():
    spec = spec_from_file_location("p18_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


plan_webhook_archive = _load().plan_webhook_archive
FIXTURES = Path(__file__).parents[1] / "fixtures" / "basic"
ENDPOINT_HEADER = "endpoint_id,base_delay,max_delay\n"


def _archive(
    root: Path,
    endpoints: str,
    attempts: dict[str, str],
    *,
    listed: list[str] | None = None,
    max_attempts: int = 5,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "endpoints.csv").write_text(endpoints, encoding="utf-8")
    for name, content in attempts.items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    manifest = {
        "endpoint_file": "endpoints.csv",
        "attempt_files": listed if listed is not None else list(attempts),
        "max_attempts": max_attempts,
    }
    path = root / "manifest.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return path


def _line(**values) -> str:
    return json.dumps(values, separators=(",", ":")) + "\n"


def test_part_1_reads_csv_and_jsonl_fixture():
    assert plan_webhook_archive(FIXTURES / "manifest.json") == [
        "RETRY,event_slow,ep_slow,6,1",
        "RETRY,event_retry,ep_main,12,1",
    ]


def test_part_2_first_valid_endpoint_wins(tmp_path):
    endpoints = ENDPOINT_HEADER + "ep,0,8\nep,1,8\nep,4,8\n"
    attempts = {
        "a.jsonl": _line(
            timestamp=10, attempt_id="a", event_id="event", endpoint_id="ep", status=500
        )
    }
    manifest = _archive(tmp_path / "archive", endpoints, attempts)
    assert plan_webhook_archive(manifest) == ["RETRY,event,ep,11,1"]


def test_part_1_bad_endpoint_header_or_manifest_returns_empty(tmp_path):
    manifest = _archive(
        tmp_path / "archive",
        "id,delay\nep,2\n",
        {"a.jsonl": ""},
    )
    assert plan_webhook_archive(manifest) == []
    manifest.write_text('{"endpoint_file": true}', encoding="utf-8")
    assert plan_webhook_archive(manifest) == []


def test_part_1_boolean_max_attempts_is_invalid(tmp_path):
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": ""},
    )
    manifest.write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": ["a.jsonl"],
                "max_attempts": True,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(manifest) == []


def test_part_1_unsafe_endpoint_path_is_a_required_input_failure(tmp_path):
    outside = tmp_path / "outside.csv"
    outside.write_text(ENDPOINT_HEADER + "ep,2,10\n", encoding="utf-8")
    root = tmp_path / "archive"
    root.mkdir()
    manifest = root / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "endpoint_file": "../outside.csv",
                "attempt_files": [],
                "max_attempts": 3,
            }
        ),
        encoding="utf-8",
    )
    output = tmp_path / "plan.csv"
    assert plan_webhook_archive(manifest, output) == []
    assert not output.exists()


def test_part_1_valid_successful_attempt_needs_no_recovery_row(tmp_path):
    attempts = {
        "a.jsonl": _line(
            timestamp=1,
            attempt_id="a",
            event_id="event",
            endpoint_id="ep",
            status=204,
        )
    }
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        attempts,
    )
    assert plan_webhook_archive(manifest) == []


def test_part_1_wrong_arity_endpoint_row_does_not_reserve_id(tmp_path):
    attempts = {
        "a.jsonl": _line(
            timestamp=1,
            attempt_id="a",
            event_id="event",
            endpoint_id="ep",
            status=500,
        )
    }
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10,extra\nep,2,10\n",
        attempts,
    )
    assert plan_webhook_archive(manifest) == ["RETRY,event,ep,3,1"]


def test_part_2_backoff_is_capped_and_uses_chronological_latest(tmp_path):
    attempts = "".join(
        [
            _line(timestamp=3, attempt_id="a3", event_id="e", endpoint_id="ep", status=500),
            _line(timestamp=1, attempt_id="a1", event_id="e", endpoint_id="ep", status=500),
            _line(timestamp=2, attempt_id="a2", event_id="e", endpoint_id="ep", status=500),
        ]
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,3,10\n",
        {"a.jsonl": attempts},
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,13,3"]


def test_part_3_equal_timestamps_use_later_manifest_file_and_line(tmp_path):
    first = _line(
        timestamp=10, attempt_id="a1", event_id="e", endpoint_id="ep", status=500
    )
    second = _line(
        timestamp=10,
        attempt_id="a2",
        event_id="e",
        endpoint_id="ep",
        status=429,
        retry_after=15,
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,20\n",
        {"first.jsonl": first, "second.jsonl": second},
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,25,2"]


def test_part_3_reads_gzip_jsonl(tmp_path):
    root = tmp_path / "archive"
    root.mkdir()
    (root / "endpoints.csv").write_text(ENDPOINT_HEADER + "ep,2,10\n", encoding="utf-8")
    with gzip.open(root / "attempts.jsonl.gz", "wt", encoding="utf-8") as handle:
        handle.write(
            _line(timestamp=4, attempt_id="a", event_id="e", endpoint_id="ep", status=500)
        )
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": ["attempts.jsonl.gz"],
                "max_attempts": 5,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(root / "manifest.json") == ["RETRY,e,ep,6,1"]


def test_part_3_unsafe_and_corrupt_attempt_shards_are_skipped(tmp_path):
    outside = tmp_path / "outside.jsonl"
    outside.write_text(
        _line(timestamp=1, attempt_id="outside", event_id="e", endpoint_id="ep", status=500),
        encoding="utf-8",
    )
    root = tmp_path / "archive"
    root.mkdir()
    (root / "endpoints.csv").write_text(ENDPOINT_HEADER + "ep,2,10\n", encoding="utf-8")
    (root / "broken.jsonl.gz").write_bytes(b"not gzip")
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": ["../outside.jsonl", "broken.jsonl.gz"],
                "max_attempts": 3,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(root / "manifest.json") == []


def test_part_3_attempt_symlink_escape_is_skipped_without_reserving_ids(tmp_path):
    outside = tmp_path / "outside.jsonl"
    outside.write_text(
        _line(timestamp=1, attempt_id="same", event_id="outside", endpoint_id="ep", status=500),
        encoding="utf-8",
    )
    root = tmp_path / "archive"
    root.mkdir()
    (root / "endpoints.csv").write_text(ENDPOINT_HEADER + "ep,2,10\n", encoding="utf-8")
    try:
        (root / "linked.jsonl").symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are not available on this platform")
    (root / "good.jsonl").write_text(
        _line(timestamp=2, attempt_id="same", event_id="good", endpoint_id="ep", status=500),
        encoding="utf-8",
    )
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": ["linked.jsonl", "good.jsonl"],
                "max_attempts": 5,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(root / "manifest.json") == ["RETRY,good,ep,4,1"]


def test_part_3_invalid_lines_do_not_reserve_attempt_ids(tmp_path):
    attempts = (
        "not json\n"
        + _line(timestamp="bad", attempt_id="same", event_id="e", endpoint_id="ep", status=500)
        + _line(timestamp=5, attempt_id="same", event_id="e", endpoint_id="ep", status=500)
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": attempts},
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,7,1"]


def test_part_3_retry_after_on_non_429_is_invalid_and_id_is_reusable(tmp_path):
    attempts = (
        _line(
            timestamp=1,
            attempt_id="same",
            event_id="e",
            endpoint_id="ep",
            status=500,
            retry_after=20,
        )
        + _line(timestamp=2, attempt_id="same", event_id="e", endpoint_id="ep", status=500)
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": attempts},
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,4,1"]


def test_part_3_attempt_ids_are_global_and_any_success_completes_pair(tmp_path):
    attempts = (
        _line(timestamp=1, attempt_id="shared", event_id="e1", endpoint_id="ep", status=500)
        + _line(timestamp=2, attempt_id="shared", event_id="e2", endpoint_id="ep", status=500)
        + _line(timestamp=3, attempt_id="success", event_id="e1", endpoint_id="ep", status=204)
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": attempts},
    )
    assert plan_webhook_archive(manifest) == []


def test_part_4_retries_precede_sorted_dead_letters(tmp_path):
    attempts = "".join(
        [
            _line(timestamp=1, attempt_id="z1", event_id="z", endpoint_id="ep", status=500),
            _line(timestamp=2, attempt_id="z2", event_id="z", endpoint_id="ep", status=500),
            _line(timestamp=1, attempt_id="a1", event_id="a", endpoint_id="ep", status=500),
            _line(timestamp=2, attempt_id="a2", event_id="a", endpoint_id="ep", status=500),
            _line(timestamp=5, attempt_id="r1", event_id="retry", endpoint_id="ep", status=500),
        ]
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": attempts},
        max_attempts=2,
    )
    assert plan_webhook_archive(manifest) == [
        "RETRY,retry,ep,7,1",
        "DEAD,a,ep,,2",
        "DEAD,z,ep,,2",
    ]


def test_part_4_csv_quotes_ids_and_writes_output_file(tmp_path):
    attempts = _line(
        timestamp=1,
        attempt_id="a",
        event_id="event,quoted",
        endpoint_id="ep",
        status=500,
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {"a.jsonl": attempts},
    )
    output = tmp_path / "out" / "plan.csv"
    assert plan_webhook_archive(manifest, output) == [
        'RETRY,"event,quoted",ep,3,1'
    ]
    with output.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.reader(handle))
    assert rows == [
        ["action", "event_id", "endpoint_id", "scheduled_at", "failure_count"],
        ["RETRY", "event,quoted", "ep", "3", "1"],
    ]


def test_part_3_retry_after_on_an_earlier_attempt_is_ignored(tmp_path):
    attempts = (
        _line(
            timestamp=1,
            attempt_id="a1",
            event_id="e",
            endpoint_id="ep",
            status=429,
            retry_after=100,
        )
        + _line(timestamp=2, attempt_id="a2", event_id="e", endpoint_id="ep", status=500)
    )
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,20\n",
        {"a.jsonl": attempts},
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,6,2"]


def test_part_3_partially_unreadable_shard_is_skipped_atomically(tmp_path):
    root = tmp_path / "archive"
    root.mkdir()
    (root / "endpoints.csv").write_text(ENDPOINT_HEADER + "ep,2,10\n", encoding="utf-8")
    valid_prefix = _line(
        timestamp=1, attempt_id="same", event_id="bad", endpoint_id="ep", status=500
    ).encode("utf-8")
    (root / "bad.jsonl").write_bytes(valid_prefix + b"\xff")
    (root / "good.jsonl").write_text(
        _line(timestamp=2, attempt_id="same", event_id="good", endpoint_id="ep", status=500),
        encoding="utf-8",
    )
    (root / "manifest.json").write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": ["bad.jsonl", "good.jsonl"],
                "max_attempts": 5,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(root / "manifest.json") == ["RETRY,good,ep,4,1"]


def test_part_2_non_string_attempt_entries_are_skipped(tmp_path):
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {
            "a.jsonl": _line(
                timestamp=1, attempt_id="a", event_id="e", endpoint_id="ep", status=500
            )
        },
    )
    manifest.write_text(
        json.dumps(
            {
                "endpoint_file": "endpoints.csv",
                "attempt_files": [None, 7, "a.jsonl"],
                "max_attempts": 5,
            }
        ),
        encoding="utf-8",
    )
    assert plan_webhook_archive(manifest) == ["RETRY,e,ep,3,1"]


def test_part_4_valid_empty_plan_still_writes_header(tmp_path):
    manifest = _archive(
        tmp_path / "archive",
        ENDPOINT_HEADER + "ep,2,10\n",
        {
            "a.jsonl": _line(
                timestamp=1, attempt_id="a", event_id="e", endpoint_id="ep", status=204
            )
        },
    )
    output = tmp_path / "nested" / "plan.csv"
    assert plan_webhook_archive(manifest, output) == []
    assert output.read_text(encoding="utf-8") == (
        "action,event_id,endpoint_id,scheduled_at,failure_count\n"
    )
