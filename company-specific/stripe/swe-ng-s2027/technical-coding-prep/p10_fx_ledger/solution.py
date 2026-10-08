"""Starter for P10. Read README.md before implementing."""
# conceptual breakdown
# this function:
# 1. takes a list of commands [OPEN, DEPOSIT, BALANCE, RATE, CONVERT]
# 2. creates user accounts with an assoc. currency
# 3. allows deposit of positive int amounts into user account, and check balance
# 4. allows for the creation of rates for foreign exchange
# 5. processes currency conversions for a given account (from currency must match current stored active currency), and the timestamp
# of the conversion ties to the timestamp of the rate, where a conversion uses the registered direct rate with the greatest timestamp
# NOT EXCEEDING the current conversion timestamp [converted = amount * numerator // denominator]
# rates are not guaranteed to be in-order, so need to get ALL rates before processing conversions
# if no elig. direct date exists, use newest elig. reverse rate [converted = amount * denominator // numerator]

# return ERROR on all failures, OK for success besides balance
# currency = 3 uppercase ascii char
# ids nonempty
# account and transaction ids are globally unique

# store rates as {(from_currency, to_currency): [(timestamp, numerator, denominator), ...]}; can check inverse rate by checking 
# 2-tuple key and its reverse against map
# store accounts as {account_id: holdings} where holdings = {currency: amount}
# store set for transactions
# search for the proper rate in backwards order (latest in command wins)

from __future__ import annotations

