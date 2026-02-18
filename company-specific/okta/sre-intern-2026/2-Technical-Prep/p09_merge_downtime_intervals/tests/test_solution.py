import tempfile
from p09_merge_downtime_intervals.solution import merge_downtime, total_downtime_seconds


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
