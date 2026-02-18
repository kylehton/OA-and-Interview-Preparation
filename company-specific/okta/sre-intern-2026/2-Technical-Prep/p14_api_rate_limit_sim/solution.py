from __future__ import annotations

from typing import List, Tuple


def schedule_retries(requests_path: str, results_path: str, retry_delay_seconds: int) -> List[Tuple[int, str]]:
    raise NotImplementedError


def dedupe_latest_retry(requests_path: str, results_path: str, retry_delay_seconds: int) -> List[Tuple[int, str]]:
    raise NotImplementedError
