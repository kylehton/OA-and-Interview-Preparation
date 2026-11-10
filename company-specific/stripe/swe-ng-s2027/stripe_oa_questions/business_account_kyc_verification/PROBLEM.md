
# Business Account KYC Verification — Parts 1–5

**Company:** Stripe  
**Difficulty:** Medium  
**Roles:** Intern, Full-Time, New Grad  
**Interview Stage:** Phone Screen

---

## Problem Statement

Validate each business account through a five-part KYC process.

Parts 1–4 are ordered validation checks. Part 5 encodes the result.

`csvData` contains a header followed by business rows with six comma-separated fields:

1. `business_name`
2. `business_profile_name`
3. `full_statement_descriptor`
4. `short_statement_descriptor`
5. `url`
6. `product_description`

Trim surrounding whitespace from every field.

---

## Part 1 — Required Fields

All six fields must be present and non-empty after trimming whitespace.

If any field is missing or empty, the business fails validation.

**Error code:** `MISSING_FIELD`

---

## Part 2 — Descriptor Length

`full_statement_descriptor` must contain between **5 and 31 characters**, inclusive, after trimming.

**Error code:** `INVALID_DESCRIPTOR_LENGTH`

---

## Part 3 — Generic Descriptor Check

The `full_statement_descriptor` must not equal any of the following strings, case-insensitively:

- `ONLINE STORE`
- `ECOMMERCE`
- `RETAIL`
- `SHOP`
- `GENERAL MERCHANDISE`

The comparison uses exact equality, not substring matching.

**Error code:** `GENERIC_DESCRIPTOR`

---

## Part 4 — Business-Name Similarity

Compare `business_name` and `business_profile_name`.

Normalize both names into sets of **distinct uppercase ASCII alphanumeric tokens**.

Ignore the following legal or generic tokens:

```text
THE
INC
INCORPORATED
LLC
LTD
LIMITED
CORP
CORPORATION
COMPANY
CO
```

### Matching Rules

The names match when:

1. Both normalized token sets are non-empty.
2. The number of shared tokens is at least half the size of the smaller set.
3. The half-overlap threshold is inclusive.

**Error code:** `NAME_MISMATCH`

---

## Part 5 — Error Codes

Apply the four validation checks in order and report **only the first failure**.

Return one string per business.

### Possible Results

```text
VERIFIED: <business_name> | OK

NOT VERIFIED: <business_name> | MISSING_FIELD

NOT VERIFIED: <business_name> | INVALID_DESCRIPTOR_LENGTH

NOT VERIFIED: <business_name> | GENERIC_DESCRIPTOR

NOT VERIFIED: <business_name> | NAME_MISMATCH
```

### Validation Order

1. `MISSING_FIELD`
2. `INVALID_DESCRIPTOR_LENGTH`
3. `GENERIC_DESCRIPTOR`
4. `NAME_MISMATCH`
5. `OK` — if all checks pass

If multiple checks would fail, only the first failure in this order is reported.

Results must be returned in the same order as the input rows.

---

## Function Signature

```text
validateBusinesses(csvData: String) → String[]
```

### Input

`csvData`: A string containing a CSV header and business records.

### Output

An array of strings containing the verification result for each business row.

---

## Examples

### Example 1

**Input:**

```text
business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description
Pawsome Pets Inc.,Pawsome Pets,PAWSOME PETS,Pawsome,pawsome.example,Pet supplies
Bean Bliss Coffee Company,Bean Bliss,,Bean,bean.example,Coffee beans
Global Goods Marketplace Inc.,Global Goods,RETAIL,Global,goods.example,General products
```

**Expected Output:**

```text
[
  "VERIFIED: Pawsome Pets Inc. | OK",
  "NOT VERIFIED: Bean Bliss Coffee Company | MISSING_FIELD",
  "NOT VERIFIED: Global Goods Marketplace Inc. | GENERIC_DESCRIPTOR"
]
```

**Explanation:**

- Pawsome passes all five parts.
- Bean Bliss fails the required-field check because its full descriptor is empty. `MISSING_FIELD` takes precedence.
- Global Goods uses `RETAIL`, which is a prohibited generic descriptor.

### Example 2

**Input:**

```text
business_name,business_profile_name,full_statement_descriptor,short_statement_descriptor,url,product_description
Alpha Beta Gamma Delta LLC,Alpha Beta Epsilon Zeta,ALPHA BETA GOODS,Alpha,alpha.example,Analytics
North Star Labs,Totally Different,STAR SERVICES,Star,north.example,Software
```

**Expected Output:**

```text
[
  "VERIFIED: Alpha Beta Gamma Delta LLC | OK",
  "NOT VERIFIED: North Star Labs | NAME_MISMATCH"
]
```

**Explanation:**

- Alpha Beta shares exactly two of four normalized tokens, satisfying the inclusive half-overlap requirement.
- North Star Labs shares no normalized name tokens with Totally Different and fails the similarity check.

---

## Constraints

1. The first line is a header and is not validated.
2. Each data row is a simple six-field CSV row with no embedded commas or quoted commas.
3. One or more empty lines at the end are ignored as record terminators.
4. An empty interior row is validated and fails Part 1.
5. Input fields use ASCII characters, so descriptor lengths and name tokenization are identical across supported languages.
6. All fields are trimmed.
7. An empty trimmed value fails Part 1.
8. The full descriptor length interval is inclusive at 5 and 31.
9. The descriptor blocklist uses case-insensitive exact equality, not substring matching.
10. Name tokens are distinct ASCII letters/digits separated by any non-alphanumeric character.
11. The four checks are evaluated in Parts 1, 2, 3, then 4 order.
12. Part 5 results must be returned in input order.

---
