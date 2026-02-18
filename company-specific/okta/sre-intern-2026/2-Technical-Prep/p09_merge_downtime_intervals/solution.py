from __future__ import annotations

from typing import Dict, List, Tuple


def merge_downtime(filepath: str) -> Dict[str, List[Tuple[int, int]]]:
    raise NotImplementedError


def total_downtime_seconds(merged: Dict[str, List[Tuple[int, int]]]) -> Dict[str, int]:
    raise NotImplementedError
