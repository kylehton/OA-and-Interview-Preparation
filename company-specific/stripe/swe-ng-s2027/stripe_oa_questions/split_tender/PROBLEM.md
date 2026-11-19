
# Split Tender — Parts 1–4

**Company:** Stripe  
**Difficulty:** Medium (Parts 1–2), Hard (Parts 3–4)  
**Roles:** Full-Time, New Grad, Intern  
**Interview Stages:** Online Assessment; Phone Screen (Part 4 also tagged)  
**Status:** Solved  
**Topics:** Event Processing, State Management, Gift Cards, Expiration, Regional Surcharges, Refunds

---

## Problem Statement

Many Stripe merchants use Stripe Terminal to accept in-person payments at the point of sale.

In physical retail, customers may pay for a single purchase using multiple payment methods.

For example, a customer might cover a $100 purchase using:

- $40 from a gift card
- $60 from a credit card

This is called a **split-tender transaction**.

Build a system that processes a chronological stream of payment events and calculates the correct credit card charge for each transaction.

The system must use available gift card balances before charging the remainder to the credit card.

The problem consists of four progressively more complex parts:

1. **Part 1 — Basic Split Tendering:** Process gift card additions and charges.
2. **Part 2 — Expiration Dates:** Support multiple gift cards, expiration dates, and spending priorities.
3. **Part 3 — Surcharges:** Apply regional surcharges to the credit card portion.
4. **Part 4 — Refunds:** Refund historical transactions to credit cards and store credit.

Each part extends the functionality of the previous parts.

---

# Shared Input Format

The system processes an array of event strings.

Each event follows one of three schemas.

## 1. ADD_GIFTCARD

```text
timestamp,ADD_GIFTCARD,customer_id,card_id,amount,valid_before
```

| Field | Description |
|---|---|
| `timestamp` | Time when the gift card is added |
| `ADD_GIFTCARD` | Event type |
| `customer_id` | Customer receiving the gift card |
| `card_id` | Unique gift card identifier |
| `amount` | Gift card value in cents |
| `valid_before` | Expiration timestamp |

## 2. CHARGE

```text
timestamp,CHARGE,charge_id,customer_id,amount,zip_code
```

| Field | Description |
|---|---|
| `timestamp` | Time when the charge occurs |
| `CHARGE` | Event type |
| `charge_id` | Unique charge identifier |
| `customer_id` | Customer making the payment |
| `amount` | Original purchase amount in cents |
| `zip_code` | Five-digit ZIP code |

## 3. REFUND

```text
timestamp,REFUND,charge_id,refund_amount
```

| Field | Description |
|---|---|
| `timestamp` | Time when the refund occurs |
| `REFUND` | Event type |
| `charge_id` | Identifier of the original charge |
| `refund_amount` | Total amount to refund, in cents |

The REFUND event type is introduced in Part 4.

---

# Shared Surcharge Configuration

Regional surcharge rules are represented as strings:

```text
start_zip-end_zip:rate
```

For example:

```text
90000-99999:0.05
```

This indicates:

- Starting ZIP: `90000`
- Ending ZIP: `99999`
- Surcharge rate: `0.05`, or 5%

Both ZIP endpoints are inclusive.

The surcharge ranges do not overlap.

Surcharge configuration is introduced in Part 3.

---

# Shared Rules and Assumptions

1. Events are provided in chronological order.
2. All event lines are well-formed.
3. Every CHARGE event has a unique `charge_id`.
4. Every REFUND event references a previous CHARGE event.
5. Each charge receives at most one REFUND event.
6. Every ADD_GIFTCARD event has a unique `card_id`.
7. Surcharge ranges are valid and non-overlapping.
8. ZIP codes contain exactly five numeric digits.
9. Monetary amounts are represented using non-negative integer cents.
10. Surcharge rates are decimal fractions.
11. Every surcharge calculation produces a whole number, so no rounding is required.

### Monetary Representation

```text
$40.00 = 4000 cents
$60.00 = 6000 cents
$100.00 = 10000 cents
```

All calculations use cents rather than dollar amounts.

---

# Part 1 — Basic Split Tendering

## Task

Implement basic gift card additions and payment charges.

