import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import count_unique_users, top_active_users


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_count_unique_users_basic():
    path = _tmpfile("\n".join(["t u1 a", "t u2 b", "t u1 c"]))
    assert count_unique_users(path) == 2


def test_ignores_invalid_lines():
    path = _tmpfile("\n".join(["bad", "t  a", "t u1 a", "t u2 b extra", "t u2 c"]))
    assert count_unique_users(path) == 2


def test_top_active_users():
    path = _tmpfile("\n".join(["t u2 a", "t u1 a", "t u2 b", "t u3 a", "t u2 c", "t u1 b"]))
    assert top_active_users(path, 2) == [("u2", 3), ("u1", 2)]


def test_top_active_users_tie_break():
    path = _tmpfile("\n".join(["t u2 a", "t u1 a"]))
    assert top_active_users(path, 10) == [("u1", 1), ("u2", 1)]


def test_k_zero():
    path = _tmpfile("t u1 a\n")
    assert top_active_users(path, 0) == []
