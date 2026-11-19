# Transaction Fee Calculator — Parts 1–3

**Company:** Stripe  
**Difficulty:** Easy (Parts 1–2), Medium (Part 3)  
**Roles:** Full-Time, New Grad, Intern (Parts 1–2); Full-Time, New Grad (Part 3)  
**Interview Stage:** Phone Screen  
**Practice Status:** Parts 1–2 Attempted; Part 3 Attempted  
**Topics:** CSV Parsing, Fee Calculation, Conditional Rules, Dictionaries, Transaction Counting, Volume Discounts

---

## Problem Overview

Build a payment-platform transaction fee calculator. The input contains transactions encoded as CSV records. Calculate the fee for each transaction and emit a CSV result.

The problem evolves across three parts:

1. **Part 1 — Basic Fee Calculation:** Calculate fees using a provider-specific percentage and fixed charge.
2. **Part 2 — Conditional Fee Rules:** Charge only completed payments and apply special rates for Ireland.
3. **Part 3 — Volume-Based Discounts:** Read configurable country/provider fees and discount fees based on each merchant's number of successful transactions.

Parts 1–2 were presented together in the reported source. Part 3 was supplied as a separate follow-up exercise.

---

## Input CSV Format (All Parts)

The input `csvData` is one CSV string. Its first row is a header, and subsequent rows are transaction records.

```text
id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
```

| Column | Description |
|---|---|
| `id` | Unique transaction ID |
| `reference` | Transaction reference number |
| `amount` | Amount in cents (e.g., `1000` = $10.00) |
| `currency` | Currency code, such as `eur` or `usd` |
| `date` | Transaction date (`YYYY-MM-DD`) |
| `merchant_id` | Seller's account ID |
| `buyer_country` | Buyer's country code |
| `transaction_type` | Transaction kind, e.g., `payment` |
| `payment_provider` | Provider, e.g., `card`, `klarna`, `bank_transfer` |
| `status` | Status, e.g., `payment_completed`, `payment_failed`, `payment_pending` |

The header is not a transaction and should not be processed as one.

### Output Format

Produce the following CSV header followed by one output record per input transaction:

```text
id,transaction_type,payment_provider,fee
```

The reported source describes a newline-delimited CSV string. **For FastPrep, the function returns `String[]`: one CSV line per array element, including the output header.**

---

## Part 1 — Basic Fee Calculation

### Task

Read the CSV input and calculate a fee for **every** transaction based on `payment_provider`, regardless of payment status.

Each provider charges a percentage of the transaction amount plus a fixed fee, except bank transfer, which has only a percentage charge.

### Standard Fee Table

| Payment Provider | Percentage Rate | Fixed Fee |
|---|---:|---:|
| `card` | 2.9% | 30 cents |
| `klarna` | 3.5% | 50 cents |
| `bank_transfer` | 0.8% | 0 cents |

The final fee must be rounded **down** to a whole number of cents.

### Example — Part 1

**Input:**

```text
id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
py_1,1,1000,eur,2024-12-24,acct_1,ie,payment,card,payment_completed
py_2,2,2500,eur,2024-12-24,acct_2,de,payment,card,payment_failed
py_3,3,3400,eur,2024-12-25,acct_2,ie,payment,klarna,payment_completed
py_4,4,5000,eur,2024-12-25,acct_1,fr,payment,bank_transfer,payment_completed
```

**Output (CSV):**

```text
id,transaction_type,payment_provider,fee
py_1,payment,card,59
py_2,payment,card,102
py_3,payment,klarna,169
py_4,payment,bank_transfer,40
```

**Explanation:**

- `py_1`: 1000 × 0.029 + 30 = 59.
- `py_2`: 2500 × 0.029 + 30 = 102.5; round down to 102. A failed payment is still charged in **Part 1**.
- `py_3`: 3400 × 0.035 + 50 = 169.
- `py_4`: 5000 × 0.008 = 40.

### Requirements

1. Parse the input CSV and skip its header.
2. Select the correct provider-specific fee formula.
3. Calculate fees for every transaction in this part.
4. Round each final fee down to an integer.
5. Return the required CSV output.

---

## Part 2 — Conditional Fee Rules

### Task

Extend Part 1 with payment-status checks and country-specific rates.

### Rule A — Payment Status

- Calculate a fee **only** when `status == payment_completed`.
- If a payment failed or is pending, its fee is `0`.

### Rule B — Ireland-Specific Rates

For buyers in Ireland (`buyer_country == ie`), apply lower rates for `card` and `klarna`.

| Payment Provider | Ireland Percentage Rate | Ireland Fixed Fee |
|---|---:|---:|
| `card` | 1.9% | 20 cents |
| `klarna` | 2.5% | 40 cents |

All other provider/country combinations continue to use the standard Part 1 fee table. In particular, `bank_transfer` remains at 0.8% with no fixed fee in Part 2.

### Example — Part 2

**Input:**

