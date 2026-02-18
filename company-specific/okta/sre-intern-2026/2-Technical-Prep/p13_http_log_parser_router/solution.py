from __future__ import annotations

from typing import Dict, List, Tuple


def route_stats(filepath: str) -> Dict[str, Dict[str, int]]:
    raise NotImplementedError


def top_routes_by_5xx(filepath: str, k: int) -> List[Tuple[str, int]]:
    raise NotImplementedError
