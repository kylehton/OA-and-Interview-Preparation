# P12 — Service Monitor (OOP + Data Structures)

Design a small monitoring component.

Implement:

    class ServiceMonitor:
        record(service: str, status_code: int) -> None
        error_rate(service: str) -> float
        top_unhealthy(n: int) -> list[tuple[str,float]]

Rules:
- A request is an error if status_code >= 500.
- error_rate = errors/total rounded to 4 decimals.
- If service has no records, error_rate(service) returns 0.0.
- top_unhealthy returns up to n services sorted by:
  1) error_rate desc
  2) total_requests desc
  3) service asc

Validity:
- record ignores entries where service is empty or status_code is not int.

## Follow-up (thread safety)
Implement:

    class ThreadSafeServiceMonitor(ServiceMonitor)

Same interface but safe for concurrent calls. (Use a lock.)
