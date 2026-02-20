import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import compute_error_rate, services_by_error_rate


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_basic_rates():
    path = _tmpfile(
        "\n".join(
            [
                "2026-02-17T10:00:00 auth 200",
                "2026-02-17T10:00:01 auth 500",
                "2026-02-17T10:00:02 auth 200",
                "2026-02-17T10:00:03 billing 503",
                "2026-02-17T10:00:04 billing 200",
                "",
            ]
        )
    )
    out = compute_error_rate(path)
    assert out == {"auth": 0.3333, "billing": 0.5}


def test_ignores_invalid_lines():
    path = _tmpfile(
        "\n".join(
            [
                "2026-02-17T10:00:00 auth 200",
                "badline",
                "2026-02-17T10:00:01 auth not_an_int",
                "2026-02-17T10:00:02  500",  # service missing after split -> invalid tokens count
                "2026-02-17T10:00:03 auth 500 extra",  # too many tokens
                "2026-02-17T10:00:04 auth 500",
            ]
        )
    )
    out = compute_error_rate(path)
    # only two valid auth lines: 200 and 500 => 0.5
    assert out == {"auth": 0.5}


def test_no_valid_lines_returns_empty():
    path = _tmpfile(" \n\nbad\nx y z w\n")
    assert compute_error_rate(path) == {}


def test_services_by_error_rate_sorting():
    path = _tmpfile(
        "\n".join(
            [
                "t a 500",  # a: 1/2 = 0.5 (total 2)
                "t a 200",
                "t b 500",  # b: 1/1 = 1.0 (total 1)
                "t c 500",  # c: 1/2 = 0.5 (total 2) => tie with a, totals equal, name asc
                "t c 200",
                "bad",
                "t d 200",  # d: 0.0
            ]
        )
    )
    res = services_by_error_rate(path)
    assert res == [("b", 1.0), ("a", 0.5), ("c", 0.5), ("d", 0.0)]
