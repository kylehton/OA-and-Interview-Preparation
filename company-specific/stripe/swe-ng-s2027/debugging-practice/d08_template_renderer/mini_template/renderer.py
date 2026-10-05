from __future__ import annotations

import html
from collections.abc import Mapping
from typing import Any

from .loader import DictTemplateLoader
from .nodes import Include, Text, Variable


class TemplateRenderer:
    def __init__(self, loader: DictTemplateLoader) -> None:
        self._loader = loader

    def render(self, name: str, context: Mapping[str, Any]) -> str:
        return self._render_nodes(self._loader.load(name), context)

    def _render_nodes(
        self,
        nodes: list[Text | Variable | Include],
        context: Mapping[str, Any],
    ) -> str:
        output = []
        for node in nodes:
            if isinstance(node, Text):
                output.append(node.value)
            elif isinstance(node, Variable):
                value = self._lookup(context, node.name)
                rendered = "" if value is None else str(value)
                output.append(rendered if node.raw else html.escape(rendered, quote=False))
            else:
                output.append(self._render_nodes(self._loader.load(node.name), {}))
        return "".join(output)

    @staticmethod
    def _lookup(context: Mapping[str, Any], name: str) -> Any:
        current: Any = context
        for part in name.split("."):
            if not isinstance(current, Mapping) or part not in current:
                return None
            current = current[part]
        return current

