from __future__ import annotations

from typing import Callable, Type, TypeVar
import time

T = TypeVar("T")

# RuntimeError, TypeError, ValueError

def retry(
    operation: Callable[[], T],
    retries: int,
    base_delay: float,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    prev_exception = None
    attempts = 0
    while (attempts <= retries):
        try:
            return_val = operation()
            return return_val
        except Exception as e:
            prev_exception = e
            if attempts == retries:
                raise ValueError(e)
            else:
                sleep_fn(base_delay * (2 ** attempts))
                attempts += 1
    return prev_exception

def retry_with_jitter(
    operation: Callable[[], T],
    retries: int,
    base_delay: float,
    jitter_fn: Callable[[], float],
    sleep_fn: Callable[[float], None] = time.sleep,
) -> T:
    prev_exception = None
    attempts = 0
    while (attempts <= retries):
        try:
            return_val = operation()
            return return_val
        except Exception as e:
            prev_exception = e
            if attempts == retries:
                raise ValueError(e)
            else:
                sleep_fn(base_delay * (2 ** attempts) + jitter_fn())
                attempts += 1
    return prev_exception
