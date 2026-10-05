from __future__ import annotations

from .models import InternalRecord, ProcessorRecord


def _fields(line: str) -> list[str]:
    return [field.strip() for field in line.split(",")]


def parse_internal(lines: list[str]) -> list[InternalRecord]:
    records = []
    for line in lines:
        fields = _fields(line)
        if len(fields) != 4:
            continue
        internal_id, processor_id, raw_amount, currency = fields
        try:
            amount = int(raw_amount)
        except ValueError:
            continue
        if not internal_id or not processor_id or amount == 0:
            continue
        if len(currency) != 3 or not currency.isupper():
            continue
        records.append(InternalRecord(internal_id, processor_id, amount, currency))
    return records


def parse_processor(lines: list[str]) -> list[ProcessorRecord]:
    records = []
    for input_index, line in enumerate(lines):
        fields = _fields(line)
        if len(fields) != 4:
            continue
        processor_id, raw_amount, currency, status = fields
        try:
            amount = int(raw_amount)
        except ValueError:
            continue
        if not processor_id or amount == 0:
            continue
        if len(currency) != 3 or not currency.isupper():
            continue
        if status not in {"SUCCEEDED", "REFUNDED", "FAILED"}:
            continue
        records.append(ProcessorRecord(processor_id, amount, currency, status, input_index))
    return records


def format_result(internal_id: str, result: str, processor_id: str) -> str:
    return f"{internal_id},{result},{processor_id}"

