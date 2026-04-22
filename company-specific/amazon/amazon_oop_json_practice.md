# Amazon Intern: OOP + JSON Practice Set

Five problems in increasing complexity, write in real code for practical coding reinforcement. 
Target: 25-40 min per problem.

---

## Problem 1: Employee Directory (warmup, ~25 min)

**Prompt**

You're given a JSON file `employees.json` with a list of employees. Each employee has a name, employee_id, department, and salary. Some entries may be missing fields.

Build a system that:
1. Loads employees from the JSON file
2. Models each employee as a class
3. Supports these operations:
   - `get_by_department(dept)` → list of employees
   - `average_salary(dept)` → float (ignore employees missing salary)
   - `give_raise(employee_id, percent)` → updates salary
   - `save_to_file(path)` → writes current state back to JSON

**Example input**
```json
[
  {"name": "Alice", "employee_id": "E001", "department": "Eng", "salary": 120000},
  {"name": "Bob", "employee_id": "E002", "department": "Eng"},
  {"name": "Carol", "employee_id": "E003", "department": "Sales", "salary": 95000}
]
```

**What this tests**
- Basic class design with `__init__`, `__repr__`
- `json.load` / `json.dump` with file objects
- Handling missing fields gracefully (use `.get()` with defaults)
- Serialization back to JSON (dunder method `to_dict()` is clean)

**Gotchas to watch for**
- Writing `json.dump(obj)` when you meant `json.dumps(obj)` — `dump` needs a file handle
- Forgetting `indent=2` makes output unreadable
- Not handling the missing-salary case in `average_salary`

---

## Problem 2: Access Control List (~30 min)

**Prompt**

A compliance system has users and resources. Users have roles. Each role grants certain permissions on certain resource types. Implement:

1. Classes: `User`, `Role`, `Resource`, `AccessControlList`
2. Load config from JSON (roles and their permissions)
3. Load users from JSON (each user has a list of role names)
4. Method: `can_access(user_id, resource_id, action)` → bool
   - Actions are "read", "write", "delete"
   - A user can perform the action if any of their roles grant it for that resource type

**Example config**
```json
{
  "roles": [
    {"name": "viewer", "permissions": {"document": ["read"]}},
    {"name": "editor", "permissions": {"document": ["read", "write"]}},
    {"name": "admin", "permissions": {"document": ["read", "write", "delete"], "user": ["read", "write"]}}
  ],
  "users": [
    {"user_id": "u1", "roles": ["viewer"]},
    {"user_id": "u2", "roles": ["editor", "viewer"]}
  ],
  "resources": [
    {"resource_id": "doc1", "type": "document"},
    {"resource_id": "user_profile", "type": "user"}
  ]
}
```

**What this tests**
- Multiple classes with relationships (composition)
- Parsing nested JSON
- Set/dict lookups for performance
- Exactly the kind of modeling a compliance platform does

**Design hint**: Store permissions as `dict[role_name] -> dict[resource_type] -> set[action]` internally, even though the JSON has them as lists. Converting to sets on load makes `can_access` O(1).

---

## Problem 3: Audit Log Aggregator (~35 min)

**Prompt**

You're given a JSON file containing a stream of audit events (think: CloudTrail-lite). Each event has a timestamp, user_id, action, resource, and status ("success" or "failure"). Build a system that:

1. Loads events and models them as `AuditEvent` objects
2. Supports filtering: `filter_by(user_id=None, action=None, status=None, start_time=None, end_time=None)`
3. Aggregates: `failure_rate_by_user()` → dict[user_id, float]
4. Detects suspicious activity: `find_brute_force_attempts(threshold=5, window_minutes=10)` — users with ≥ threshold failures inside any rolling window
5. Exports flagged events to a new JSON file

**Example input**
```json
[
  {"timestamp": "2026-04-20T10:15:00Z", "user_id": "u1", "action": "login", "resource": "console", "status": "failure"},
  {"timestamp": "2026-04-20T10:16:00Z", "user_id": "u1", "action": "login", "resource": "console", "status": "failure"},
  {"timestamp": "2026-04-20T10:20:00Z", "user_id": "u2", "action": "read", "resource": "doc1", "status": "success"}
]
```

**What this tests**
- Datetime parsing (ISO 8601 strings → `datetime` objects)
- Custom JSON encoder for datetime on export (or convert back to ISO string)
- A sliding window algorithm on top of OOP data modeling
- This is the most "real work" flavored problem of the five

**Key Python bits**
- `datetime.fromisoformat(s.replace("Z", "+00:00"))` for parsing
- For custom encoding on dump: `json.dump(obj, f, default=str)` is a cheap escape hatch
- Or define a `DateTimeEncoder(json.JSONEncoder)` and pass `cls=DateTimeEncoder`

**Gotcha**: "rolling window" is the trap. The naive O(N²) solution is fine for interview — don't over-optimize with deques unless you have time. Mention the tradeoff out loud.

---

## Problem 4: Compliance Control Library (~40 min)

**Prompt**

This one is thematically the closest to your actual team's work.

