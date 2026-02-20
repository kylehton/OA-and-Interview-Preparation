import tempfile
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from solution import route_stats, top_routes_by_5xx


def _tmpfile(content: str) -> str:
    f = tempfile.NamedTemporaryFile(mode="w+", delete=False)
    f.write(content)
    f.flush()
    f.close()
    return f.name


def test_normalization_and_buckets():
    content = "\n".join(
        [
            "GET /api/v1/users/123/profile 200",
            "GET /api/v1/users/456/profile 500",
            "POST /api/v1/login 401",
            "GET /api/v1/login 499",
            "GET /api/v1/login 200",
            "BADLINE",
            "GET /api/v1/users/x/profile 500",  # 'x' not numeric => not replaced
            "GET /api/v1/users/999/profile 302",  # ignored bucket
        ]
    )
    path = _tmpfile(content)
    stats = route_stats(path)

    assert stats["/api/v1/users/{id}/profile"] == {"2xx": 1, "4xx": 0, "5xx": 1}
    assert stats["/api/v1/login"] == {"2xx": 1, "4xx": 2, "5xx": 0}
    assert stats["/api/v1/users/x/profile"] == {"2xx": 0, "4xx": 0, "5xx": 1}


def test_top_routes_by_5xx():
    content = "\n".join(
        [
            "GET /a/1 500",
            "GET /a/2 500",
            "GET /b 500",
            "GET /b 500",
            "GET /b 500",
        ]
    )
    path = _tmpfile(content)
    assert top_routes_by_5xx(path, 2) == [("/b", 3), ("/a/{id}", 2)]


def test_k_zero():
    path = _tmpfile("GET /a 500\n")
    assert top_routes_by_5xx(path, 0) == []
