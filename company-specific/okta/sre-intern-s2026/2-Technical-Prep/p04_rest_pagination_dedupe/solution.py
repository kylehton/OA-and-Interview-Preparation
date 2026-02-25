from __future__ import annotations

from typing import Callable, Dict, List, Optional, Any


def fetch_all_items(fetch_page: Callable[[Optional[str]], Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Traverse paginated API starting at token None.
    Deduplicate by item["id"], keep first occurrence, preserve order.
    Detect pagination token cycles -> raise ValueError("pagination cycle").
    """
    item_list = []
    id_set = set()
    page_set = set()
    curr_page = fetch_page(None)
    while curr_page is not None:
        next_page = curr_page['next']
        if next_page in page_set:
            raise ValueError('pagination cycle')
        page_set.add(next_page)
        items = curr_page['items']
        for item in items:
            curr_id = item.get('id')
            if curr_id and curr_id not in id_set:
                item_list.append(item)
                id_set.add(curr_id)
        if next_page == None:
            break
        curr_page = fetch_page(next_page)
    return list(item_list)
    


def fetch_all_ids(fetch_page: Callable[[Optional[str]], Dict[str, Any]]) -> List[str]:
    """
    Same traversal as fetch_all_items but returns list of deduped ids.
    """
    id_list = []
    id_set = set()
    page_set = set()
    curr_page = fetch_page(None)
    while curr_page is not None:
        next_page = curr_page['next']
        if next_page in page_set:
            raise ValueError('pagination cycle')
        page_set.add(next_page)
        items = curr_page['items']
        for item in items:
            curr_id = item.get('id')
            if curr_id and curr_id not in id_set:
                id_list.append(curr_id)
                id_set.add(curr_id)
        if next_page == None:
            break
        curr_page = fetch_page(next_page)
    return list(id_list)
