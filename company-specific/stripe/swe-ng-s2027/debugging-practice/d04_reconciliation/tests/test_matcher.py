import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from reconciliation import reconcile


def test_basic_match():
    assert reconcile(["i1,p1,100,USD"], ["p1,100,USD,SUCCEEDED"]) == [
        "i1,MATCH,p1"
    ]


def test_mismatch_and_missing():
    internal = ["i1,p1,100,USD", "i2,p2,50,EUR"]
    processor = ["p1,99,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["i1,MISMATCH,p1", "i2,MISSING,-"]


def test_prefers_exact_match_over_earlier_mismatch():
    internal = ["i1,p1,100,USD"]
    processor = ["p1,80,USD,SUCCEEDED", "p1,100,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["i1,MATCH,p1"]


def test_processor_rows_are_consumed_at_most_once():
    internal = ["i1,p1,100,USD", "i2,p1,100,USD"]
    processor = ["p1,100,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["i1,MATCH,p1", "i2,MISSING,-"]


def test_consumed_rows_are_not_reported_as_orphans():
    internal = ["i1,p1,100,USD"]
    processor = ["p1,100,USD,SUCCEEDED", "p2,50,USD,FAILED"]
    assert reconcile(internal, processor, include_orphans=True) == [
        "i1,MATCH,p1", "-,ORPHAN,p2"
    ]


def test_quoted_csv_fields_are_parsed_and_formatted():
    internal = ['"order,one",p1,100,USD']
    processor = ["p1,100,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ['"order,one",MATCH,p1']


def test_non_positive_amount_rows_are_ignored():
    internal = ["i1,p1,-100,USD"]
    processor = ["p1,-100,USD,SUCCEEDED"]
    assert reconcile(internal, processor, include_orphans=True) == []

