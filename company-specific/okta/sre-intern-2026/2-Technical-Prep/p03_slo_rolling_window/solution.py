from __future__ import annotations

from typing import Optional


def first_slo_breach(
    filepath: str,
    service: str,
    window_seconds: int,
    max_error_rate: float,
) -> Optional[str]:
    """
    Return timestamp of first request that causes rolling window error rate
    for `service` to exceed max_error_rate. See README for details.
    """
    raise NotImplementedError
