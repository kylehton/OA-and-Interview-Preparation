"""Starter for P06. Read README.md before implementing."""

from __future__ import annotations

# each invoice needs: customer id, currency, draft=bool, line dict storing lines with unique id
class Invoice:
    def __init__(self, customer_id, currency, state='DRAFT'):
        self.customer_id = customer_id
        self.currency = currency
        self.state = state
        self.total = 0
        self.paid = 0
        self.lines = {}
        self.firstPayment = False

    def addLine(self, line_id: str, amount: int) -> str:
        if line_id not in self.lines:
            self.lines[line_id] = amount
            self.total += amount
            return 'OK'
        return 'ERROR'

    def numLines(self):
        return len(self.lines)

    def hasFirstPayment(self):
        return self.firstPayment

# DRAFT -> OPEN, VOID
# VOID -> none
# OPEN -> PAID

    def setState(self, state):
        if state == 'VOID':
            if self.state != 'DRAFT' and self.state != 'OPEN':
                return False
            elif (self.state == 'OPEN' and self.hasFirstPayment()):
                return False
        if state == 'PAID':
            if self.state != 'OPEN':
                return False
        if state == 'OPEN':
            if self.state != 'DRAFT' and self.state != 'PAID':
                return False
        self.state = state
        return True

    def getState(self):
        return self.state

    def getTotal(self):
        return self.total

    def getPaid(self):
        return self.paid
    
    def getRemaining(self):
        return self.total - self.paid

    def pay(self, amount: int):
        if amount <= self.getRemaining():
            if amount == self.getRemaining():
                self.setState('PAID')
            self.paid += amount
            self.firstPayment = True
            return True
        return False

    def getStatus(self):
        return f'{self.getState()},{self.getTotal()},{self.getPaid()}'

    def process_refund(self, amount: int):
        if self.state == 'OPEN' or self.state == 'PAID':
            if amount <= self.paid:
                self.paid -= amount
                if self.state == 'PAID':
                    self.state = 'OPEN'
                return True
        return False
            
class InvoiceProcessor:
    def __init__(self):
        self.invoices = {}
        self.payments = {}

    def process_invoice(self, command: str) -> str:
        parts = command.strip().split()
        if len(parts) == 2:
            operation = parts[0].strip()
            if operation == 'TOTAL':
                invoice_id = parts[1].strip()
                if invoice_id in self.invoices:
                    obj = self.invoices[invoice_id]
                    return str(obj.getTotal())
            elif operation == 'FINALIZE':
                invoice_id = parts[1].strip()
                if invoice_id in self.invoices:
                    obj = self.invoices[invoice_id]
                    if (obj.numLines()) > 0 and obj.setState('OPEN'):
                        return 'OK'
            elif operation == 'STATUS':
                invoice_id = parts[1].strip()
                if invoice_id in self.invoices:
                    obj = self.invoices[invoice_id]
                    return obj.getStatus()
            elif operation == 'VOID':
                invoice_id = parts[1].strip()
                if invoice_id in self.invoices:
                    obj = self.invoices[invoice_id]
                    if obj.setState('VOID'):
                        return 'OK'
        elif len(parts) == 4:
            operation = parts[0].strip()
            invoice_id = parts[1].strip()
            if len(invoice_id) != 0:
                if invoice_id not in self.invoices:
                    if operation == 'CREATE':
                        customer_id = parts[2].strip()
                        currency = parts[3].strip()
                        if len(customer_id) != 0 and currency.isascii() and currency.isupper() and len(currency) == 3:
                            self.invoices[invoice_id] = Invoice(customer_id, currency)
                            return 'OK'
                else:
                    if operation == 'ADD':
                        line_id = parts[2].strip()
                        amount = parts[3].strip()
                        if amount.isnumeric() and int(amount) > 0:
                            obj = self.invoices[invoice_id]
                            if obj.getState() == 'DRAFT':
                                return obj.addLine(line_id, int(amount))
                    elif operation == 'PAY':
                        payment_id = parts[2].strip()
                        amount = parts[3].strip()
                        if payment_id not in self.payments and amount.isnumeric() and int(amount) > 0:
                            obj = self.invoices[invoice_id]
                            if obj.getState() == 'OPEN':
                                if obj.pay(int(amount)):
                                    self.payments[payment_id] = [invoice_id, amount]
                                    return 'OK'
                    elif operation == 'REFUND':
                        refund_id = parts[2].strip()
                        amount = parts[3].strip()
                        if refund_id not in self.payments and amount.isnumeric() and int(amount) > 0:
                            obj = self.invoices[invoice_id]
                            if obj.getState() == 'OPEN' or obj.getState() == 'PAID':
                                if obj.process_refund(int(amount)):
                                    self.payments[refund_id] = [invoice_id, amount]
                                    return 'OK'

        return 'ERROR'
                    


def process_invoices(commands: list[str]) -> list[str]:
    """Execute invoice commands and return one response per command."""
    invoiceProcessor = InvoiceProcessor()
    responses = []
    for command in commands:
        responses.append(invoiceProcessor.process_invoice(command))
    return responses

