from dataclasses import dataclass


@dataclass(frozen=True)
class Rate:
    timestamp: int
    numerator: int
    denominator: int

