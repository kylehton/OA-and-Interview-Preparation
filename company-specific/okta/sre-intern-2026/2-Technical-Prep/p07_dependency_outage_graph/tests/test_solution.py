import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import impacted_services, has_cycle


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_impacted_basic():
    path = _tmpfile("\n".join(["api -> auth", "auth -> db", "billing -> db"]))
    assert impacted_services(path, "db") == ["api", "auth", "billing"]
    assert impacted_services(path, "auth") == ["api"]


def test_ignores_invalid_lines():
    path = _tmpfile("\n".join(["api->auth", "x -> y", "bad", "x -> z"]))
    assert impacted_services(path, "y") == ["x"]


def test_cycles_do_not_infinite_loop():
    path = _tmpfile("\n".join(["a -> b", "b -> c", "c -> a", "d -> a"]))
    assert impacted_services(path, "a") == ["b", "c", "d"]
    assert has_cycle(path) is True


def test_has_cycle_false():
    path = _tmpfile("\n".join(["a -> b", "b -> c", "c -> d"]))
    assert has_cycle(path) is False

def test_has_cycle_disconnected_component():
    path = _tmpfile(
        "\n".join(
            [
                # Component 1 (has cycle)
                "a -> b",
                "b -> a",
                # Component 2 (acyclic, appears last)
                "x -> y",
                "y -> z",
            ]
        )
    )
    assert has_cycle(path) is True

def test_self_cycle():
    path = _tmpfile("a -> a")
    assert has_cycle(path) is True

def test_disconnected_no_cycle():
    path = _tmpfile("\n".join([
        "a -> b",
        "c -> d",
    ]))
    assert has_cycle(path) is False
