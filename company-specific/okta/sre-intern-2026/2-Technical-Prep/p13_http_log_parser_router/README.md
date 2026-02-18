# P13 — HTTP Log Router (String Parsing + Robustness)

File format per line:

    <method> <path> <status>

Examples:
    GET /api/v1/users 200
    POST /api/v1/login 401

Implement:

    route_stats(filepath: str) -> dict[str, dict[str,int]]

Normalize routes by replacing numeric path segments with "{id}".

Example:
    /api/v1/users/123/profile  -> /api/v1/users/{id}/profile

Return:
{
  "/api/v1/users/{id}/profile": {"2xx": 10, "4xx": 3, "5xx": 1},
  "/api/v1/login": {"2xx": 0, "4xx": 5, "5xx": 0}
}

Rules:
- Only count valid lines with exactly 3 tokens
- method ignored other than being present
- status must be int
- bucket status:
  - 200-299 => "2xx"
  - 400-499 => "4xx"
  - 500-599 => "5xx"
  - other statuses ignored

Follow-up:
    top_routes_by_5xx(filepath, k) -> list[tuple[str,int]]
Sort by 5xx desc, route asc.
