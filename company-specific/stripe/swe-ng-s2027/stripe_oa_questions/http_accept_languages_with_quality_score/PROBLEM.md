
# HTTP Accept-Language Matching — Parts 1–4

**Company:** Stripe  
**Difficulty:** Medium  
**Roles:** Full-Time, New Grad, Intern  
**Interview Stage:** Phone Screen  
**Topics:** String Parsing, Matching, Deduplication, Sorting

---

## Problem Statement

You serve localized content by resolving a browser's HTTP `Accept-Language` header against the languages your server supports.

The header lists language tags in order of preference, separated by commas, with optional surrounding spaces.

Given `acceptHeader` and `supportedLanguages`, return the supported language tags that work for the request.

The problem is divided into four parts:

1. Exact language matching
2. Generic language (prefix) matching
3. Wildcard matching
4. Quality-score matching and sorting

Parts 1–3 establish the matching rules. Part 4 extends the matcher with numeric quality factors.

---

## Part 1 — Exact Matching

A language tag such as `en-US` matches the identical tag in `supportedLanguages`.

Only supported tags that exactly match the requested tag are included.

### Requirements

- Process header entries from left to right.
- Match complete language tags.
- Skip unsupported languages.
- Preserve the client's preference order.
- Never return the same supported language twice.

### Example

**Input:**

```text
acceptHeader = "en-US, fr-FR"
supportedLanguages = ["fr-FR", "en-US"]
```

**Expected Output:**

```text
["en-US", "fr-FR"]
```

The output follows the header's preference order rather than the order of `supportedLanguages`.

---

## Part 2 — Generic Language (Prefix Matching)

A region-less language tag such as `en` matches supported language variants beginning with `en-`.

For example, `en` matches:

- `en-US`
- `en-GB`
- `en-AU`

### Requirements

- A generic tag matches supported tags starting with the generic tag followed by `-`.
- If several supported languages match one generic tag, preserve their order from `supportedLanguages`.
- Do not add previously selected languages again.
- Continue processing header entries in their original order.

### Example

**Input:**

```text
acceptHeader = "fr"
supportedLanguages = ["en-US", "fr-CA", "fr-FR"]
```

**Expected Output:**

```text
["fr-CA", "fr-FR"]
```

Both French variants match the generic `fr` request.

---

## Part 3 — Wildcard Matching

The wildcard `*` matches every supported language that has not already been selected.

### Requirements

- `*` selects all remaining unmatched supported languages.
- Preserve their order from `supportedLanguages`.
- Do not return duplicates.
- Process wildcard entries according to their position in the header.

### Example

**Input:**

```text
acceptHeader = "fr-FR, *"
supportedLanguages = ["en-US", "fr-CA", "fr-FR"]
```

**Expected Output:**

```text
["fr-FR", "en-US", "fr-CA"]
```

The exact match `fr-FR` is selected first. The wildcard then selects the remaining supported languages.

---

## Matching Order and Deduplication (Parts 1–3)

Process the `acceptHeader` entries strictly from left to right.

For each entry:

1. Determine whether it is an exact, generic, or wildcard request.
2. Apply the appropriate matching rule.
3. Add the matched supported languages to the result.
4. Skip any supported language already selected.

**Important:** Exact, generic, and wildcard matching do not have global priority over one another.

A generic entry appearing before an exact entry is processed first.

When one entry matches several supported languages, preserve their order from `supportedLanguages`.

---

## Function Signature — Parts 1–3

```text
parseAcceptLanguage(
    acceptHeader: String,
    supportedLanguages: String[]
) → String[]
```

### Input

**`acceptHeader`**

A comma-separated string of requested language tags ordered by client preference.

**`supportedLanguages`**

An array containing language tags supported by the server.

### Output

A `String[]` containing matched supported languages in client preference order without duplicates.

---

## Examples — Parts 1–3

### Example 1

**Input:**

```text
acceptHeader = "fr-FR, fr"
supportedLanguages = ["en-US", "fr-CA", "fr-FR"]
```

**Expected Output:**

```text
["fr-FR", "fr-CA"]
```

**Explanation:**

1. `fr-FR` exactly matches a supported language.
2. The generic `fr` matches the remaining variant `fr-CA`.
3. `fr-FR` is skipped during generic matching because it was already selected.
4. `en-US` is not requested.

### Example 2

**Input:**

```text
acceptHeader = "fr-FR, fr, *"
supportedLanguages = ["en-US", "fr-CA", "fr-FR"]
```

**Expected Output:**

```text
["fr-FR", "fr-CA", "en-US"]
```

**Explanation:**

1. `fr-FR` is selected through exact matching.
2. `fr` selects `fr-CA` through generic matching.
3. `fr-FR` is not selected again.
4. The wildcard selects the last unmatched supported language, `en-US`.

### Example 3

**Input:**

```text
acceptHeader = "en-US, fr-CA, fr-FR"
supportedLanguages = ["fr-FR", "en-US"]
```

**Expected Output:**

```text
["en-US", "fr-FR"]
```

**Explanation:**

1. `en-US` matches exactly.
2. `fr-CA` is unsupported and is skipped.
3. `fr-FR` matches exactly.
4. The result follows the header's preference order.

