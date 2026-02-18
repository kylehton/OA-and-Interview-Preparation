from p04_rest_pagination_dedupe.solution import fetch_all_items, fetch_all_ids


def test_basic_pagination_and_dedupe():
    pages = {
        None: {"items": [{"id": "a"}, {"id": "b"}], "next": "t1"},
        "t1": {"items": [{"id": "b"}, {"id": "c"}], "next": None},
    }

    def fetch(token):
        return pages[token]

    items = fetch_all_items(fetch)
    assert [x["id"] for x in items] == ["a", "b", "c"]
    assert fetch_all_ids(fetch) == ["a", "b", "c"]


def test_empty_pages_ok():
    pages = {None: {"items": [], "next": "t1"}, "t1": {"items": [], "next": None}}

    def fetch(token):
        return pages[token]

    assert fetch_all_items(fetch) == []
    assert fetch_all_ids(fetch) == []


def test_missing_id_items_ignored():
    pages = {None: {"items": [{"id": "a"}, {"nope": 1}, {"id": "b"}], "next": None}}

    def fetch(token):
        return pages[token]

    assert [x["id"] for x in fetch_all_items(fetch)] == ["a", "b"]
    assert fetch_all_ids(fetch) == ["a", "b"]


def test_cycle_detection_raises():
    pages = {
        None: {"items": [{"id": "a"}], "next": "t1"},
        "t1": {"items": [{"id": "b"}], "next": "t1"},  # cycle on same token
    }

    def fetch(token):
        return pages[token]

    try:
        fetch_all_items(fetch)
        assert False, "expected ValueError"
    except ValueError as e:
        assert str(e) == "pagination cycle"
