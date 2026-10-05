from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    captured_at: datetime
    transaction_id: str
    merchant_id: str
    currency: str
    amount: int

