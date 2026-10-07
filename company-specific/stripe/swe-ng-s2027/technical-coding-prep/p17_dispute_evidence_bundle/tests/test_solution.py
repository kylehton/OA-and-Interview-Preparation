import json
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pytest


def _load():
    spec = spec_from_file_location("p17_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


build_dispute_report = _load().build_dispute_report
FIXTURES = Path(__file__).parents[1] / "fixtures" / "basic"
CHARGE_HEADER = "charge_id,merchant_id,amount,currency,captured_at\n"
DISPUTE_HEADER = "dispute_id,charge_id,amount,opened_on,evidence_path\n"


def _bundle(
    root: Path,
    charges: str,
    disputes: str,
    *,
    policy: dict | None = None,
    evidence: dict[str, str | bytes] | None = None,
) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "charges.csv").write_text(charges, encoding="utf-8")
    (root / "disputes.csv").write_text(disputes, encoding="utf-8")
    (root / "policy.json").write_text(
        json.dumps(policy if policy is not None else {"response_days": 7, "high_value": {}}),
        encoding="utf-8",
    )
    for name, content in (evidence or {}).items():
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(content, encoding="utf-8")
    return root


def test_part_3_reads_complete_fixture_bundle():
    assert build_dispute_report(FIXTURES, "2026-01-10") == [
        "dp_1,m_1,USD,4000,2026-01-12,REVIEW",
        'dp_2,"merchant,quoted",EUR,5000,2026-01-13,MISSING_EVIDENCE',
    ]


def test_part_1_invalid_charge_row_does_not_reserve_charge_id(tmp_path):
    charges = (
        CHARGE_HEADER
        + "ch,m,0,USD,2026-01-01T00:00:00Z\n"
        + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    )
    disputes = DISPUTE_HEADER + "d,ch,10,2026-01-02,evidence/d.txt\n"
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={"evidence/d.txt": "charge_id=ch\nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "d,m,USD,10,2026-01-09,READY"
    ]


def test_part_1_bad_required_header_returns_empty(tmp_path):
    bundle = _bundle(
        tmp_path / "bundle",
        "wrong,header\na,b\n",
        DISPUTE_HEADER,
    )
    assert build_dispute_report(bundle, "2026-01-01") == []


def test_part_1_invalid_as_of_is_rejected_with_otherwise_valid_bundle(tmp_path):
    bundle = _bundle(
        tmp_path / "bundle",
        CHARGE_HEADER + "ch,m,10,USD,2026-01-01T00:00:00Z\n",
        DISPUTE_HEADER,
    )
    assert build_dispute_report(bundle, "2026-1-2") == []


def test_part_1_capture_timestamp_must_be_exact_utc_and_failed_id_is_reusable(tmp_path):
    charges = (
        CHARGE_HEADER
        + "ch,m,10,USD,2026-01-01T00:00:00+00:00\n"
        + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    )
    disputes = DISPUTE_HEADER + "d,ch,10,2026-01-01,\n"
    bundle = _bundle(tmp_path / "bundle", charges, disputes)
    assert build_dispute_report(bundle, "2026-01-01") == [
        "d,m,USD,10,2026-01-08,MISSING_EVIDENCE"
    ]


def test_part_2_evidence_binding_and_body_are_required(tmp_path):
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = (
        DISPUTE_HEADER
        + "wrong,ch,10,2026-01-02,evidence/wrong.txt\n"
        + "empty,ch,10,2026-01-03,evidence/empty.txt\n"
    )
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={
            "evidence/wrong.txt": "charge_id=other\nproof\n",
            "evidence/empty.txt": "\ncharge_id=ch\n\n",
        },
    )
    assert build_dispute_report(bundle, "2026-01-03") == [
        "wrong,m,USD,10,2026-01-09,MISSING_EVIDENCE",
        "empty,m,USD,10,2026-01-10,MISSING_EVIDENCE",
    ]


def test_part_2_unsafe_and_non_utf8_evidence_are_missing(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("charge_id=ch\nproof\n", encoding="utf-8")
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = (
        DISPUTE_HEADER
        + "escape,ch,10,2026-01-02,../outside.txt\n"
        + "binary,ch,10,2026-01-02,evidence/binary.txt\n"
    )
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={"evidence/binary.txt": b"\xff\xfe"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "binary,m,USD,10,2026-01-09,MISSING_EVIDENCE",
        "escape,m,USD,10,2026-01-09,MISSING_EVIDENCE",
    ]


def test_part_2_evidence_symlink_escape_is_missing(tmp_path):
    outside = tmp_path / "outside.txt"
    outside.write_text("charge_id=ch\nproof\n", encoding="utf-8")
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = DISPUTE_HEADER + "d,ch,10,2026-01-02,evidence/link.txt\n"
    bundle = _bundle(tmp_path / "bundle", charges, disputes)
    (bundle / "evidence").mkdir()
    try:
        (bundle / "evidence" / "link.txt").symlink_to(outside)
    except OSError:
        pytest.skip("symlinks are not available on this platform")

    assert build_dispute_report(bundle, "2026-01-02") == [
        "d,m,USD,10,2026-01-09,MISSING_EVIDENCE"
    ]


def test_part_3_expired_status_has_highest_precedence(tmp_path):
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = DISPUTE_HEADER + "d,ch,100,2026-01-02,missing.txt\n"
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        policy={"response_days": 2, "high_value": {"USD": 100}},
    )
    assert build_dispute_report(bundle, "2026-01-05") == [
        "d,m,USD,100,2026-01-04,EXPIRED"
    ]


