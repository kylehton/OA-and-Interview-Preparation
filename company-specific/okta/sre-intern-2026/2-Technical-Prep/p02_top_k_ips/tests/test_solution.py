import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import top_k_ips


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_basic_topk():
    path = _tmpfile(
        "\n".join(
            [
                "t 1.1.1.1 /a",
                "t 2.2.2.2 /b",
                "t 1.1.1.1 /c",
                "t 3.3.3.3 /d",
                "t 2.2.2.2 /e",
                "t 2.2.2.2 /f",
            ]
        )
    )
    assert top_k_ips(path, 2) == ["2.2.2.2", "1.1.1.1"]


def test_tie_break_lexicographic():
    path = _tmpfile("\n".join(["t 10.0.0.2 /x", "t 10.0.0.10 /y"]))
    # both freq 1 => lex asc
    assert top_k_ips(path, 10) == ["10.0.0.10", "10.0.0.2"]


def test_ignores_invalid_lines_and_empty_ip():
    path = _tmpfile("\n".join(["bad", "t  /x", "t 1.1.1.1 /a extra", "t 1.1.1.1 /ok"]))
    assert top_k_ips(path, 5) == ["1.1.1.1"]


def test_k_zero_or_negative():
    path = _tmpfile("\n".join(["t 1.1.1.1 /a", "t 2.2.2.2 /b"]))
    assert top_k_ips(path, 0) == []
    assert top_k_ips(path, -3) == []