For Part 1, process only:

- `ADD_GIFTCARD`
- `CHARGE`

All customers begin with a gift card balance of zero.

Each customer holds at most one active gift card at a time.

Gift card expiration and ZIP codes are ignored in this part.

## ADD_GIFTCARD Rules

When receiving:

```text
timestamp,ADD_GIFTCARD,customer_id,card_id,amount,valid_before
```

Add the specified amount to the customer's available gift card balance.

Return an empty string:

```text
""
```

## CHARGE Rules

When receiving:

```text
timestamp,CHARGE,charge_id,customer_id,amount,zip_code
```

Attempt to pay for the purchase using the customer's gift card balance first.

### Case 1 — Gift Card Covers the Entire Charge

If the available gift card balance is greater than or equal to the purchase amount:

- Deduct the purchase amount from the gift card.
- Charge zero to the credit card.

### Case 2 — Insufficient Gift Card Balance

If the purchase amount exceeds the available gift card balance:

- Consume the entire available gift card balance.
- Reduce the gift card balance to zero.
- Charge the remaining unpaid amount to the credit card.

### Case 3 — No Available Gift Card

If the customer has no available gift card balance:

- Charge the entire purchase amount to the credit card.

## Output Format

For ADD_GIFTCARD:

```text
""
```

For CHARGE:

```text
CC_CHARGE_AMOUNT,GIFT_CARD_ID:AMOUNT_USED
```

If multiple gift cards are used in later parts:

```text
CC_CHARGE_AMOUNT,GIFT_CARD_ID_1:AMOUNT_USED,GIFT_CARD_ID_2:AMOUNT_USED
```

If no gift card is debited, output only the credit card amount.

For example:

```text
1250
```

The returned array must contain exactly one string for every input event.

---

## Part 1 Function Signature

```text
processEvents(events: String[]) → String[]
```

### Input

`events`: An array of chronological ADD_GIFTCARD and CHARGE event strings.

### Output

A `String[]` containing one result for every event.

---

## Part 1 Examples

### Example 1 — Multiple Customers

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,ADD_GIFTCARD,cust2,gc2,2000,15",
    "3,CHARGE,chg1,cust2,3000,10000",
    "4,CHARGE,chg2,cust1,3000,10000"
]
```

**Expected Output:**

```python
[
    "",
    "",
    "1000,gc2:2000",
    "0,gc1:3000"
]
```

**Explanation:**

1. Customer `cust1` receives gift card `gc1` with 5000 cents.
2. Customer `cust2` receives gift card `gc2` with 2000 cents.
3. `cust2` makes a 3000-cent purchase:
   - Gift card covers 2000 cents.
   - Credit card covers 1000 cents.
4. `cust1` makes a 3000-cent purchase:
   - Gift card covers all 3000 cents.
   - Credit card charge is zero.

### Example 2 — No Available Gift Card

**Input:**

```python
events = [
    "1,CHARGE,c1,alice,1250,94105"
]
```

**Expected Output:**

```python
["1250"]
```

**Explanation:**

Alice has no available gift card balance.

The entire 1250-cent purchase is charged to her credit card.

### Example 3 — Multiple Charges on One Gift Card

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,alice,g1,2550,50",
    "2,CHARGE,c1,alice,1025,10000",
    "3,CHARGE,c2,alice,2000,10000"
]
```

**Expected Output:**

```python
[
    "",
    "0,g1:1025",
    "475,g1:1525"
]
```

**Explanation:**

1. Alice receives a gift card containing 2550 cents.
2. The first purchase consumes 1025 cents.
3. The gift card has 1525 cents remaining.
4. The second purchase consumes the remaining 1525 cents.
5. The credit card covers the final 475 cents.

---

# Part 2 — Expiration Dates

## Task

Extend Part 1 to support:

- Multiple gift cards per customer.
- Individual gift card balances.
- Gift card expiration dates.
- Earliest-expiration-first spending.
- Deterministic ordering of gift card debits.

All Part 1 rules continue to apply.

The single-active-gift-card restriction no longer applies.

## Gift Card Expiration

Each gift card has a `valid_before` timestamp.

