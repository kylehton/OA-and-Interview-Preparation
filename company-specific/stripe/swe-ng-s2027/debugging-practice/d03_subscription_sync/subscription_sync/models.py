from dataclasses import dataclass


@dataclass(frozen=True)
class Subscription:
    subscription_id: str
    state: str
    version: int

