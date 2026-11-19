# Shipping Cost Calculator — Parts 1–3

**Company:** Stripe  
**Difficulty:** Medium  
**Roles:** Intern, Full-Time, New Grad  
**Interview Stage:** Phone Screen  
**Topics:** CSV Parsing, Hash Maps, Sorting, Tiered Pricing, Greedy Allocation

---

## Problem Overview

Calculate shipping costs for products shipped to a destination country. The problem evolves through three stages:

1. **Part 1 — Basic Per-Unit Shipping:** Calculate shipping costs using a single rate per product and country.
2. **Part 2 — Volume-Tiered Pricing:** Products have multiple quantity tiers, each charging a different per-unit rate.
3. **Part 3 — Mixed Fixed/Incremental Tiers:** Each tier charges either once for the batch (`fixed`) or per unit (`incremental`).

> **Source fidelity note:** The full original Part 1 prompt, exact function signature, examples, and constraints were not supplied in this conversation. The Part 1 section below is a **high-level reconstruction** of the prerequisite basic shipping calculation, not a verbatim FastPrep problem. Parts 2 and 3 are transcribed from the supplied practice descriptions.

---

## Part 1 — Basic Shipping Cost Calculator (Reconstructed Overview)

### Goal

Given a destination country, requested products with quantities, and country/product shipping rates, calculate the total shipping cost.

Under the basic per-unit model, each requested product has one applicable shipping rate for the selected country.

For each item, its charge is:

`quantity × per-unit shipping cost`

Return the sum of all applicable item charges.

### Progression to Part 2

Part 2 replaces the single per-product rate with multiple quantity tiers. Its rule schema and exact examples are documented below.

> **Not specified in the supplied Part 1 source:** Its precise input record formats, output signature, sample cases, and invalid-input policy. Do not assume this reconstruction is the exact judged Part 1 contract.

---

## Part 2 — Volume-Tiered Pricing

### Problem Statement

This continues the shipping cost calculator. Now each product's per-unit cost varies by quantity using **tiered (volume-discount) pricing**.

### Inputs

- **`country`** — Destination country code.
- **`items`** — `String[]` of `"product,quantity"`.
- **`rules`** — `String[]` of `"country,product,minQuantity,maxQuantity,cost"`.

A `maxQuantity` of `*` means the tier has no upper limit.

### Pricing Rules

For each item, walk that product's tiers in ascending order of `minQuantity`.

- Each tier has a **half-open range** `[minQuantity, maxQuantity)`.
- A bounded tier's capacity is `maxQuantity - minQuantity`.
- An unbounded tier (`*`) has no capacity limit.
- Assign as many remaining units as fit in the current tier: `min(remaining units, tier capacity)`.
- Charge `units assigned × cost` for that tier.
- Continue until all units are priced.
- Sum charges across all items and return the total integer cost.

**Important:** Tiers allocate units sequentially by their *capacities*. In the supplied examples, `[0,2)` and `[3,*)` are used together: the first takes 2 units and the second takes the remaining 3, despite the gap in the numerical endpoints.

### Function Signature

```text
calculateTieredShippingCost(country: String, items: String[], rules: String[]) → int
```

### Example 1 — United States

**Input:**

```python
country = "US"
items = ["mouse,20", "laptop,5"]
rules = [
    "US,mouse,0,*,550",
    "US,laptop,0,2,1000",
    "US,laptop,3,*,900",
    "CA,mouse,0,*,750",
    "CA,laptop,0,2,1100",
    "CA,laptop,3,*,1000"
]
```

**Expected Output:**

```text
15700
```

**Explanation:**

- US mouse: 20 × 550 = 11,000 (single unbounded tier).
- US laptop: first 2 units × 1,000 = 2,000; remaining 3 units × 900 = 2,700.
- Laptop subtotal = 4,700.
- **Total = 11,000 + 4,700 = 15,700.**

### Example 2 — Canada

**Input:**

```python
country = "CA"
items = ["mouse,20", "laptop,5"]
rules = [
    "US,mouse,0,*,550",
    "US,laptop,0,2,1000",
    "US,laptop,3,*,900",
    "CA,mouse,0,*,750",
    "CA,laptop,0,2,1100",
    "CA,laptop,3,*,1000"
]
```

**Expected Output:**

```text
20200
```

**Explanation:**

