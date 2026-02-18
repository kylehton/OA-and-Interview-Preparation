from __future__ import annotations

from typing import List


def impacted_services(filepath: str, failed: str) -> List[str]:
    raise NotImplementedError


def has_cycle(filepath: str) -> bool:
    raise NotImplementedError
