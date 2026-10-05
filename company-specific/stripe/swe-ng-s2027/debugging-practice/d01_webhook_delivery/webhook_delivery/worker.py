from __future__ import annotations

from collections.abc import Callable

from .models import DeliveryResult, Event, Response
from .store import MemoryEventStore


class WebhookWorker:
    def __init__(
        self,
        sender: Callable[[Event], Response],
        store: MemoryEventStore,
        sleeper: Callable[[int], None],
        *,
        max_attempts: int = 3,
        base_delay: int = 1,
    ) -> None:
        self._sender = sender
        self._store = store
        self._sleeper = sleeper
        self._max_attempts = max_attempts
        self._base_delay = base_delay

    def deliver(self, event: Event) -> DeliveryResult:
        if self._store.is_processed(event.event_id):
            return DeliveryResult("DUPLICATE", 0)

        attempts = 0
        for attempt_index in range(self._max_attempts):
            response = self._sender(event)
            attempts += 1

            if response.status_code == 200:
                self._store.mark_processed(event.event_id)
                return DeliveryResult("DELIVERED", attempts)

            if 400 <= response.status_code < 500:
                return DeliveryResult("FAILED", attempts)

            if attempt_index < self._max_attempts - 1:
                delay = self._base_delay * (2**attempt_index)
                if response.status_code == 429:
                    retry_after = response.headers.get("Retry-After")
                    if retry_after and retry_after.isdigit():
                        delay = max(delay, int(retry_after))
                self._sleeper(delay)

        self._store.mark_processed(event.event_id)
        return DeliveryResult("FAILED", attempts)

