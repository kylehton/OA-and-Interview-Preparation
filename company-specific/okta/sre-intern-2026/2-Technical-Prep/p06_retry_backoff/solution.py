from __future__ import annotations

from typing import Callable, TypeVar
import time

T = TypeVar("T")


def retry(
    operation: Callable[[], T],
    retries: int,
    base_delay: float,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    raise NotImplementedError


def retry_with_jitter(
    operation: Callable[[], T],
    retries: int,
    base_delay: float,
    jitter_fn: Callable[[], float],
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    raise NotImplementedError