```text
id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status
py_1,1,1000,eur,2024-12-24,acct_1,ie,payment,card,payment_completed
py_2,2,2500,eur,2024-12-24,acct_2,de,payment,card,payment_failed
py_3,3,3400,eur,2024-12-25,acct_2,ie,payment,klarna,payment_completed
py_4,4,5000,eur,2024-12-25,acct_1,fr,payment,bank_transfer,payment_completed
py_5,5,2000,eur,2024-12-26,acct_1,ie,payment,card,payment_pending
```

**Output (CSV):**

```text
id,transaction_type,payment_provider,fee
py_1,payment,card,39
py_2,payment,card,0
py_3,payment,klarna,125
py_4,payment,bank_transfer,40
py_5,payment,card,0
```

**FastPrep function result:**

```text
[
  "id,transaction_type,payment_provider,fee",
  "py_1,payment,card,39",
  "py_2,payment,card,0",
  "py_3,payment,klarna,125",
  "py_4,payment,bank_transfer,40",
  "py_5,payment,card,0"
]
```

**Explanation:**

- `py_1`: Completed Ireland card payment; 1000 × 0.019 + 20 = 39.
- `py_2`: Failed payment; fee is 0.
- `py_3`: Completed Ireland Klarna payment; 3400 × 0.025 + 40 = 125.
- `py_4`: Completed France bank transfer; standard 5000 × 0.008 = 40.
- `py_5`: Pending payment; fee is 0.

### Requirements

1. Check `status` before calculating a fee.
2. Use zero fees for unsuccessful payments.
3. Apply Ireland-specific rates for `card` and `klarna`.
4. Use standard Part 1 rates otherwise.
5. Keep status checks and fee calculations conceptually separate.
6. Round final fees down and preserve CSV output ordering.

### Function Signature — Parts 1–2

```text
calculateFees(csvData: String) → String[]
```

---

## Part 3 — Volume-Based Discounts

### Task

Extend the transaction fee calculator to award volume discounts to merchants who process many successful payments.

The calculator must maintain a **separate successful-transaction count per merchant** while processing CSV records **in input order**. A discount applies according to the number of successful transactions for that merchant, including the current completed payment.

### Discount Table

| Successful Transaction Number | Discount | Fee Multiplier |
|---|---:|---:|
| 1–10 | 0% off | 1.00 |
| 11–50 | 10% off | 0.90 |
| 51–100 | 15% off | 0.85 |
| 101+ | 20% off | 0.80 |

Only transactions with status `payment_completed` increase the merchant's count. Failed and pending payments have fee 0 and do not increase the count.

### Country Fee Configuration — Original Source Representation

The original interview wording describes a nested dictionary of configurable fee rates:

```python
country_fees = {
    "ie": {
        "card": (0.019, 20),
        "klarna": (0.025, 40),
        "bank_transfer": (0.006, 0)
    },
    "de": {
        "card": (0.025, 25),
        "klarna": (0.030, 45),
        "bank_transfer": (0.007, 0)
    },
    "fr": {
        "card": (0.027, 28),
        "klarna": (0.032, 48),
        "bank_transfer": (0.008, 0)
    },
    "default": {
        "card": (0.029, 30),
        "klarna": (0.035, 50),
        "bank_transfer": (0.008, 0)
    }
}
```

Each tuple contains `(decimal_percentage_rate, fixed_fee_in_cents)`.

If `buyer_country` is not configured, use the `default` rate for that payment provider.

**Important:** Part 3's configuration supersedes Part 2's hardcoded region rules. For example, the Irish bank-transfer rate in this Part 3 configuration is 0.6%, whereas Part 2 used the standard 0.8% rate.

### FastPrep Fee Configuration Adapter

For the judged cross-language function, `countryFees` is **not** supplied as a nested dictionary. It is a `String[][]` whose rows have the form:

```text
[country, provider, rateBasisPoints, fixedFee]
```

Examples:

```text
["ie", "card", "190", "20"]
["ie", "klarna", "250", "40"]
["default", "card", "290", "30"]
```

The percentage is expressed in **basis points**, not a decimal:

- 190 basis points = 1.9% = 0.019.
- 250 basis points = 2.5% = 0.025.
- 290 basis points = 2.9% = 0.029.
- 80 basis points = 0.8% = 0.008.

**Conversion:** `decimal rate = rateBasisPoints / 10000`.

### Fee and Discount Rules

1. Look up the applicable fee configuration by buyer country and payment provider, using `default` when needed.
2. Calculate the base fee using the configured percentage and fixed amount.
3. Select the discount according to the merchant's successful-transaction number **including the current payment**.
4. Apply the discount to the unrounded base fee.
5. Round the discounted final fee **down** to an integer.
6. Produce output in the same CSV order as the transactions.

### Worked Example — Eleventh Payment

Imagine merchant `acct_1` has already completed ten transactions. Their next completed payment is an Ireland card transaction of 1500 cents.

- Base fee: 1500 × 0.019 + 20 = 48.5 cents.
- The eleventh successful transaction qualifies for 10% off.
- Discounted fee: 48.5 × 0.9 = 43.65 cents.
- Round down: **43 cents**.

