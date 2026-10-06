"""Starter for P02. Read README.md before implementing."""

from __future__ import annotations


class WalletCollection:
    def __init__(self):
        self.collection = {}
        self.transactions = {}

    def create_wallet(self, wallet_id: str):
        if wallet_id not in self.collection:
            self.collection[wallet_id] = 0
        else:
            return 'ERROR'
        return 'OK'

    def create_transaction(self, transac_id, wallet_id, amount: int, status=False):
        if transac_id in self.transactions:
            return 'ERROR'
        self.transactions[transac_id] = [wallet_id, amount, status]
        return 'OK'

    def mark_transaction_complete(self, transaction_id, status=True):
        if transaction_id not in self.transactions:
            return 'ERROR'
        self.transactions[transaction_id][2] = status
        return 'OK'

    def perform_transaction(self, command: str):
        parts = command.strip().split()
        if len(parts) >= 2:
            operation = parts[0].strip()
            if len(parts) == 2:
                wallet_id = parts[1].strip()
                if operation == 'CREATE':
                    return self.create_wallet(wallet_id)
                elif operation == 'BALANCE':
                    return self.get_balance(wallet_id)
            elif len(parts) == 3:
                if operation ==  'REVERSE':
                    reversal_id = parts[1].strip()
                    transac_id = parts[2].strip()
                    if reversal_id not in self.transactions and self.reverse_transaction(transac_id) == 'OK':
                        wallet_id, amount, _ = self.transactions[transac_id]
                        if self.mark_transaction_complete(transac_id) == 'OK':
                            if self.create_transaction(reversal_id, wallet_id, amount, True) == 'ERROR':
                                self.mark_transaction_complete(transac_id, False)
                            else:
                                return 'OK'
            elif len(parts) == 4:
                transaction_id = parts[1].strip()
                wallet_id = parts[2].strip()
                amount = parts[3].strip()
                if amount.isnumeric():
                    amount = int(amount)
                    if operation == 'CREDIT':
                            if transaction_id not in self.transactions and self.credit_wallet(wallet_id, amount) == 'OK':
                                if self.create_transaction(transaction_id, wallet_id, amount) == 'ERROR':
                                    self.debit_wallet(wallet_id, amount)
                                else:
                                    return 'OK'
                    elif operation == 'DEBIT':
                            if transaction_id not in self.transactions and self.debit_wallet(wallet_id, amount) == 'OK':
                                if self.create_transaction(transaction_id, wallet_id, -amount) == 'ERROR':
                                    self.credit_wallet(wallet_id, amount)
                                else:
                                    return 'OK'
            elif len(parts) == 5:
                if operation ==  'TRANSFER':
                    transaction_id = parts[1].strip()
                    source_id = parts[2].strip()
                    destination_id = parts[3].strip()
                    amount = parts[4].strip()
                    if amount.isnumeric():
                        amount = int(amount)
                        if self.transfer(source_id, destination_id, amount) == 'OK':
                            if self.create_transaction(transaction_id, (source_id, destination_id), amount) == 'ERROR':
                                self.transfer(destination_id, source_id, amount)
                            else:
                                return 'OK'
        return 'ERROR'

    def credit_wallet(self, wallet_id: str, amount: int):
        if wallet_id not in self.collection or int(amount) <= 0:
            return 'ERROR'
        self.collection[wallet_id] += amount
        return 'OK'

    def debit_wallet(self, wallet_id: str, amount: int):
        if wallet_id not in self.collection or amount <= 0 or amount > self.collection[wallet_id]:
            return 'ERROR'
        self.collection[wallet_id] -= amount
        return 'OK'

    # reverse cred req. amount still there, debit adds amt back
    def reverse_transaction(self, transaction_id: str):
        if transaction_id in self.transactions:
            wallet_id, amount, reversed = self.transactions[transaction_id]
            # added this if-else in order to deal with reversal of transfer op.
            if not reversed:
                if isinstance(wallet_id, tuple):
                    source, dest = wallet_id
                    return self.transfer(dest, source, amount)
                elif isinstance(wallet_id, str):
                    if amount > 0 and self.collection[wallet_id] < amount:
                        return 'ERROR'
                    self.collection[wallet_id] -= amount
                    return 'OK'
        return 'ERROR'

    def transfer(self, source_id: str, destination_id: str, amount: int):
        if source_id in self.collection and destination_id in self.collection and source_id != destination_id:
            if self.debit_wallet(source_id, amount) == 'OK':
                if self.credit_wallet(destination_id, amount) == 'ERROR':
                    self.credit_wallet(source_id, amount)
                else:
                    return 'OK'
        return 'ERROR'

    def get_balance(self, wallet_id: str):
        if wallet_id not in self.collection:
            return 'ERROR'
        return str(self.collection[wallet_id])

def process_commands(commands: list[str]) -> list[str]:
    """Process wallet commands and return one response per command."""
    wallet_collection = WalletCollection()
    responses = []
    for command in commands:
        responses.append(wallet_collection.perform_transaction(command))
    return responses
                   

