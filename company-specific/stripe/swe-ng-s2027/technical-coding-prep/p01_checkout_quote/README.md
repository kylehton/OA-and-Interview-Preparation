# P01 — Checkout Quote

**Difficulty:** Easy  
**Target:** 35 minutes  
**Entry point:** `checkout_total(catalog, order, rules=None) -> int`

All monetary values are integer cents. Parse comma-separated fields after
trimming surrounding whitespace. Do not use floating-point arithmetic.

## Part 1 — Base total

`catalog` rows have the form:

```text
<sku>,<unit_price>
```

`order` rows have the form:

```text
<sku>,<quantity>
```

Return the sum of `unit_price * quantity`. Repeated order rows for the same SKU
are combined. If a SKU appears more than once in the catalog, the first valid
row wins.

## Part 2 — Defensive parsing

A valid catalog row has exactly two fields, a non-empty SKU, and a positive
integer price. A valid order row has exactly two fields, a known non-empty SKU,
and a positive integer quantity. Ignore invalid rows without partially applying
them. An empty or wholly invalid order costs `0`.

## Part 3 — Best item discount

Support these optional `rules` rows:

```text
BULK,<sku>,<minimum_quantity>,<discounted_unit_price>
PERCENT,<sku>,<basis_points_off>
```

All numeric fields must be positive integers. `basis_points_off` must be at most
`10000`. A bulk rule applies when the SKU's combined quantity meets its minimum.
A percentage rule produces:

```python
base_line_total * (10000 - basis_points_off) // 10000
```

For each SKU independently, calculate every applicable valid candidate and use
the lowest line total. Discounts do not stack. Rules for unknown SKUs are
ignored.

## Part 4 — Tax after discounts

Support:

```text
TAX,<basis_points>
```

The basis points must be an integer from `0` through `10000`. The first valid
`TAX` row wins. Tax is calculated once on the discounted subtotal:

```python
tax = subtotal * tax_basis_points // 10000
final_total = subtotal + tax
```

## Example

```python
catalog = ["notebook,500", "pen,125"]
order = ["notebook,2", "pen,4", "pen,2"]
rules = ["BULK,pen,5,100", "PERCENT,notebook,1000", "TAX,825"]

checkout_total(catalog, order, rules)  # 1623
```

The notebook costs `900`, the six pens cost `600`, and 8.25% tax contributes
`123` cents.

Aim for `O(C + O + R)` time and `O(C + O)` space.