def test_part_3_deadline_is_inclusive_and_high_value_threshold_is_inclusive(tmp_path):
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = DISPUTE_HEADER + "d,ch,50,2026-01-02,evidence/d.txt\n"
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        policy={"response_days": 2, "high_value": {"USD": 50}},
        evidence={"evidence/d.txt": "charge_id=ch\nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-04") == [
        "d,m,USD,50,2026-01-04,REVIEW"
    ]


def test_part_1_malformed_policy_returns_empty(tmp_path):
    bundle = tmp_path / "bundle"
    bundle.mkdir()
    (bundle / "charges.csv").write_text(CHARGE_HEADER, encoding="utf-8")
    (bundle / "disputes.csv").write_text(DISPUTE_HEADER, encoding="utf-8")
    (bundle / "policy.json").write_text(
        '{"response_days": true, "high_value": {}}', encoding="utf-8"
    )
    assert build_dispute_report(bundle, "2026-01-01") == []


def test_part_4_failed_dispute_id_is_reusable_and_limit_is_per_charge(tmp_path):
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = (
        DISPUTE_HEADER
        + "first,ch,70,2026-01-02,evidence/first.txt\n"
        + "retry,missing,1,2026-01-02,evidence/retry.txt\n"
        + "retry,ch,31,2026-01-02,evidence/retry.txt\n"
        + "retry,ch,30,2026-01-02,evidence/retry.txt\n"
    )
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={
            "evidence/first.txt": "charge_id=ch\nfirst proof\n",
            "evidence/retry.txt": "charge_id=ch\nretry proof\n",
        },
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "first,m,USD,70,2026-01-09,READY",
        "retry,m,USD,30,2026-01-09,READY",
    ]


def test_part_4_sorts_by_deadline_then_dispute_id(tmp_path):
    charges = CHARGE_HEADER + "ch,m,100,USD,2026-01-01T00:00:00Z\n"
    disputes = (
        DISPUTE_HEADER
        + "z,ch,10,2026-01-02,evidence/z.txt\n"
        + "b,ch,10,2026-01-03,evidence/b.txt\n"
        + "a,ch,10,2026-01-03,evidence/a.txt\n"
    )
    evidence = {
        f"evidence/{name}.txt": "charge_id=ch\nproof\n" for name in ("z", "b", "a")
    }
    bundle = _bundle(tmp_path / "bundle", charges, disputes, evidence=evidence)
    rows = build_dispute_report(bundle, "2026-01-03")
    assert [row.split(",", 1)[0] for row in rows] == ["z", "a", "b"]


def test_part_1_policy_rejects_boolean_threshold_and_bad_currency(tmp_path):
    charges = CHARGE_HEADER + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    for index, high_value in enumerate(({"USD": True}, {"Usd": 10})):
        bundle = _bundle(
            tmp_path / str(index),
            charges,
            DISPUTE_HEADER,
            policy={"response_days": 0, "high_value": high_value},
        )
        assert build_dispute_report(bundle, "2026-01-01") == []


def test_part_3_zero_day_deadline_is_inclusive(tmp_path):
    charges = CHARGE_HEADER + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    disputes = DISPUTE_HEADER + "d,ch,10,2026-01-02,evidence/d.txt\n"
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        policy={"response_days": 0, "high_value": {}},
        evidence={"evidence/d.txt": "charge_id=ch\nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "d,m,USD,10,2026-01-02,READY"
    ]


def test_part_4_missing_evidence_still_reserves_id_and_allocation(tmp_path):
    charges = CHARGE_HEADER + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    disputes = (
        DISPUTE_HEADER
        + "same,ch,10,2026-01-02,missing.txt\n"
        + "same,ch,1,2026-01-02,evidence/good.txt\n"
        + "other,ch,1,2026-01-02,evidence/good.txt\n"
    )
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={"evidence/good.txt": "charge_id=ch\nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "same,m,USD,10,2026-01-09,MISSING_EVIDENCE"
    ]


def test_part_2_evidence_binding_line_is_not_whitespace_normalized(tmp_path):
    charges = CHARGE_HEADER + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    disputes = DISPUTE_HEADER + "d,ch,10,2026-01-02,evidence/d.txt\n"
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={"evidence/d.txt": " charge_id=ch \nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "d,m,USD,10,2026-01-09,MISSING_EVIDENCE"
    ]


def test_part_1_wrong_arity_rows_do_not_reserve_ids(tmp_path):
    charges = (
        CHARGE_HEADER
        + "ch,m,10,USD,2026-01-01T00:00:00Z,extra\n"
        + "ch,m,10,USD,2026-01-01T00:00:00Z\n"
    )
    disputes = (
        DISPUTE_HEADER
        + "d,ch,10,2026-01-02,evidence/d.txt,extra\n"
        + "d,ch,10,2026-01-02,evidence/d.txt\n"
    )
    bundle = _bundle(
        tmp_path / "bundle",
        charges,
        disputes,
        evidence={"evidence/d.txt": "charge_id=ch\nproof\n"},
    )
    assert build_dispute_report(bundle, "2026-01-02") == [
        "d,m,USD,10,2026-01-09,READY"
    ]
