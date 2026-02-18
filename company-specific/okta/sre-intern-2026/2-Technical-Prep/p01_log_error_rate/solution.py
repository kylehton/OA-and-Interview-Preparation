from __future__ import annotations

from typing import Dict, List, Tuple


def compute_error_rate(filepath: str) -> Dict[str, float]:
    """
    Compute error rate per service from a log file.

    See README for line format and invalid-line rules.
    Must stream the file line-by-line.
    """
    raise NotImplementedError


def services_by_error_rate(filepath: str) -> List[Tuple[str, float]]:
    """
    Follow-up: returns (service, error_rate) sorted by:
    - error_rate desc
    - total_requests desc
    - service asc
    """
    raise NotImplementedError
