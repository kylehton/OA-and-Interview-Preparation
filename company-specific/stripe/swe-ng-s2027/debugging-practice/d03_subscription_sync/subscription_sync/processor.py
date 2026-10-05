from __future__ import annotations

from .models import Subscription
from .repository import SubscriptionRepository


class SubscriptionProcessor:
    _supported = {"CREATED", "PAUSED", "RESUMED", "CANCELED"}

    def __init__(self, repository: SubscriptionRepository) -> None:
        self._repository = repository
        self._processed_event_ids: set[str] = set()

    def process(self, event: dict[str, str]) -> str:
        required = {"event_id", "subscription_id", "version", "type"}
        if required - event.keys():
            raise ValueError("missing event field")
        if not event["event_id"] or not event["subscription_id"]:
            raise ValueError("empty identifier")
        if not event["version"].isdigit() or int(event["version"]) <= 0:
            raise ValueError("invalid version")
        if event["type"] not in self._supported:
            raise ValueError("invalid event type")

        event_id = event["event_id"]
        if event_id in self._processed_event_ids:
            return "DUPLICATE"
        self._processed_event_ids.add(event_id)

        subscription_id = event["subscription_id"]
        version = event["version"]
        current = self._repository.get(subscription_id)
        if current is not None and version <= str(current.version):
            return "STALE"

        event_type = event["type"]
        if event_type == "CREATED":
            if current is not None:
                return "IGNORED"
            next_state = "ACTIVE"
        elif current is None:
            return "IGNORED"
        elif event_type == "PAUSED" and current.state == "ACTIVE":
            next_state = "PAUSED"
        elif event_type == "RESUMED" and current.state in {"PAUSED", "CANCELED"}:
            next_state = "ACTIVE"
        elif event_type == "CANCELED" and current.state in {"ACTIVE", "PAUSED"}:
            next_state = "CANCELED"
        else:
            return "IGNORED"

        self._repository.save(Subscription(subscription_id, next_state, version))
        return "APPLIED"