When processing a CHARGE event at time `T`, a gift card is valid only when:

```text
T < valid_before
```

If:

```text
T >= valid_before
```

the gift card is expired.

An expired gift card:

- Cannot be used to pay for a charge.
- Has its remaining balance permanently voided.
- Cannot become valid again.

Expiration is exclusive: a card cannot be used at its exact `valid_before` timestamp.

## Gift Card Spending Priority

When multiple gift cards are available, use them according to these rules:

1. Use valid gift cards with the earliest expiration date first.
2. Completely drain one gift card before moving to the next.
3. If two gift cards have the same expiration timestamp, prioritize the lexicographically smaller `card_id`.
4. Gift cards without expiration dates are valid forever.
5. Non-expiring gift cards are used after all valid cards with finite expiration timestamps.

Refund-created non-expiring cards are introduced in Part 4.

For this practice version of Part 2, supplied gift cards have finite expiration timestamps.

## Output Ordering

Gift cards are consumed according to expiration priority.

However, their output entries must be ordered differently.

**Output rule:**

Sort positive gift card debit entries lexicographically by `card_id`, regardless of the order in which gift cards were consumed.

For example, a card named `z` may be consumed before a card named `a`, but the output must list `a` first.

Only positive debit amounts appear in the output.

## Output Format

The CHARGE output remains:

```text
CC_CHARGE_AMOUNT,CARD_ID_1:AMOUNT_USED,CARD_ID_2:AMOUNT_USED
```

ADD_GIFTCARD still returns:

```text
""
```

---

## Part 2 Function Signature

```text
processEvents(events: String[]) → String[]
```

### Input

An array of chronological ADD_GIFTCARD and CHARGE events.

### Output

A `String[]` containing one result per event, incorporating expiration and gift card priority.

---

## Part 2 Examples

### Example 1 — Expiration Priority

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,ADD_GIFTCARD,cust1,gc2,4000,5",
    "3,CHARGE,chg1,cust1,6000,10000",
    "11,CHARGE,chg2,cust1,1000,10000"
]
```

**Expected Output:**

```python
[
    "",
    "",
    "0,gc1:2000,gc2:4000",
    "1000"
]
```

**Explanation:**

1. `gc1` contains 5000 cents and expires at timestamp 10.
2. `gc2` contains 4000 cents and expires at timestamp 5.
3. At timestamp 3, `gc2` expires sooner and is therefore consumed first.
4. `gc2` covers 4000 cents.
5. `gc1` covers the remaining 2000 cents.
6. The credit card charge is zero.
7. Output gift card entries are sorted lexicographically by card ID.
8. At timestamp 11, the remaining `gc1` balance has expired.
9. The final 1000-cent charge goes entirely to the credit card.

### Example 2 — Spending Order vs. Output Order

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,alice,z,400,5",
    "2,ADD_GIFTCARD,alice,a,500,10",
    "3,CHARGE,c1,alice,600,10000",
    "5,CHARGE,c2,alice,400,10000"
]
```

**Expected Output:**

```python
[
    "",
    "",
    "0,a:200,z:400",
    "100,a:300"
]
```

**Explanation:**

1. Gift card `z` expires first and is consumed first.
2. `z` covers 400 cents.
3. Gift card `a` covers the remaining 200 cents.
4. The output lists `a` before `z` because output entries are sorted by card ID.
5. At timestamp 5, gift card `z` is expired.
6. The remaining 300 cents in `a` are consumed.
7. The credit card covers the final 100 cents.

---

# Part 3 — Regional Credit Card Surcharges

## Task

Extend Parts 1–2 by applying regional processing surcharges to the credit card portion of a transaction.

The system now receives an additional parameter:

```text
surchargeRates
```

Each surcharge rule specifies a ZIP code range and a surcharge percentage.

All previous split-tender and expiration rules remain in effect.

Refunds are not processed in this part.

## Surcharge Rules

When processing a CHARGE event:

1. Apply gift card balances to the original purchase amount.
2. Determine the remaining credit card portion.
3. Find the surcharge rate associated with the event's ZIP code.
4. Apply the surcharge only to the remaining credit card portion.
5. Add the surcharge to the credit card portion.
6. Return the final credit card charge along with the gift card debit entries.

