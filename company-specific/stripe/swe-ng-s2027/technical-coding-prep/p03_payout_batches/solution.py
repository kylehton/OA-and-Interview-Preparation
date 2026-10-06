"""Starter for P03. Read README.md before implementing."""

from __future__ import annotations
class PaymentBatch:
    def __init__(self, min_amount: int=0, max_batch: int=0):
        self.payments = {}
        self.events = {}
        self.refunds = {}
        self.min_amount = min_amount
        self.max_batch_size = max_batch

    def handle_payment(self, merchant_id: str, currency: str, amount: int):
        if len(merchant_id) == 0 or len(currency) != 3 or not currency.isascii() or not currency.isalpha() or not currency.isupper() or amount <= 0:
            return False
        key = (merchant_id, currency)
        if key not in self.payments:
            self.payments[key] = [1, amount]
        else:
            self.payments[key][1] += amount
        return True

    def log_payments(self) -> list[str]:
        results = []
        for key, val in sorted(self.payments.items(), key=lambda x: x[0]):
            if val[1] >= self.min_amount and val[1] > 0:
                batch_num, curr_amt = val[0], val[1]
                if self.max_batch_size <= 0:
                    results.append(key[0] + "," + key[1] + "," + str(batch_num) + "," + str(curr_amt))
                else:
                    while curr_amt > 0:
                        results.append(key[0] + "," + key[1] + "," + str(batch_num) + "," + str(min(self.max_batch_size, curr_amt)))
                        curr_amt -= self.max_batch_size
                        batch_num += 1
        return results

    def record_event(self, operation, event_id, merchant_id, currency, amount):
            self.events[event_id] = [operation, merchant_id, currency, int(amount)]

    def handle_refund(self, payment_event_id, refund_amount):
        if payment_event_id in self.events:
            operation, merchant_id, currency, payment_amount = self.events[payment_event_id]
            key = (merchant_id, currency)
            if operation == 'PAYMENT' and key in self.payments:
                total_amount = self.payments[key][1]
                if 0 < refund_amount <= payment_amount:
                    self.payments[key][1] = total_amount - refund_amount
                    self.events[payment_event_id][3] = payment_amount - refund_amount
                    return True
        return False

    def process_events(self, event: str):
        parts = event.strip().split(',')
        if len(parts) == 4:
            operation = parts[0].strip()
            if operation == 'REFUND':
                event_id = parts[1].strip()
                payment_event_id = parts[2].strip()
                amount = parts[3].strip()
                if amount.isnumeric() and len(event_id) != 0 and event_id not in self.events:
                    if self.handle_refund(payment_event_id, int(amount)):
                        
                        _, merchant_id, currency, _ = self.events[payment_event_id]
                        self.record_event(operation, event_id, merchant_id, currency, amount)
        elif len(parts) == 5:
            operation = parts[0].strip()
            if operation == 'PAYMENT':
                event_id = parts[1].strip()
                merchant_id = parts[2].strip()
                currency = parts[3].strip()
                amount = parts[4].strip()
                if amount.isnumeric() and len(event_id) != 0 and event_id not in self.events:
                    if self.handle_payment(merchant_id, currency, int(amount)):
                        self.record_event(operation, event_id, merchant_id, currency, amount)
                
def create_payout_batches(
    events: list[str], minimum_amount: int = 0, max_batch_amount: int = 0
) -> list[str]:
    """Aggregate valid events and return deterministic payout batch lines."""
    paymentBatch = PaymentBatch(minimum_amount, max_batch_amount)
    responses = []
    for event in events:
        responses.append(paymentBatch.process_events(event))
    return paymentBatch.log_payments()
