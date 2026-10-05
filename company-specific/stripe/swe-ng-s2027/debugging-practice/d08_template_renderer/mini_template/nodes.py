from dataclasses import dataclass


@dataclass(frozen=True)
class Text:
    value: str


@dataclass(frozen=True)
class Variable:
    name: str
    raw: bool = False


@dataclass(frozen=True)
class Include:
    name: str