---

## Part 4 — Quality Scores (q-factors)

Extend the HTTP Accept-Language matcher to support numeric quality factors.

Each requested language may include a quality factor using the following syntax:

```text
tag;q=value
```

Where:

```text
0 <= value <= 1
```

If an entry does not specify `;q=`, its quality defaults to `1.0`.

### Requirements

1. Each header entry is either `tag` or `tag;q=value`.
2. Quality factors are numeric values between 0 and 1, inclusive.
3. Missing quality factors default to `1.0`.
4. Exact, generic, and wildcard matching continue to use the rules from Parts 1–3.
5. Each supported language receives the quality score of the header entry that selected it.
6. A supported language is selected only once.
7. Return the matched supported languages sorted by quality in descending order.
8. When quality scores tie, preserve the original match order.
9. A quality score of `0` is valid and sorts last.
10. Return only the language tags, not the quality scores.

### Important Ordering Distinction

Parts 1–3 return matches according to the client's header preference order.

Part 4 introduces a new final ordering requirement:

**Matched languages must be sorted by descending quality score.**

When two or more languages have equal quality, their original match order must be preserved.

---

## Function Signature — Part 4

```text
parseAcceptLanguageWithQuality(
    acceptHeader: String,
    supportedLanguages: String[]
) → String[]
```

### Input

**`acceptHeader`**

A comma-separated list of language entries, potentially containing quality factors.

Each entry takes one of these forms:

```text
en-US
en-US;q=0.8
fr;q=0.5
*;q=0.2
```

**`supportedLanguages`**

An array of language tags supported by the server.

### Output

A `String[]` containing matched supported languages ordered by descending quality score.

Only language tags are returned.

---

## Examples — Part 4

### Example 1 — Exact and Generic Matches with Quality

**Input:**

```text
acceptHeader = "fr-FR;q=1, fr-CA;q=0, fr;q=0.5"

supportedLanguages = ["fr-FR", "fr-CA", "fr-BG"]
```

**Expected Output:**

```text
["fr-FR", "fr-BG", "fr-CA"]
```

**Explanation:**

- `fr-FR` matches exactly with quality `1.0`.
- `fr-CA` matches exactly with quality `0`.
- The generic `fr` matches the remaining French variant `fr-BG` with quality `0.5`.

The final result is sorted by descending quality:

1. `fr-FR` — 1.0
2. `fr-BG` — 0.5
3. `fr-CA` — 0

### Example 2 — Wildcard with Quality

**Input:**

```text
acceptHeader = "fr-FR;q=1, fr-CA;q=0, *;q=0.5"

supportedLanguages = ["fr-FR", "fr-CA", "fr-BG", "en-US"]
```

**Expected Output:**

```text
["fr-FR", "fr-BG", "en-US", "fr-CA"]
```

**Explanation:**

- `fr-FR` matches exactly with quality `1.0`.
- `fr-CA` matches exactly with quality `0`.
- The wildcard selects the remaining supported languages:
  - `fr-BG` with quality `0.5`
  - `en-US` with quality `0.5`

The final ordering is:

1. `fr-FR` — 1.0
2. `fr-BG` — 0.5
3. `en-US` — 0.5
4. `fr-CA` — 0

The tied languages `fr-BG` and `en-US` retain their match order.

### Example 3 — Generic Matches with Different Qualities

**Input:**

```text
acceptHeader = "en;q=0.8, fr;q=0.9, de;q=0.7"

supportedLanguages = ["en-US", "fr-FR", "de-DE"]
```

**Expected Output:**

```text
["fr-FR", "en-US", "de-DE"]
```

**Explanation:**

- Generic `en` matches `en-US` with quality `0.8`.
- Generic `fr` matches `fr-FR` with quality `0.9`.
- Generic `de` matches `de-DE` with quality `0.7`.

The result is sorted by descending quality:

1. `fr-FR` — 0.9
2. `en-US` — 0.8
3. `de-DE` — 0.7

---

## Constraints — Parts 1–3

1. `acceptHeader` is a comma-separated list of language tags with optional surrounding whitespace.
2. Exact matches use the complete language tag.
3. A region-less generic tag matches every supported tag starting with the generic tag followed by `-`.
4. The wildcard `*` matches all supported tags that have not already been selected.
5. Wildcard matches preserve the order of `supportedLanguages`.
6. Header entries are processed from left to right.
7. When a single header entry matches multiple supported tags, their order follows `supportedLanguages`.
8. A supported language must never appear more than once.
9. Return the matched supported tags as a `String[]`.

## Constraints — Part 4

1. Each header entry has the form `tag` or `tag;q=value`.
2. Quality factors satisfy `0 <= q <= 1`.
3. An entry without a quality factor defaults to `q=1.0`.
4. Matching uses the existing exact, generic, and wildcard rules.
5. A supported tag receives the quality score from the entry that selected it.
6. A supported tag is selected only once.
7. Matched languages are sorted by descending quality score.
8. Equal-quality matches preserve their original match order (stable ordering).
9. A quality score of `0` is valid and sorts last.
10. Return only the language tags as a `String[]`.

---