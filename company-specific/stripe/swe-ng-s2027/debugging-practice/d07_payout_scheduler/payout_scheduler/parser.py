from __future__ import annotations

import csv
from datetime import datetime

from .models import Transaction


def parse_transactions(lines: list[str]) -> list[Transaction]:
    transactions = []
    seen_ids: set[str] = set()
    for row in csv.reader(lines):
        if len(row) != 6:
            continue
        raw_time, transaction_id, merchant_id, currency, raw_amount, status = (
            field.strip() for field in row
        )
        try:
            captured_at = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
            amount = int(raw_amount)
        except ValueError:
            continue
        if captured_at.tzinfo is None:
            continue
        if not transaction_id or not merchant_id or transaction_id in seen_ids:
            continue
        if len(currency) != 3 or not currency.isupper() or amount <= 0:
            continue
        if status != "CAPTURED":
            continue
        seen_ids.add(transaction_id)
        transactions.append(
            Transaction(captured_at, transaction_id, merchant_id, currency, amount)
        )
    return transactions

