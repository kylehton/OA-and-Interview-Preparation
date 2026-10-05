import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1]))

from webhook_delivery import Event, MemoryEventStore, Response, WebhookWorker


class ScriptedSender:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = 0

    def __call__(self, event):
        self.calls += 1
        return self.responses.pop(0)


def make_worker(responses, *, attempts=3, base_delay=1):
    sender = ScriptedSender(responses)
    store = MemoryEventStore()
    sleeps = []
    worker = WebhookWorker(
        sender, store, sleeps.append, max_attempts=attempts, base_delay=base_delay
    )
    return worker, sender, store, sleeps


def test_delivers_200_and_deduplicates_success():
    worker, sender, _, _ = make_worker([Response(200)])
    event = Event("evt_1", "{}")
    assert worker.deliver(event).outcome == "DELIVERED"
    assert worker.deliver(event).outcome == "DUPLICATE"
    assert sender.calls == 1


def test_every_2xx_status_is_success():
    worker, sender, _, sleeps = make_worker([Response(204)])
    assert worker.deliver(Event("evt_1", "{}")).outcome == "DELIVERED"
    assert sender.calls == 1
    assert sleeps == []


def test_retries_server_error_with_exponential_delay():
    worker, sender, _, sleeps = make_worker([Response(503), Response(200)], base_delay=2)
    result = worker.deliver(Event("evt_1", "{}"))
    assert result == result.__class__("DELIVERED", 2)
    assert sender.calls == 2
    assert sleeps == [2]


def test_429_uses_retry_after_and_then_retries():
    worker, sender, _, sleeps = make_worker(
        [Response(429, {"Retry-After": "7"}), Response(200)], base_delay=2
    )
    assert worker.deliver(Event("evt_1", "{}")).outcome == "DELIVERED"
    assert sender.calls == 2
    assert sleeps == [7]


def test_non_rate_limit_4xx_is_not_retried():
    worker, sender, store, sleeps = make_worker([Response(400)])
    result = worker.deliver(Event("evt_1", "{}"))
    assert result.outcome == "FAILED"
    assert sender.calls == 1
    assert sleeps == []
    assert not store.is_processed("evt_1")


def test_exhausted_delivery_is_not_marked_processed():
    responses = [Response(500), Response(500), Response(500), Response(200)]
    worker, sender, store, _ = make_worker(responses, attempts=3)
    event = Event("evt_1", "{}")
    assert worker.deliver(event).outcome == "FAILED"
    assert not store.is_processed(event.event_id)
    assert worker.deliver(event).outcome == "DELIVERED"
    assert sender.calls == 4

