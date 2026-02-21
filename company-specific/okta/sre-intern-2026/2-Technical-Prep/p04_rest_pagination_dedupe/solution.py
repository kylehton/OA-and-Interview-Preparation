from __future__ import annotations

from typing import Callable, Dict, List, Optional, Any


def fetch_all_items(fetch_page: Callable[[Optional[str]], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Traverse paginated API starting at token None.
    Deduplicate by item["id"], keep first occurrence, preserve order.
    Detect pagination token cycles -> raise ValueError("pagination cycle").
    """
    raise NotImplementedError
    


def fetch_all_ids(fetch_page: Callable[[Optional[str]], Dict[str, Any]]) -> List[str]:
    """
    Same traversal as fetch_all_items but returns list of deduped ids.
    """
    raise NotImplementedError