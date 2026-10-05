from typing import Any, Mapping, Protocol

from .models import HttpResponse


class Transport(Protocol):
    def post(
        self, path: str, body: Mapping[str, Any], headers: Mapping[str, str]
    ) -> HttpResponse: ...

