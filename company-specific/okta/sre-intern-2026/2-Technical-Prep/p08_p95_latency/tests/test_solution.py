import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import p95_latency, top_p95_services


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_p95_nearest_rank():
    # n=20 => ceil(0.95*20)=19 => index 18 (0-based) => value 19
    samples = "\n".join([f"auth {i}" for i in range(1, 21)])
    path = _tmpfile(samples)
    assert p95_latency(path) == {"auth": 19}


def test_multiple_services_and_invalid():
    content = "\n".join(
        [
            "a 10",
            "a -1",
            "a x",
            "b 5",
            "b 100",
            "badline",
            "b 50",
        ]
    )
    path = _tmpfile(content)
    # a has [10] => p95 = 10
    # b has [5,50,100], n=3 => ceil(2.85)=3 => idx 2 => 100
    assert p95_latency(path) == {"a": 10, "b": 100}


def test_top_k_sorting():
    content = "\n".join(
        [
            "a 1",
            "a 2",
            "a 3",
            "b 10",
            "b 20",
            "c 20",
        ]
    )
    path = _tmpfile(content)
    res = top_p95_services(path, 2)
    # p95 nearest-rank:
    # a n=3 => ceil(2.85)=3 => 3
    # b n=2 => ceil(1.9)=2 => 20
    # c n=1 => 20
    assert res == [("b", 20), ("c", 20)]


def test_k_zero():
    path = _tmpfile("a 1\n")
    assert top_p95_services(path, 0) == []
