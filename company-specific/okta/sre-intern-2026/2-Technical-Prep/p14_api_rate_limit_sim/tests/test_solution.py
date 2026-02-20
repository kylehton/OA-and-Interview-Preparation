import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import schedule_retries, dedupe_latest_retry


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_schedule_retries_basic():
    req = _tmpfile("\n".join(["10 r1 /x", "12 r2 /y", "13 r1 /x"]))
    res = _tmpfile("\n".join(["r1 429", "r2 200"]))
    out = schedule_retries(req, res, 5)
    # r1 appears twice => two retries
    assert out == [(15, "r1"), (18, "r1")]


def test_ignores_missing_results_and_invalid():
    req = _tmpfile("\n".join(["10 r1 /x", "bad", "11 r3 /z"]))
    res = _tmpfile("\n".join(["r1 429", "oops", "r2 429"]))
    assert schedule_retries(req, res, 1) == [(11, "r1")]


def test_sorting_request_id_on_tie():
    req = _tmpfile("\n".join(["10 a /x", "10 b /y"]))
    res = _tmpfile("\n".join(["a 429", "b 429"]))
    assert schedule_retries(req, res, 0) == [(10, "a"), (10, "b")]


def test_dedupe_latest_retry():
    req = _tmpfile("\n".join(["10 r1 /x", "20 r1 /x", "30 r2 /y"]))
    res = _tmpfile("\n".join(["r1 429", "r2 429"]))
    out = dedupe_latest_retry(req, res, 5)
    # r1 latest is 20->25, r2 is 30->35
    assert out == [(25, "r1"), (35, "r2")]