Gift card deductions are never subject to surcharges.

### ZIP Code Matching

Each surcharge rule has the format:

```text
start_zip-end_zip:rate
```

Both endpoints are inclusive.

For example:

```text
90000-99999:0.05
```

A transaction with ZIP code `90210` falls within this range.

If a ZIP code does not match any surcharge range, the surcharge rate is zero.

Ranges are guaranteed not to overlap.

## Surcharge Calculation

The surcharge is calculated as:

```text
surcharge = credit_card_portion × rate
```

The final credit card charge is:

```text
final_cc_charge = credit_card_portion + surcharge
```

### Example

A purchase leaves 10000 cents to be paid by credit card.

The applicable surcharge rate is 5%.

```text
Credit card principal: 10000
Surcharge: 10000 × 0.05 = 500
Final credit card charge: 10500
```

If the entire purchase is covered by gift cards, the credit card portion is zero and no surcharge is charged.

The problem guarantees surcharge calculations produce whole-number cents.

## Output Format

The CHARGE output remains:

```text
CC_CHARGE_AMOUNT,CARD_ID_1:AMOUNT_USED,CARD_ID_2:AMOUNT_USED
```

However, `CC_CHARGE_AMOUNT` now includes the applicable surcharge.

The gift card entries continue to be ordered lexicographically by card ID.

---

## Part 3 Function Signature

```text
processEvents(
    events: String[],
    surchargeRates: String[]
) → String[]
```

### Input

**`events`**

An array of chronological ADD_GIFTCARD and CHARGE events.

**`surchargeRates`**

An array of non-overlapping ZIP code ranges and surcharge percentages.

### Output

A `String[]` containing one result per event.

CHARGE results include the surcharge-adjusted credit card amount.

---

## Part 3 Examples

### Example 1 — Partial Gift Card Payment with Surcharge

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,CHARGE,chg1,cust1,15000,90210"
]

surchargeRates = [
    "80000-89999:0.02",
    "90000-99999:0.05"
]
```

**Expected Output:**

```python
[
    "",
    "10500,gc1:5000"
]
```

**Explanation:**

1. The original purchase amount is 15000 cents.
2. Gift card `gc1` covers 5000 cents.
3. The remaining credit card portion is 10000 cents.
4. ZIP code `90210` matches the 5% surcharge range.
5. The surcharge is 500 cents.
6. The final credit card charge is 10500 cents.

### Example 2 — Fully Covered Charge and Expiration

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,alice,g1,1000,3",
    "2,CHARGE,c1,alice,500,90210",
    "3,CHARGE,c2,alice,1000,90210"
]

surchargeRates = [
    "90000-99999:0.05"
]
```

**Expected Output:**

```python
[
    "",
    "0,g1:500",
    "1050"
]
```

**Explanation:**

1. Alice receives a gift card containing 1000 cents.
2. At timestamp 2, the gift card covers the first 500-cent charge entirely.
3. No credit card portion exists, so no surcharge applies.
4. At timestamp 3, the gift card has expired.
5. The entire second purchase goes to the credit card.
6. The 5% surcharge adds 50 cents.
7. The final credit card charge is 1050 cents.

---

# Part 4 — Refunds

## Task

Extend Parts 1–3 to support refunds of previously processed charges.

The system now processes three event types:

- `ADD_GIFTCARD`
- `CHARGE`
- `REFUND`

All previous gift card, expiration, prioritization, and surcharge rules remain in effect.

Refunds reference historical charges using their `charge_id`.

## REFUND Event Format

```text
timestamp,REFUND,charge_id,refund_amount
```

### Requirements

- Every refund references a previous CHARGE event.
- Each charge receives at most one refund.
- `refund_amount` includes any refundable credit card surcharge.
- The refund amount does not exceed the original total amount paid, including surcharge.
- Refunds must be routed back to the customer in the specified priority order.

## Refund Priority

Refunds are distributed in two stages.

### Stage 1 — Credit Card Refund

Refund actual money to the credit card first.

The credit card refund cannot exceed the amount originally charged to the credit card for the referenced transaction, including surcharge.