class FxProcessor:
    def __init__(self):
        self.accounts = {}
        self.rates = {}
        self.transactions = set()

    def parse_input(self, input: str) -> list[str] | None:
        parts = input.strip().split()
        parts = [part.strip() for part in parts]
        if len(parts) != 0:
            return parts
        return None

    def valid_currency(self, currency: str) -> bool:
        return len(currency) == 3 and currency.isascii() and currency.isupper() and currency.isalpha()

    def can_parse_int(self, num: str) -> bool:
        if not num.isdecimal():
            return False
        try:
            int(num)
        except ValueError:
            return False
        return True
 
    def valid_num(self, num: str) -> bool:
        return self.can_parse_int(num) and int(num) >= 0

    def create_account(self, account_id: str, base_currency: str) -> str:
        if account_id not in self.accounts and self.valid_currency(base_currency):
            self.accounts[account_id] = ()
            self.accounts[account_id] = (base_currency, {})
            self.accounts[account_id][1][base_currency] = 0
            return 'OK'
        return 'ERROR'

    def check_balance(self, account_id: str, currency: str) -> str:
        if account_id in self.accounts:
            if currency in self.accounts[account_id][1]:
                return str(self.accounts[account_id][1][currency])
            return '0'
        return 'ERROR'

    def deposit_amount(self, transaction_id: str, account_id: str, currency: str, amount: int):
        if transaction_id not in self.transactions and account_id in self.accounts:
            holdings = self.accounts[account_id][1]
            holdings[currency] = holdings.get(currency, 0) + amount
            self.transactions.add(transaction_id)
            return 'OK'
        return 'ERROR'

    def create_rate(self, timestamp: int, from_c: str, to_c: str, numer: int, denom: int) -> str:
        key = (from_c, to_c)
        if from_c == to_c:
            return 'ERROR'
        if key not in self.rates:
            self.rates[key] = []
        self.rates[key].append((timestamp, numer, denom))
        self.rates[key].sort(key=lambda x: x[0])
        return 'OK'

    def get_rate(self, timestamp: int, from_c: str, to_c: str) -> tuple[int | None, int | None]:
        key, inv_key = (from_c, to_c), (to_c, from_c)
        n, d = None, None
        if key in self.rates or inv_key in self.rates:
            if key in self.rates:
                valid_rates = self.rates[key]
                for i in range(len(valid_rates)-1, -1, -1):
                    curr_rate = valid_rates[i]
                    if curr_rate[0] <= timestamp:
                        n, d = curr_rate[1], curr_rate[2]
                        break
            if not n and not d and inv_key in self.rates:
                valid_rates = self.rates[inv_key]
                for i in range(len(valid_rates)-1, -1, -1):
                    curr_rate = valid_rates[i]
                    if curr_rate[0] <= timestamp:
                        n, d = curr_rate[2], curr_rate[1]
                        break
        return n, d # returns none if rate and inv_rate not found

    def process_amount(self, transaction_id: str, timestamp: int, from_account_id: str, to_account_id: str, from_c: str, to_c: str, amount: int) -> str:
        if transaction_id not in self.transactions and from_account_id in self.accounts and to_account_id in self.accounts:
            from_holdings = self.accounts[from_account_id][1]
            to_holdings = self.accounts[to_account_id][1]
            if from_c in from_holdings and from_holdings[from_c] >= amount:
                n, d = self.get_rate(timestamp, from_c, to_c)
                if n and d:
                    converted = amount * n // d
                    if converted > 0:
                        from_holdings[from_c] -= amount
                        to_holdings[to_c] = to_holdings.get(to_c, 0) + converted
                        self.transactions.add(transaction_id)
                        return 'OK'
                else: # rate not found, check if transfer
                    base_from, base_to = self.accounts[from_account_id][0], self.accounts[to_account_id][0]
                    if from_account_id != to_account_id and base_from == base_to:
                        from_holdings[from_c] -= amount
                        to_holdings[to_c] = to_holdings.get(to_c, 0) + amount
                        self.transactions.add(transaction_id)
                        return 'OK'
        return 'ERROR'

    def process_command(self, command: str):
        parts = self.parse_input(command)
        response = 'ERROR'
        if parts is not None and len(parts) != 0:
            operation = parts[0]
            if len(parts) == 3:
                account_id, currency = parts[1], parts[2]               
                if account_id and self.valid_currency(currency):
                    if operation == 'OPEN':
                        response = self.create_account(account_id, currency)
                    elif operation == 'BALANCE':
                        response = self.check_balance(account_id, currency)
            elif len(parts) == 5:
                if operation == 'DEPOSIT':
                    transaction_id, account_id, currency, amount = parts[1:]
                    if transaction_id and account_id and self.valid_currency(currency) and self.valid_num(amount):
                        if int(amount) > 0:
                            response = self.deposit_amount(transaction_id, account_id, currency, int(amount))
            elif len(parts) == 6:
                if operation == 'RATE':
                    timestamp, from_currency, to_currency, numerator, denominator = parts[1:]
                    if self.valid_currency(from_currency) and self.valid_currency(to_currency):
                        if self.valid_num(timestamp) and self.valid_num(numerator) and self.valid_num(denominator):
                            timestamp, numerator, denominator = int(timestamp), int(numerator), int(denominator)
                            if numerator > 0 and denominator > 0:
                                response = self.create_rate(timestamp, from_currency, to_currency, numerator, denominator)
                elif operation == 'TRANSFER':
                    transaction_id, timestamp, source, destination, amount = parts[1:]
                    if transaction_id and self.valid_num(timestamp) and self.valid_num(amount) and source != destination:
                        timestamp, amount = int(timestamp), int(amount)
                        if amount > 0 and source in self.accounts and destination in self.accounts:
                            source_base = self.accounts[source][0]
                            destination_base = self.accounts[destination][0]
                            response = self.process_amount(transaction_id, timestamp, source, destination, source_base, destination_base, amount)
            elif len(parts) == 7:
                if operation == 'CONVERT':
                    transaction_id, timestamp, account_id, from_currency, to_currency, amount = parts[1:]
                    if transaction_id and account_id and self.valid_currency(from_currency) and self.valid_currency(to_currency):
                        if self.valid_num(timestamp) and self.valid_num(amount):
                            timestamp, amount = int(timestamp), int(amount)
                            if amount > 0:
                                response = self.process_amount(transaction_id, timestamp, account_id, account_id, from_currency, to_currency, amount)
        return response

def process_ledger(commands: list[str]) -> list[str]:
    """Execute FX-ledger commands and return one response per command."""
    fxProcessor = FxProcessor()
    responses = []
    for command in commands:
        responses.append(fxProcessor.process_command(command))
    return responses