You're building a mini version of a Risk and Control Library. The JSON defines:
- **Frameworks** (e.g., "SOC2", "ISO27001")
- **Controls** (each has an id, title, description, and maps to one or more frameworks)
- **Evidence** items (each has an id, control_id, type, status, and collected_date)

Build:
1. Classes: `Framework`, `Control`, `Evidence`, `ControlLibrary`
2. Load everything from a single JSON config
3. Methods:
   - `get_controls_for_framework(framework_id)` → list of Controls
   - `coverage_report(framework_id)` → dict with total_controls, controls_with_evidence, coverage_percent
   - `stale_evidence(days=90)` → list of evidence older than N days
   - `add_evidence(control_id, evidence_data)` — validates the control exists, raises otherwise
4. Export the current library state to JSON (round-trip: `ControlLibrary.load(path)` then `.save(path2)` should produce equivalent data)

**Example input**
```json
{
  "frameworks": [
    {"id": "SOC2", "name": "SOC 2 Type II"},
    {"id": "ISO27001", "name": "ISO/IEC 27001:2022"}
  ],
  "controls": [
    {"id": "AC-1", "title": "Access control policy", "frameworks": ["SOC2", "ISO27001"]},
    {"id": "AC-2", "title": "Account management", "frameworks": ["SOC2"]}
  ],
  "evidence": [
    {"id": "E-001", "control_id": "AC-1", "type": "policy_doc", "status": "approved", "collected_date": "2025-11-15"},
    {"id": "E-002", "control_id": "AC-2", "type": "screenshot", "status": "pending", "collected_date": "2026-04-01"}
  ]
}
```

**What this tests**
- Multi-entity domain modeling (this is the actual job at a compliance platform)
- Round-trip serialization correctness
- Validation logic (rejecting evidence for nonexistent controls)
- Domain reasoning (coverage, staleness — interviewer-friendly talking points)

**Talking points to have ready if you do this one well**
- Why you modeled frameworks as their own class vs. just strings on Control (extensibility)
- Why you used dicts keyed by id internally vs. just lists (lookup perf)
- How you'd extend this to support control-to-control dependencies

---

## Problem 5: Config Diff Tool (~35 min, stretch)

**Prompt**

Compliance teams constantly diff configurations between environments ("what changed in prod since last audit?"). Build a tool that:

1. Loads two JSON files representing system configs (nested dicts and lists)
2. Produces a diff showing:
   - Keys added
   - Keys removed
   - Keys with changed values (show old and new)
3. Supports nested paths using dot notation (e.g., `"database.host"`)
4. Outputs the diff as structured JSON
5. Bonus: `apply_diff(config, diff)` → config — apply a diff to transform one config into another

**Example**
```json
// old.json
{"database": {"host": "db.old.com", "port": 5432}, "features": {"auth": true}}

// new.json
{"database": {"host": "db.new.com", "port": 5432, "replica": "db2.new.com"}, "features": {"auth": true, "sso": true}}

// expected diff
{
  "added": {"database.replica": "db2.new.com", "features.sso": true},
  "removed": {},
  "changed": {"database.host": {"old": "db.old.com", "new": "db.new.com"}}
}
```

**What this tests**
- Recursive traversal of nested structures
- Designing a representation for diffs (harder than it sounds)
- Edge cases: what if a value changes from dict to scalar? From list to dict?

**If you're short on time, skip this one.** It's the hardest and least likely to be interview-shaped.

---

## How to work through these

1. **Write actual code.** Don't just sketch. The goal is muscle memory on `json.load`, class structure, and common patterns.
2. **Time yourself.** Stop at 40 min even if unfinished. Interview time pressure is real.
3. **After each problem, do a 5-min review:** what did I fumble? What would I say differently to an interviewer?
4. **Talk out loud** on at least two of them. Pretend you're being watched.

## Priority order if you can only do some

- **Must do**: Problem 1 (mechanics) + Problem 2 (multi-class design)
- **Should do**: Problem 4 (thematically closest to your team)
- **Nice to have**: Problem 3 (time-series flavor)
- **Skip if crunched**: Problem 5

## Python `json` quick reference

```python
import json

# File → Python object
with open("data.json") as f:
    data = json.load(f)

# String → Python object
data = json.loads('{"key": "value"}')

# Python object → file
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)

# Python object → string
s = json.dumps(data, indent=2)

# Custom types (e.g., datetime)
json.dumps(data, default=str)  # quick escape hatch

# Or a proper encoder
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

## OOP patterns worth having ready

```python
from dataclasses import dataclass, field, asdict

@dataclass
class Employee:
    name: str
    employee_id: str
    department: str
    salary: float = 0.0
    
    @classmethod
    def from_dict(cls, d: dict) -> "Employee":
        return cls(
            name=d["name"],
            employee_id=d["employee_id"],
            department=d.get("department", "Unknown"),
            salary=d.get("salary", 0.0),
        )
    
    def to_dict(self) -> dict:
        return asdict(self)
```

`@dataclass` is your friend for intern-level OOP — it gives you `__init__`, `__repr__`, and `__eq__` for free. Many candidates don't know about it; using it signals fluency.
