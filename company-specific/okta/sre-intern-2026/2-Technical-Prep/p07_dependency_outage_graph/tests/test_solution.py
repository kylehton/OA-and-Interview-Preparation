import tempfile
from p07_dependency_outage_graph.solution import impacted_services, has_cycle


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
