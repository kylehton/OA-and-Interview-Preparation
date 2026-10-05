# P06 — Invoice Lifecycle

**Difficulty:** Medium  
**Target:** 50 minutes  
**Entry point:** `process_invoices(commands) -> list[str]`

Process whitespace-separated commands in order. Return one response per command.
Invalid commands return `ERROR` and do not mutate or reserve any identifier.
Currency codes are exactly three uppercase ASCII letters.

## Part 1 — Draft invoices and line items

```text
CREATE <invoice_id> <customer_id> <currency>
ADD <invoice_id> <line_id> <positive_amount>
TOTAL <invoice_id>
```

Invoice IDs are unique. New invoices are `DRAFT`. Line IDs must be unique
within an invoice, and lines may be added only while it is `DRAFT`. `TOTAL`
returns the sum of its line items in minor units.

## Part 2 — Finalization and partial payment

```text
FINALIZE <invoice_id>
PAY <invoice_id> <payment_id> <positive_amount>
```

A non-empty draft can be finalized into `OPEN`. An open invoice accepts a
payment no larger than its outstanding amount. It stays `OPEN` after a partial
payment and becomes `PAID` when paid in full. Payment IDs are globally unique.

## Part 3 — Status and voiding

```text
STATUS <invoice_id>
VOID <invoice_id>
```

Status returns `<state>,<total>,<paid>`. A draft may be voided. An open invoice
may be voided only before any payment. `PAID` and already `VOID` invoices cannot
be voided. A void invoice accepts no further mutation.

## Part 4 — Refunds

```text
REFUND <invoice_id> <refund_id> <positive_amount>
```

Refund IDs share the global transaction-ID namespace with payment IDs. A refund
may be applied to an `OPEN` or `PAID` invoice when the amount does not exceed
the invoice's currently paid amount. Subtract it from `paid`; the invoice state
then becomes `OPEN`. (Its original total never changes.)

## Example

```python
process_invoices([
    "CREATE inv1 cus1 USD",
    "ADD inv1 setup 300",
    "ADD inv1 usage 200",
    "FINALIZE inv1",
    "PAY inv1 pay1 500",
    "REFUND inv1 ref1 125",
    "STATUS inv1",
])
# ["OK", "OK", "OK", "OK", "OK", "OK", "OPEN,500,375"]
```

