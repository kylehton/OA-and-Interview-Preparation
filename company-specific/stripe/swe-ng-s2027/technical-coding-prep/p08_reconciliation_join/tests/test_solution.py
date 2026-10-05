from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load():
    spec = spec_from_file_location("p08_solution", Path(__file__).parents[1] / "solution.py")
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


reconcile = _load().reconcile


def test_part_1_exact_matches_preserve_internal_order():
    internal = ["i2,p2,200,EUR", "i1,p1,100,USD"]
    processor = ["p1,100,USD,SUCCEEDED", "p2,200,EUR,SUCCEEDED"]
    assert reconcile(internal, processor) == ["i2,MATCH,p2", "i1,MATCH,p1"]


def test_part_2_missing_and_mismatched():
    internal = ["i1,p1,100,USD", "i2,p2,50,USD", "i3,p3,1,USD"]
    processor = ["p1,99,USD,SUCCEEDED", "p2,50,USD,FAILED"]
    assert reconcile(internal, processor) == [
        "i1,MISMATCH,p1", "i2,MISMATCH,p2", "i3,MISSING,-"
    ]


def test_part_2_invalid_rows_are_ignored():
    internal = ["bad", "i,p,10,usd", "good,p,10,USD"]
    processor = ["p,10,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["good,MATCH,p"]


def test_part_3_appends_orphans_in_processor_order():
    internal = ["i,p1,10,USD"]
    processor = [
        "p2,20,USD,SUCCEEDED",
        "p1,10,USD,SUCCEEDED",
        "p3,30,USD,FAILED",
    ]
    assert reconcile(internal, processor, True) == [
        "i,MATCH,p1", "-,ORPHAN,p2", "-,ORPHAN,p3"
    ]


def test_part_4_exact_match_is_preferred_over_earlier_mismatch():
    internal = ["i1,p1,100,USD", "i2,p1,80,USD", "i3,p1,80,USD"]
    processor = [
        "p1,80,USD,SUCCEEDED",
        "p1,100,USD,SUCCEEDED",
    ]
    assert reconcile(internal, processor) == [
        "i1,MATCH,p1", "i2,MATCH,p1", "i3,MISSING,-"
    ]


def test_part_4_csv_output_escapes_quoted_ids():
    internal = ['"order,one",p1,100,USD']
    processor = ["p1,100,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ['"order,one",MATCH,p1']


def test_part_2_invalid_processor_rows_are_neither_matched_nor_orphans():
    internal = ["pay_1,p_1,100,USD"]
    processor = [
        "p_1,-100,USD,SUCCEEDED",
        "p_2,100,usd,SUCCEEDED",
        "p_3,100,USD,UNKNOWN",
        ",100,USD,SUCCEEDED",
    ]
    assert reconcile(internal, processor, True) == ["pay_1,MISSING,-"]


def test_part_2_nonpositive_internal_amounts_are_ignored():
    internal = ["zero,p0,0,USD", "negative,pn,-1,USD", "good,p1,1,USD"]
    processor = ["p0,1,USD,SUCCEEDED", "pn,1,USD,SUCCEEDED", "p1,1,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["good,MATCH,p1"]


def test_part_3_a_processor_row_can_only_be_consumed_once():
    internal = ["a,p,90,USD", "b,p,80,USD"]
    processor = ["p,100,USD,SUCCEEDED"]
    assert reconcile(internal, processor) == ["a,MISMATCH,p", "b,MISSING,-"]


def test_part_3_fields_are_trimmed_before_matching():
    internal = [" pay_1 , p_1 , 100 , USD "]
    processor = [" p_1 , 100 , USD , SUCCEEDED "]
    assert reconcile(internal, processor) == ["pay_1,MATCH,p_1"]


def test_part_4_orphan_output_escapes_processor_id():
    assert reconcile([], ['"p,one",100,USD,SUCCEEDED'], True) == [
        '-,ORPHAN,"p,one"'
    ]
