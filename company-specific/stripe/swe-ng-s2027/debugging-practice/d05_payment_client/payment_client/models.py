from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: Mapping[str, Any] = field(default_factory=dict)
    headers: Mapping[str, str] = field(default_factory=dict)


class PaymentError(RuntimeError):
    pass

