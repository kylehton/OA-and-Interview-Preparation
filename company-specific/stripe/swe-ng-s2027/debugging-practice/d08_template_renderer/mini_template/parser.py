from __future__ import annotations

import re

from .nodes import Include, Text, Variable


TOKEN = re.compile(r"(\{\{.*?\}\}|\{%.*?%\})")
INCLUDE = re.compile(r'^include\s+["\'](.+)["\']$')


def parse(source: str) -> list[Text | Variable | Include]:
    nodes: list[Text | Variable | Include] = []
    position = 0
    for match in TOKEN.finditer(source):
        if match.start() > position:
            nodes.append(Text(source[position : match.start()]))
        token = match.group(0)
        if token.startswith("{{{"):
            nodes.append(Variable(token[3:-3].strip(), raw=True))
        elif token.startswith("{{"):
            nodes.append(Variable(token[2:-2].strip()))
        else:
            directive = token[2:-2].strip()
            include = INCLUDE.match(directive)
            if include is None:
                raise ValueError(f"unknown directive: {directive}")
            nodes.append(Include(include.group(1)))
        position = match.end()
    if position < len(source):
        nodes.append(Text(source[position:]))
    return nodes