The twelfth successful transaction also receives a 10% discount, assuming the merchant remains within the 11–50 tier.

---

## Part 3 — Examples

### Example 1 — Mixed Countries and Payment Statuses

**Input:**

```text
csvData = "id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status\npy_1,1,1000,eur,2024-12-24,acct_1,ie,payment,card,payment_completed\npy_2,2,2500,eur,2024-12-24,acct_2,de,payment,card,payment_failed\npy_3,3,3400,eur,2024-12-25,acct_2,ie,payment,klarna,payment_completed\npy_4,4,5000,eur,2024-12-25,acct_1,fr,payment,bank_transfer,payment_completed\npy_5,5,2000,eur,2024-12-26,acct_1,ie,payment,card,payment_pending"
```

```python
countryFees = [
    ["ie", "card", "190", "20"],
    ["ie", "klarna", "250", "40"],
    ["ie", "bank_transfer", "60", "0"],
    ["de", "card", "250", "25"],
    ["de", "klarna", "300", "45"],
    ["de", "bank_transfer", "70", "0"],
    ["fr", "card", "270", "28"],
    ["fr", "klarna", "320", "48"],
    ["fr", "bank_transfer", "80", "0"],
    ["default", "card", "290", "30"],
    ["default", "klarna", "350", "50"],
    ["default", "bank_transfer", "80", "0"]
]
```

**Expected Output:**

```text
[
  "id,transaction_type,payment_provider,fee",
  "py_1,payment,card,39",
  "py_2,payment,card,0",
  "py_3,payment,klarna,125",
  "py_4,payment,bank_transfer,40",
  "py_5,payment,card,0"
]
```

**Explanation:** Failed and pending transactions have zero fees and do not affect merchant volume. No merchant reaches their eleventh completed payment, so no volume discounts apply.

### Example 2 — The Eleventh Successful Transaction

**Input:**

```text
csvData = "id,reference,amount,currency,date,merchant_id,buyer_country,transaction_type,payment_provider,status\nt1,1,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt2,2,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt3,3,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt4,4,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt5,5,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt6,6,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt7,7,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt8,8,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt9,9,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt10,10,1000,usd,2025-01-01,m1,us,payment,card,payment_completed\nt11,11,1000,usd,2025-01-01,m1,ie,payment,card,payment_completed"
```

```python
countryFees = [
    ["ie", "card", "190", "20"],
    ["default", "card", "290", "30"],
    ["default", "klarna", "350", "50"],
    ["default", "bank_transfer", "80", "0"]
]
```

**Expected Output:**

```text
[
  "id,transaction_type,payment_provider,fee",
  "t1,payment,card,59",
  "t2,payment,card,59",
  "t3,payment,card,59",
  "t4,payment,card,59",
  "t5,payment,card,59",
  "t6,payment,card,59",
  "t7,payment,card,59",
  "t8,payment,card,59",
  "t9,payment,card,59",
  "t10,payment,card,59",
  "t11,payment,card,35"
]
```

**Explanation:**

- Payments `t1` through `t10` each have the default card base fee of 1000 × 0.029 + 30 = 59, with no discount.
- Payment `t11` is the merchant's eleventh completed transaction.
- It is an Ireland card payment, so its base fee is 1000 × 0.019 + 20 = 39.
- The 10% volume discount gives 39 × 0.9 = 35.1, rounded down to **35**.

---

## Function Signature — Part 3

```text
calculateDiscountedFees(csvData: String, countryFees: String[][]) → String[]
```

### Inputs

- `csvData`: A CSV-formatted transaction string, including the ten-column header.
- `countryFees`: A list of fee-configuration rows, where each row contains `[country, provider, rateBasisPoints, fixedFee]` as strings.

### Output

An array of CSV lines. The first element is the required output header; each later element is the result for one input transaction.

---

## Constraints — Parts 1–2

1. CSV transactions use the ten-column schema shown above.
2. For Part 1, provider rates are those in the standard fee table.
3. For Part 2, a fee is charged only if `status` equals `payment_completed`.
4. For Part 2, Ireland-specific rates apply to `card` and `klarna`; other combinations retain standard Part 1 rates.
5. Round final fees down using integer conversion.
6. In the FastPrep adapter, return the newline-delimited CSV result as `String[]`, with one CSV line per element.

## Constraints — Part 3

1. Process transactions in CSV input order.
2. Only `payment_completed` transactions increase a merchant's successful-transaction count.
3. Use the merchant's transaction number **including the current successful payment** to select the discount tier.
4. Apply the discount **before** rounding down.
5. If the buyer country is absent from the fee configuration, use `default`.
6. `countryFees` is a `String[][]` of `[country, provider, rateBasisPoints, fixedFee]` rows.
7. Basis-point rates represent decimal rates divided by 10,000 (e.g., 190 → 0.019).
8. Return `String[]` with the CSV header and one result row for each transaction.
