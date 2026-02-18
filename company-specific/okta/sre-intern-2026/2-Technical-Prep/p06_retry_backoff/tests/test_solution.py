import pytest
from p06_retry_backoff.solution import retry, retry_with_jitter


def test_retry_succeeds_after_failures():
    calls = {"n": 0}
    sleeps = []

    def op():
        calls["n"] += 1
        if calls["n"] < 3:
            raise RuntimeError("boom")
        return 123

    def sleep_fn(d):
        sleeps.append(d)

    assert retry(op, retries=5, base_delay=0.5, sleep_fn=sleep_fn) == 123
    assert calls["n"] == 3
    assert sleeps == [0.5, 1.0]  # attempt_index 0 then 1


def test_retry_reraises_last_exception():
    calls = {"n": 0}
    sleeps = []

    def op():
        calls["n"] += 1
        raise ValueError("nope")

    def sleep_fn(d):
        sleeps.append(d)

    with pytest.raises(ValueError) as e:
        retry(op, retries=2, base_delay=1.0, sleep_fn=sleep_fn)
    assert "nope" in str(e.value)
    assert calls["n"] == 3  # 1 + 2 retries
    assert sleeps == [1.0, 2.0]


def test_retry_with_jitter():
    calls = {"n": 0}
    sleeps = []
    jitters = [0.1, 0.2, 0.3]

    def op():
        calls["n"] += 1
        if calls["n"] < 4:
            raise RuntimeError("fail")
        return "ok"

    def jitter_fn():
        return jitters.pop(0)

    def sleep_fn(d):
        sleeps.append(d)

    assert retry_with_jitter(op, retries=5, base_delay=1.0, jitter_fn=jitter_fn, sleep_fn=sleep_fn) == "ok"
    assert sleeps == [1.0 + 0.1, 2.0 + 0.2, 4.0 + 0.3]
