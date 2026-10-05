import sys
from copy import deepcopy
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))

from payment_client import HttpResponse, PaymentClient, PaymentError


class FakeTransport:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = []

    def post(self, path, body, headers):
        self.calls.append((path, deepcopy(body), dict(headers)))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


def client_for(outcomes, *, attempts=3, base_delay=1):
    transport = FakeTransport(outcomes)
    sleeps = []
    keys = iter(["key-1", "key-2", "key-3", "key-4"])
    client = PaymentClient(
        transport,
        sleeps.append,
        lambda: next(keys),
        max_attempts=attempts,
        base_delay=base_delay,
    )
    return client, transport, sleeps


def test_successful_200_returns_payment_id():
    client, transport, sleeps = client_for([HttpResponse(200, {"id": "pay_1"})])
    assert client.create_payment({"amount": 100}) == "pay_1"
    assert len(transport.calls) == 1
    assert sleeps == []


def test_every_2xx_status_is_successful():
    client, _, _ = client_for([HttpResponse(201, {"id": "pay_created"})])
    assert client.create_payment({"amount": 100}) == "pay_created"


def test_non_retryable_400_stops_immediately():
    client, transport, sleeps = client_for([HttpResponse(400)])
    with pytest.raises(PaymentError):
        client.create_payment({"amount": 100})
    assert len(transport.calls) == 1
    assert sleeps == []


def test_retries_reuse_key_and_body_without_mutating_caller():
    outcomes = [HttpResponse(500), HttpResponse(200, {"id": "pay_1"})]
    client, transport, sleeps = client_for(outcomes, base_delay=2)
    payload = {"amount": 100, "metadata": {"order": "o1"}}
    original = deepcopy(payload)
    assert client.create_payment(payload) == "pay_1"
    assert payload == original
    assert [call[1] for call in transport.calls] == [original, original]
    assert [call[2]["Idempotency-Key"] for call in transport.calls] == ["key-1", "key-1"]
    assert sleeps == [2]


def test_retry_after_is_a_minimum_delay():
    outcomes = [
        HttpResponse(429, headers={"Retry-After": "8"}),
        HttpResponse(200, {"id": "pay_1"}),
    ]
    client, _, sleeps = client_for(outcomes, base_delay=2)
    assert client.create_payment({"amount": 100}) == "pay_1"
    assert sleeps == [8]


def test_timeout_is_retryable():
    client, transport, sleeps = client_for(
        [TimeoutError(), HttpResponse(200, {"id": "pay_1"})], base_delay=3
    )
    assert client.create_payment({"amount": 100}) == "pay_1"
    assert len(transport.calls) == 2
    assert sleeps == [3]


def test_max_attempts_is_total_http_calls():
    client, transport, sleeps = client_for(
        [HttpResponse(500), HttpResponse(500), HttpResponse(500)], attempts=2
    )
    with pytest.raises(PaymentError):
        client.create_payment({"amount": 100})
    assert len(transport.calls) == 2
    assert sleeps == [1]

