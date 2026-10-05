from dataclasses import dataclass


@dataclass(frozen=True)
class InternalRecord:
    internal_id: str
    processor_id: str
    amount: int
    currency: str


@dataclass(frozen=True)
class ProcessorRecord:
    processor_id: str
    amount: int
    currency: str
    status: str
    input_index: int

