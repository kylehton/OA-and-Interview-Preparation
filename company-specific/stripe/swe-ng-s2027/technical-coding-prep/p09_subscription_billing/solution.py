"""Starter for P09. Read README.md before implementing."""

from __future__ import annotations

import io
import csv
class SubscriptionManager:
    def __init__(self):
        self.plans = {}
        self.subscriptions = {}

    def parse_csv_input(self, input: str) -> list[str] | None:
        try:
            parts = next(csv.reader([input], strict=True))
            parts = [part.strip() for part in parts]
            if len(parts) != 0:
                return parts
        except csv.Error:
            return None
        return None

    def to_csv_output(self, to_output: list[str]) -> str | None:
        output = io.StringIO()
        writer = csv.writer(output, lineterminator="")
        writer.writerow(to_output)
        return output.getvalue()

    def process_plans(self, plans: list[str]):
        for plan in plans:
            parsed_input = self.parse_csv_input(plan)
            if parsed_input is not None:
                if all(value.isnumeric() and int(value) > 0 for value in parsed_input[1:]):
                    plan_id, period_fee, included_units, price_per_unit = parsed_input
                    if plan_id not in self.plans:
                        self.plans[plan_id] = [int(period_fee), int(included_units), int(price_per_unit)]

    def process_subscriptions(self, subscriptions: list[str]):
        for subscription in subscriptions:
            parsed_input = self.parse_csv_input(subscription)
            if parsed_input is not None:
                sub_id, customer_id, plan_id, start, end = parsed_input
                if plan_id in self.plans and sub_id not in self.subscriptions:
                    if start.isnumeric() and end.isnumeric() and int(start) > 0 and int(end) > 0:
                        self.subscriptions[sub_id] = [customer_id, plan_id, int(start), int(end)]

    def return_subscriptions(self):
        subs = list(self.subscriptions.values())
        for subscription in self.subscriptions:
            

def generate_invoices(
    plans: list[str],
    subscriptions: list[str],
    usage: list[str],
    period_start: int,
    period_end: int,
) -> list[str]:
    """Return one invoice line per valid subscription."""
    

