from __future__ import annotations

from pathlib import Path

from .nodes import Include, Text, Variable
from .parser import parse


class DictTemplateLoader:
    def __init__(self, templates: dict[str, str]) -> None:
        self._templates = dict(templates)
        self._cache: dict[str, list[Text | Variable | Include]] = {}

    def load(self, name: str) -> list[Text | Variable | Include]:
        cache_key = Path(name).name
        if cache_key not in self._cache:
            try:
                source = self._templates[name]
            except KeyError as error:
                raise FileNotFoundError(name) from error
            self._cache[cache_key] = parse(source)
        return self._cache[cache_key]