If the entire refund can be returned to the credit card, no store credit is created.

### Stage 2 — Store Credit Refund

If the refund amount exceeds the credit card amount refundable for the referenced charge, return the remaining amount as store credit.

Store credit is represented by a newly created gift card.

The gift card must:

- Belong to the customer who made the original charge.
- Have the card ID `REFUND_{charge_id}`.
- Have no expiration date.
- Contain the remaining refunded amount after the credit card refund.

For example:

```text
Original charge ID: chg1
New store credit gift card ID: REFUND_chg1
```

## Refund-Created Gift Card Rules

Refund-created gift cards behave like ordinary gift cards during future CHARGE events, with one exception: they never expire.

When selecting gift cards for future payments:

1. Use valid finite-expiration gift cards first.
2. Follow earliest-expiration-first ordering.
3. Break equal-expiration ties lexicographically by card ID.
4. Use non-expiring refund gift cards after all valid finite-expiration cards.

Refund-created gift cards may be partially or fully consumed by future charges.

User-supplied gift card IDs cannot begin with `REFUND_`.

## REFUND Output Format

Return a string containing:

```text
CC_REFUND,GC_REFUND
```

Where:

- `CC_REFUND` is the amount returned to the credit card.
- `GC_REFUND` is the amount returned as newly created store credit.

The two amounts are separated by one comma.

Examples:

```text
10500,1500
```

```text
3000,0
```

```text
0,2000
```

ADD_GIFTCARD events continue to return empty strings.

CHARGE events continue to use the previous output format, including surcharges and sorted gift card debits.

---

## Part 4 Function Signature

```text
processEvents(
    events: String[],
    surchargeRates: String[]
) → String[]
```

### Input

**`events`**

An array of chronological ADD_GIFTCARD, CHARGE, and REFUND events.

**`surchargeRates`**

An array of non-overlapping regional surcharge configurations.

### Output

A `String[]` containing exactly one result for every input event.

- ADD_GIFTCARD → empty string.
- CHARGE → surcharge-inclusive credit card charge and gift card debits.
- REFUND → credit card refund and store credit refund.

---

## Part 4 Examples

### Example 1 — Basic Split Tendering

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,ADD_GIFTCARD,cust2,gc2,2000,15",
    "3,CHARGE,chg1,cust2,3000,10000",
    "4,CHARGE,chg2,cust1,3000,10000"
]

surchargeRates = []
```

**Expected Output:**

```python
[
    "",
    "",
    "1000,gc2:2000",
    "0,gc1:3000"
]
```

**Explanation:**

The first purchase drains `gc2` and charges the remaining 1000 cents to the credit card.

The second purchase consumes 3000 cents from `gc1`.

### Example 2 — Expiration and Multiple Gift Cards

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,ADD_GIFTCARD,cust1,gc2,4000,5",
    "3,CHARGE,chg1,cust1,6000,10000",
    "11,CHARGE,chg2,cust1,1000,10000"
]

surchargeRates = []
```

**Expected Output:**

```python
[
    "",
    "",
    "0,gc1:2000,gc2:4000",
    "1000"
]
```

**Explanation:**

`gc2` expires sooner and is consumed first.

The output lists gift card debits lexicographically.

At timestamp 11, the remaining `gc1` balance has expired.

### Example 3 — Regional Surcharge

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,CHARGE,chg1,cust1,15000,90210"
]

surchargeRates = [
    "80000-89999:0.02",
    "90000-99999:0.05"
]
```

**Expected Output:**

```python
[
    "",
    "10500,gc1:5000"
]
```

**Explanation:**

1. The gift card covers 5000 cents.
2. The remaining credit card principal is 10000 cents.
3. The 5% surcharge adds 500 cents.
4. The final credit card charge is 10500 cents.

### Example 4 — Refund to Credit Card and Store Credit

**Input:**

```python
events = [
    "1,ADD_GIFTCARD,cust1,gc1,5000,10",
    "2,CHARGE,chg1,cust1,15000,90210",
    "3,REFUND,chg1,12000"
]

