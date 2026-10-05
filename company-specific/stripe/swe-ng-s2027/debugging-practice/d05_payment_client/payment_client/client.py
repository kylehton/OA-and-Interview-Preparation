from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .models import PaymentError
from .transport import Transport


class PaymentClient:
    def __init__(
        self,
        transport: Transport,
        sleeper: Callable[[int], None],
        key_factory: Callable[[], str],
        *,
        max_attempts: int = 3,
        base_delay: int = 1,
    ) -> None:
        self._transport = transport
        self._sleeper = sleeper
        self._key_factory = key_factory
        self._max_attempts = max_attempts
        self._base_delay = base_delay

    def create_payment(self, payload: dict[str, Any]) -> str:
        last_error = "request failed"
        for attempt_index in range(self._max_attempts + 1):
            headers = {"Idempotency-Key": self._key_factory()}
            payload["attempt"] = attempt_index + 1
            try:
                response = self._transport.post("/payments", payload, headers)
            except TimeoutError:
                last_error = "request timed out"
                if attempt_index < self._max_attempts:
                    self._sleeper(self._base_delay * (2**attempt_index))
                continue

            if response.status_code == 200:
                payment_id = response.body.get("id")
                if not isinstance(payment_id, str) or not payment_id:
                    raise PaymentError("successful response has no payment id")
                return payment_id

            retryable = response.status_code == 429 or response.status_code >= 500
            if not retryable:
                raise PaymentError(f"non-retryable status {response.status_code}")

            last_error = f"retryable status {response.status_code}"
            if attempt_index < self._max_attempts:
                delay = self._base_delay * (2**attempt_index)
                retry_after = response.headers.get("Retry-After")
                if response.status_code == 429 and retry_after and retry_after.isdigit():
                    delay = max(delay, int(retry_after))
                self._sleeper(delay)

        raise PaymentError(last_error)