- CA mouse: 20 × 750 = 15,000.
- CA laptop: first 2 units × 1,100 = 2,200; remaining 3 units × 1,000 = 3,000.
- Laptop subtotal = 5,200.
- **Total = 15,000 + 5,200 = 20,200.**

### Constraints — Part 2

1. Each rule is `country,product,minQuantity,maxQuantity,cost`.
2. `maxQuantity = *` means the tier is unbounded.
3. Process a product's tiers from lowest to highest `minQuantity`.
4. Ranges are half-open: `[minQuantity, maxQuantity)`.
5. Bounded tier capacity is `maxQuantity - minQuantity`.
6. Each tier prices `min(remaining units, tier capacity) × cost`.
7. Return the integer total shipping cost across all items.

---

## Part 3 — Mixed Fixed/Incremental Tiers

### Problem Statement

This continues the shipping cost calculator. A product's tiers can charge in one of two ways:

- **`incremental`** — Charge per unit: `units_in_tier × cost` (same as Part 2).
- **`fixed`** — Charge a **single flat cost for the entire tier**, regardless of how many units enter it, provided **at least one** unit enters.

A single product can use both types across different tiers.

### Inputs

- **`country`** — Destination country code.
- **`items`** — `String[]` of `"product,quantity"`.
- **`rules`** — `String[]` of `"country,product,type,minQuantity,maxQuantity,cost"`.
- **`type`** — Either `fixed` or `incremental`.
- **`maxQuantity`** — An integer upper bound or `*` (unbounded).

### Pricing Rules

For each requested item:

1. Process its applicable tiers in ascending order.
2. Treat each tier as half-open `[minQuantity, maxQuantity)` with capacity `maxQuantity - minQuantity` (unbounded for `*`).
3. Assign `min(remaining units, tier capacity)` units to that tier.
4. If at least one unit enters the tier:
   - `incremental`: charge `units assigned × cost`.
   - `fixed`: charge `cost` **once**, not per unit.
5. Continue until all units are priced; sum across all items.

For a fixed tier, assigning 1 unit or several units incurs the same single tier charge. Assigning 0 incurs no charge.

### Function Signature

```text
calculateMixedShippingCost(country: String, items: String[], rules: String[]) → int
```

### Example 1 — United States

**Input:**

```python
country = "US"
items = ["mouse,20", "laptop,5"]
rules = [
    "US,mouse,incremental,0,*,550",
    "US,laptop,fixed,0,2,1000",
    "US,laptop,incremental,3,*,900",
    "CA,mouse,incremental,0,*,750",
    "CA,laptop,fixed,0,2,1100",
    "CA,laptop,incremental,3,*,1000"
]
```

**Expected Output:**

```text
14700
```

**Explanation:**

- US mouse incremental tier: 20 × 550 = 11,000.
- US laptop first tier `[0,2)` is fixed: 2 units enter, so charge **1,000 once**.
- US laptop second tier `[3,*)` is incremental: 3 × 900 = 2,700.
- Laptop subtotal = 3,700.
- **Total = 11,000 + 3,700 = 14,700.**

### Example 2 — Canada

**Input:**

```python
country = "CA"
items = ["mouse,20", "laptop,5"]
rules = [
    "US,mouse,incremental,0,*,550",
    "US,laptop,fixed,0,2,1000",
    "US,laptop,incremental,3,*,900",
    "CA,mouse,incremental,0,*,750",
    "CA,laptop,fixed,0,2,1100",
    "CA,laptop,incremental,3,*,1000"
]
```

**Expected Output:**

```text
19100
```

**Explanation:**

- CA mouse incremental tier: 20 × 750 = 15,000.
- CA laptop first tier `[0,2)` is fixed: charge 1,100 once for the first 2 units.
- CA laptop second tier `[3,*)` is incremental: 3 × 1,000 = 3,000.
- Laptop subtotal = 4,100.
- **Total = 15,000 + 4,100 = 19,100.**

### Constraints — Part 3

1. Each rule is `country,product,type,minQuantity,maxQuantity,cost`.
2. `type` is `fixed` or `incremental`.
3. `maxQuantity = *` represents an unbounded tier.
4. Process a product's tiers in ascending order of `minQuantity`.
5. Each tier's range is half-open `[minQuantity, maxQuantity)`.
6. A **fixed** tier adds `cost` once if at least one unit enters it.
7. An **incremental** tier adds `units assigned × cost`.
8. A product can mix fixed and incremental tiers.
9. Return the integer total cost across all items.

---