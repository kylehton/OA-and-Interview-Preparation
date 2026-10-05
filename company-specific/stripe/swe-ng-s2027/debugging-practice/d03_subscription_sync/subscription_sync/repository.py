from .models import Subscription


class SubscriptionRepository:
    _records: dict[str, Subscription] = {}

    def get(self, subscription_id: str) -> Subscription | None:
        return self._records.get(subscription_id)

    def save(self, subscription: Subscription) -> None:
        self._records[subscription.subscription_id] = subscription

