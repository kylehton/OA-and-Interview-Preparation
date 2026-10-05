from __future__ import annotations

from collections import defaultdict
from datetime import date, time, timedelta

from .calendar import next_business_day, normalize_business_day
from .parser import parse_transactions


def schedule_payouts(
    transaction_lines: list[str],
    delay_business_days: int,
    holidays: list[str] | None = None,
) -> list[str]:
    if delay_business_days < 0:
        raise ValueError("negative payout delay")
    holiday_dates = {date.fromisoformat(value) for value in (holidays or [])}
    grouped: dict[tuple[date, str], tuple[str, int]] = {}

    for transaction in parse_transactions(transaction_lines):
        captured = transaction.captured_at
        effective = captured.date()
        if captured.time() > time(17, 0):
            effective += timedelta(days=1)
        payout_date = normalize_business_day(effective, holiday_dates)
        for _ in range(delay_business_days):
            payout_date = next_business_day(payout_date, holiday_dates)

        key = (payout_date, transaction.merchant_id)
        if key not in grouped:
            grouped[key] = (transaction.currency, 0)
        currency, amount = grouped[key]
        grouped[key] = (currency, amount + transaction.amount)

    rows = []
    for (payout_date, merchant_id), (currency, amount) in sorted(grouped.items()):
        rows.append(f"{payout_date.isoformat()},{merchant_id},{currency},{amount}")
    return rows

