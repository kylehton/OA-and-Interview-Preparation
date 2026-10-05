from __future__ import annotations

from collections import defaultdict

from .csvio import format_result, parse_internal, parse_processor


def reconcile(
    internal_lines: list[str],
    processor_lines: list[str],
    *,
    include_orphans: bool = False,
) -> list[str]:
    internal_records = parse_internal(internal_lines)
    processor_records = parse_processor(processor_lines)
    by_id = defaultdict(list)
    for record in processor_records:
        by_id[record.processor_id].append(record)

    results = []
    matched_indexes: set[int] = set()
    for internal in internal_records:
        candidates = by_id[internal.processor_id]
        exact = next(
            (
                candidate
                for candidate in candidates
                if candidate.amount == internal.amount
                and candidate.currency == internal.currency
                and candidate.status == "SUCCEEDED"
            ),
            None,
        )
        if exact is not None:
            results.append(format_result(internal.internal_id, "MATCH", exact.processor_id))
            matched_indexes.add(exact.input_index)
        elif candidates:
            selected = candidates[0]
            results.append(format_result(internal.internal_id, "MISMATCH", selected.processor_id))
            matched_indexes.add(selected.input_index)
        else:
            results.append(format_result(internal.internal_id, "MISSING", "-"))

    if include_orphans:
        for record in processor_records:
            if record.input_index not in matched_indexes:
                results.append(format_result("-", "ORPHAN", record.processor_id))
    return results

