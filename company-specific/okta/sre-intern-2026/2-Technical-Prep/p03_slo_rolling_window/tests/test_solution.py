import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import first_slo_breach


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_no_breach_when_equal_threshold():
    # 1 error / 100 total => 0.01 equals threshold; breach requires >
    lines = ["2026-02-17T10:00:00 api 200"] * 99 + ["2026-02-17T10:01:00 api 500"]
    path = _tmpfile("\n".join(lines))
    assert first_slo_breach(path, "api", 3600, 0.01) is None


def test_breach_occurs():
    # window 300s, at t=10:04:00 we have 2 errors out of 3 => 0.666... > 0.5
    content = "\n".join(
        [
            "2026-02-17T10:00:00 api 200",
            "2026-02-17T10:04:00 api 500",
            "2026-02-17T10:04:01 api 500",
        ]
    )
    path = _tmpfile(content)
    assert first_slo_breach(path, "api", 300, 0.5) == "2026-02-17T10:04:01"


def test_window_boundary_inclusive():
    # window 60 seconds inclusive: at t=10:01:00 includes t=10:00:00
    content = "\n".join(
        [
            "2026-02-17T10:00:00 api 500",
            "2026-02-17T10:01:00 api 200",
        ]
    )
    path = _tmpfile(content)
    # window [10:00:00, 10:01:00] => 1/2 = 0.5, threshold 0.4 => breach at second line
    assert first_slo_breach(path, "api", 60, 0.4) == "2026-02-17T10:01:00"


def test_ignores_other_services_and_invalid_lines():
    content = "\n".join(
        [
            "2026-02-17T10:00:00 other 500",
            "bad line",
            "2026-02-17T10:00:10 api 500",
            "2026-02-17T10:00:20 api oops",
            "2026-02-17T10:00:30 api 500",
            "2026-02-17T10:00:40 api 200",
        ]
    )
    path = _tmpfile(content)
    # valid api lines: 500, 500, 200 => errors 2/3 = 0.666 > 0.6 at 10:00:40
    assert first_slo_breach(path, "api", 999, 0.6) == "2026-02-17T10:00:30"
