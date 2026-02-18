from __future__ import annotations

from typing import Dict, List, Tuple


def p95_latency(filepath: str) -> Dict[str, int]:
    raise NotImplementedError


def top_p95_services(filepath: str, k: int) -> List[Tuple[str, int]]:
    raise NotImplementedError
