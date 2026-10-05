import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from subscription_sync import SubscriptionProcessor, SubscriptionRepository


def event(event_id, subscription_id, version, event_type):
    return {
        "event_id": event_id,
        "subscription_id": subscription_id,
        "version": str(version),
        "type": event_type,
    }


def test_basic_lifecycle():
    repo = SubscriptionRepository()
    processor = SubscriptionProcessor(repo)
    assert processor.process(event("life-1", "life-sub", 1, "CREATED")) == "APPLIED"
    assert processor.process(event("life-2", "life-sub", 2, "PAUSED")) == "APPLIED"
    assert processor.process(event("life-3", "life-sub", 3, "RESUMED")) == "APPLIED"
    assert repo.get("life-sub").state == "ACTIVE"


def test_duplicate_event_is_not_applied_twice():
    repo = SubscriptionRepository()
    processor = SubscriptionProcessor(repo)
    item = event("dup-1", "dup-sub", 1, "CREATED")
    assert processor.process(item) == "APPLIED"
    assert processor.process(item) == "DUPLICATE"


def test_versions_are_compared_numerically():
    repo = SubscriptionRepository()
    processor = SubscriptionProcessor(repo)
    assert processor.process(event("ver-1", "ver-sub", 2, "CREATED")) == "APPLIED"
    assert processor.process(event("ver-2", "ver-sub", 10, "PAUSED")) == "APPLIED"
    assert repo.get("ver-sub").version == 10


def test_cancellation_is_terminal():
    repo = SubscriptionRepository()
    processor = SubscriptionProcessor(repo)
    processor.process(event("cancel-1", "cancel-sub", 1, "CREATED"))
    processor.process(event("cancel-2", "cancel-sub", 2, "CANCELED"))
    assert processor.process(event("cancel-3", "cancel-sub", 3, "RESUMED")) == "IGNORED"
    assert repo.get("cancel-sub").state == "CANCELED"


def test_repository_instances_are_isolated():
    first = SubscriptionRepository()
    second = SubscriptionRepository()
    SubscriptionProcessor(first).process(event("iso-1", "iso-sub", 1, "CREATED"))
    assert second.get("iso-sub") is None


def test_malformed_event_does_not_reserve_its_id():
    processor = SubscriptionProcessor(SubscriptionRepository())
    with pytest.raises(ValueError):
        processor.process({"event_id": "retry-id"})
    assert processor.process(event("retry-id", "retry-sub", 1, "CREATED")) == "APPLIED"


def test_stale_event_is_idempotently_recorded():
    processor = SubscriptionProcessor(SubscriptionRepository())
    processor.process(event("stale-1", "stale-sub", 5, "CREATED"))
    stale = event("stale-2", "stale-sub", 4, "PAUSED")
    assert processor.process(stale) == "STALE"
    assert processor.process(stale) == "DUPLICATE"

