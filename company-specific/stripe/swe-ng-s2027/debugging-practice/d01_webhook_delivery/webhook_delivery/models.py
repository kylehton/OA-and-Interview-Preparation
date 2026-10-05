from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class Event:
    event_id: str
    payload: str


@dataclass(frozen=True)
class Response:
    status_code: int
    headers: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class DeliveryResult:
    outcome: str
    attempts: int

