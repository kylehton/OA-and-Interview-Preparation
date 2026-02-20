 # P01 — Log Error Rate Aggregator (File I/O + Parsing)

You are given an access log file where each non-empty line is:

    <iso8601_timestamp> <service> <status_code>

Example:
    2026-02-17T10:00:00 auth-service 200
    
    2026-02-17T10:00:01 auth-service 500

## Task

Implement:

    compute_error_rate(filepath: str) -> dict[str, float]

Return a mapping of service -> error rate, where:
- total requests = number of valid lines for that service
- error requests = status_code >= 500
- error rate = error / total
- round to 4 decimal places (e.g., 0.3333)

### Validity rules
A line is **valid** only if:
- it splits into exactly 3 tokens by whitespace
- status_code is an integer
- service is a non-empty string

Invalid lines must be ignored.

### Output rules
- If a service has 0 valid lines, it must not appear in output.
- Return a normal dict (order not required).

## Follow-up (implemented as separate function)

Implement:

    services_by_error_rate(filepath: str) -> list[tuple[str, float]]

Return a list of (service, error_rate) sorted by:
1) descending error_rate
2) if tie: descending total_requests
3) if tie: lexicographically ascending service name

## Constraints
- File can be large: process line-by-line (do not read entire file into memory).
- O(n) time, O(#services) memory.

## Notes
- Timestamp does not need to be validated beyond being a token.
