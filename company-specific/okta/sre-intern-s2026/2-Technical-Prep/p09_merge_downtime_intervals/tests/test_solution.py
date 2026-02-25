import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import merge_downtime, total_downtime_seconds


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_merge_overlap_and_adjacent():
    content = "\n".join(
        [
            "a 10 12",
            "a 13 13",  # adjacent to [10,12] => merge
            "a 20 25",
            "a 24 30",  # overlap => merge
        ]
    )
    path = _tmpfile(content)
    merged = merge_downtime(path)
    assert merged["a"] == [(10, 13), (20, 30)]
    totals = total_downtime_seconds(merged)
    assert totals["a"] == (13 - 10 + 1) + (30 - 20 + 1)

def test_out_of_order_intervals():
    path = _tmpfile("\n".join([
        "a 20 25",
        "a 1 5",
        "a 6 10",
    ]))

    merged = merge_downtime(path)

    # Correct result should merge 1-5 and 6-10 (adjacent),
    # and keep 20-25 separate.
    assert merged["a"] == [(1, 10), (20, 25)]


def test_multiple_services_and_invalid_lines():
    content = "\n".join(
        [
            "a 1 1",
            "b 5 4",      # invalid start>end
            "b x y",      # invalid
            "b 10 10",
            "bad",
            "a 2 2",
        ]
    )
    path = _tmpfile(content)
    merged = merge_downtime(path)
    assert merged == {"a": [(1, 2)], "b": [(10, 10)]}
    assert total_downtime_seconds(merged) == {"a": 2, "b": 1}

def test_cascading_merge():
    path = _tmpfile("\n".join([
        "a 1 3",
        "a 5 7",
        "a 2 6",   # overlaps both previous intervals
    ]))

    merged = merge_downtime(path)
    # Correct result should be single merged interval:
    assert merged["a"] == [(1, 7)]

def test_cascade_break():
    path = _tmpfile("\n".join([
        "a 2 6",
        "a 1 3",
        "a 5 7",
    ]))

    merged = merge_downtime(path)

    assert merged["a"] == [(1, 7)]