surchargeRates = [
    "90000-99999:0.05"
]
```

**Expected Output:**

```python
[
    "",
    "10500,gc1:5000",
    "10500,1500"
]
```

**Explanation:**

**Original charge:**

- Purchase amount: 15000 cents.
- Gift card payment: 5000 cents.
- Credit card principal: 10000 cents.
- Credit card surcharge: 500 cents.
- Final credit card charge: 10500 cents.

**Refund:**

- Requested refund: 12000 cents.
- Credit card refund: 10500 cents.
- Remaining refund: 1500 cents.

The remaining 1500 cents are returned as store credit.

A new non-expiring gift card is created:

```text
REFUND_chg1
```

The new gift card belongs to `cust1`.

It can be used toward future charges after all valid finite-expiration gift cards.

---

# Consolidated Constraints

The following constraints apply to the combined exercise, with part-specific restrictions noted.

## Event Constraints

1. `1 <= events.length <= 100000`.
2. Events are processed in chronological timestamp order.
3. Events with equal timestamps are processed in input order.
4. Every event is well-formed.
5. Every CHARGE event has a unique `charge_id`.
6. Every REFUND references an earlier CHARGE.
7. Each charge ID receives at most one REFUND.
8. Every user-supplied gift card ID is unique.
9. The input describes valid payment events.

## Identifier Constraints

1. Customer IDs, card IDs, and charge IDs contain ASCII letters, digits, or underscores.
2. Identifier lengths range from 1 to 64 characters.
3. Identifiers contain no commas.
4. User-supplied gift card IDs cannot begin with `REFUND_` in Part 4.

## Monetary Constraints

1. All monetary amounts are non-negative integer cents.
2. Every input amount is at most `10^9` cents.
3. Running balances and intermediate money calculations fit signed 64-bit integers.
4. Surcharge calculations produce whole-number amounts.
5. No surcharge rounding is required.

## Gift Card Constraints

1. Part 1 permits at most one active gift card per customer.
2. Parts 2–4 permit multiple gift cards per customer.
3. In Part 1, a gift card is active while it has a positive balance.
4. In Part 1, a zero-value gift card addition does not replace an existing active card.
5. Gift cards with finite expiration timestamps are valid only before `valid_before`.
6. Finite timestamps and expirations are integers from 0 to `10^9`.
7. Expired gift card balances are permanently voided.
8. Earlier-expiring cards are consumed first.
9. Equal-expiration cards are prioritized lexicographically by card ID.
10. Non-expiring cards are consumed after finite-expiration cards.
11. Gift card debit entries in the output are sorted lexicographically by card ID.
12. Only positive gift card debit amounts are listed.
13. Supplied gift cards have finite expiration timestamps in Parts 2–4.
14. Non-expiring refund-created gift cards are introduced in Part 4.

## Surcharge Constraints

1. At most `10^4` surcharge ranges are provided.
2. All surcharge ranges are valid.
3. Surcharge ranges do not overlap.
4. ZIP codes contain exactly five numeric digits.
5. ZIP range endpoints are inclusive.
6. Surcharge rates are between 0 and 1.
7. Rates contain at most six fractional digits.
8. ZIP codes outside all supplied ranges have a zero surcharge.
9. Surcharges apply only to the credit card portion.
10. Gift card deductions are never subject to surcharges.

## Refund Constraints

1. Refunds reference historical charges.
2. Each charge can receive at most one refund.
3. Refund amounts cannot exceed the original total paid, including surcharge.
4. Credit card refunds have priority over store credit.
5. Credit card refunds are capped at the original credit card charge, including surcharge.
6. Remaining refund amounts are returned through new store credit gift cards.
7. Refund-created gift cards are named `REFUND_{charge_id}`.
8. Refund-created gift cards never expire.
9. Refund-created gift cards participate in subsequent payments.

## Output Constraints

1. Return a `String[]`.
2. Return exactly one string per input event.
3. Preserve input event order.
4. ADD_GIFTCARD returns `""`.
5. CHARGE returns the credit card total followed by positive gift card debit entries.
6. Gift card debit entries are sorted lexicographically by card ID.
7. REFUND returns `CC_REFUND,GC_REFUND`.
8. The final credit card amount for CHARGE includes any applicable surcharge.

---
