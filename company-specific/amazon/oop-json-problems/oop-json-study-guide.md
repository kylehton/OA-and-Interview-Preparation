# Python OOP + JSON: Full Interview Study Guide

Review for OOP and JSON-centric questions.

---

## Part 1: The JSON module

### The four functions you must know cold

There are exactly four functions that matter. The naming is confusing on purpose — memorize it once.

| Function | Input | Output | When |
|----------|-------|--------|------|
| `json.load(f)` | file object | Python object | Reading from a file |
| `json.loads(s)` | string | Python object | Parsing a string |
| `json.dump(obj, f)` | object + file | writes to file | Writing to a file |
| `json.dumps(obj)` | object | string | Converting to string |

**The mnemonic**: the `s` stands for "string". `loads` loads from a string. `dumps` dumps to a string. No `s` = file.

### Standard reading pattern

```python
import json

with open("data.json") as f:
    data = json.load(f)
```

That's it. `data` is now a Python `dict` or `list` depending on the JSON root.

### Standard writing pattern

```python
with open("out.json", "w") as f:
    json.dump(data, f, indent=2)
```

**Always use `indent=2`** when writing. Unindented JSON is unreadable to the interviewer when they look at your output.

### The type mapping

JSON doesn't have all Python's types. Know what converts to what:

| JSON | Python |
|------|--------|
| `object` | `dict` |
| `array` | `list` |
| `string` | `str` |
| `number` (int) | `int` |
| `number` (decimal) | `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

**What's NOT supported natively**: `datetime`, `set`, `tuple` (becomes list), custom classes, `bytes`. If you try to `json.dumps()` any of these, you get `TypeError: Object of type X is not JSON serializable`.

### Handling non-serializable types

Three approaches, from quickest to cleanest:

**Approach 1: `default=str` (the escape hatch)**
```python
from datetime import datetime
data = {"timestamp": datetime.now()}
json.dumps(data, default=str)  # just stringifies anything it can't handle
```

Good for quick scripts. Says "if you can't serialize it, call `str()` on it."

**Approach 2: Convert before dumping**
```python
data = {"timestamp": datetime.now().isoformat()}
json.dumps(data)  # works, timestamp is now a string
```

Cleanest for interview code. Convert at the boundary.

**Approach 3: Custom encoder**
```python
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, set):
            return list(obj)
        return super().default(obj)

json.dumps(data, cls=DateTimeEncoder)
```

Use this if the interviewer asks "how would you handle multiple custom types cleanly?"

### Reading JSON: navigating nested structures

Given:
```python
data = {
    "users": [
        {"name": "Alice", "roles": ["admin", "user"]},
        {"name": "Bob", "roles": ["user"]}
    ]
}
```

Common operations:
```python
# Access by key
users = data["users"]           # KeyError if missing
users = data.get("users", [])   # returns default if missing

# Iterate
for user in data["users"]:
    print(user["name"])

# Nested access with safety
first_user_role = data["users"][0]["roles"][0]  # fragile, errors on missing
first_user_role = data.get("users", [{}])[0].get("roles", [""])[0]  # safer

# The cleanest safe pattern
users = data.get("users", [])
if users:
    first = users[0]
    roles = first.get("roles", [])
```

**Common interview trap**: the input has a field sometimes missing. Always use `.get(key, default)` for optional fields, not `dict[key]`. Decide at the start: "I'll use `.get()` for anything that might be missing."

### Writing JSON: when field names don't match your class

If your class has `self.employee_id` but the JSON key is `"employeeId"`, handle it explicitly:

```python
@classmethod
def from_dict(cls, d):
    return cls(
        name=d["name"],
        employee_id=d["employeeId"],  # different name
    )

def to_dict(self):
    return {
        "name": self.name,
        "employeeId": self.employee_id,
    }
```

Don't try to be clever with reflection in an interview. Just write the mapping.

---

## Part 2: Python OOP fundamentals

### Basic class structure

```python
class Employee:
    def __init__(self, name, employee_id, salary=0):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary
    
    def give_raise(self, percent):
        self.salary *= (1 + percent / 100)
    
    def __repr__(self):
        return f"Employee(name={self.name!r}, id={self.employee_id!r}, salary={self.salary})"
```

Things to internalize:
- `__init__` is the constructor
- `self` is always the first parameter of instance methods
- Default parameter values go in `__init__`
- `!r` in f-strings calls `repr()` — wraps strings in quotes, which is what you want in `__repr__`

### `__repr__` vs `__str__`

- `__repr__`: for developers. Should look like valid code that recreates the object. Used by default in REPL, lists, debugger.
- `__str__`: for users. Pretty/readable. Falls back to `__repr__` if not defined.

**In interviews**: always define `__repr__`. Skip `__str__` unless asked. Why? Because when you `print([obj1, obj2])`, Python uses `__repr__`. Without it, you get `[<Employee object at 0x7f...>]` and you can't debug anything.

### `@dataclass`: the cheat code

```python
from dataclasses import dataclass, field

@dataclass
class Employee:
    name: str
    employee_id: str
    salary: float = 0.0
    roles: list = field(default_factory=list)
```

This auto-generates:
- `__init__(self, name, employee_id, salary=0.0, roles=None)`
- `__repr__` with all fields shown
- `__eq__` that compares field-by-field

**Critical rule**: mutable defaults (`list`, `dict`, `set`) must use `field(default_factory=list)`, never `= []` directly. This trips people up. If you write `roles: list = []`, every Employee shares the same list — classic Python gotcha.

**When to use `@dataclass`**:
- You have a class that's mostly data with a few methods
- You want free `__repr__` and `__eq__`
- 90% of interview OOP problems

**When NOT to use it**:
- Heavy custom `__init__` logic (validation, derived fields)
- When you need to control attribute access carefully

### The `asdict` helper

```python
from dataclasses import asdict

emp = Employee("Alice", "E001", 100000)
asdict(emp)  # {"name": "Alice", "employee_id": "E001", "salary": 100000, "roles": []}
```

This is huge for JSON serialization. Your `to_dict()` method can just be `return asdict(self)` for simple dataclasses.

**Caveat**: `asdict` recursively converts nested dataclasses too. If you have dataclass A containing dataclass B, `asdict(a)` gives you a fully nested dict. Very useful.

### `from_dict` / `to_dict` pattern

This is the interview-standard pattern for JSON ↔ class conversion:

```python
@dataclass
class Employee:
    name: str
    employee_id: str
    salary: float = 0.0
    
    @classmethod
    def from_dict(cls, d: dict) -> "Employee":
        return cls(
            name=d["name"],
            employee_id=d["employee_id"],
            salary=d.get("salary", 0.0),
        )
    
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "employee_id": self.employee_id,
            "salary": self.salary,
        }
```

Note:
- `from_dict` is a `@classmethod` — it constructs an instance from data
- `cls(...)` inside a classmethod is how you instantiate (not `Employee(...)`)
- Use `.get()` for optional fields with sensible defaults
- `to_dict` is a regular method

**Why not just use `asdict`?** Because sometimes the dict shape differs from the field names, or you want to omit internal state, or add computed fields. `to_dict` gives you control.

### Inheritance basics

```python
class Vehicle:
    def __init__(self, license_plate):
        self.license_plate = license_plate
    
    def describe(self):
        return f"Vehicle {self.license_plate}"


class Car(Vehicle):
    def __init__(self, license_plate, num_doors):
        super().__init__(license_plate)  # call parent __init__
        self.num_doors = num_doors
    
    def describe(self):
        return f"Car {self.license_plate} with {self.num_doors} doors"
```

Key things:
- `class Car(Vehicle)` = Car inherits from Vehicle
- `super().__init__(...)` calls the parent's `__init__`
- Methods in child override methods in parent automatically
- `isinstance(my_car, Vehicle)` returns `True` (Car IS-A Vehicle)

### When to use inheritance vs composition

**Use inheritance** when the child truly IS-A parent (Car IS-A Vehicle). The interface makes sense for both.

**Use composition** when one thing HAS-A another (Car HAS-AN engine). Store the other object as an attribute.

Interview heuristic: prefer composition. Inheritance is often overused. A `ParkingLot` should have a list of `ParkingSpot`s, not inherit from one.

### Abstract base classes (if you have time)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
```

You can't instantiate `Shape()` directly — it's abstract. Any subclass must implement `area()`. Useful for interview design questions where you want to enforce an interface.

Not strictly necessary for most problems. Skip if short on time.

---

## Part 3: Data structure cheatsheet for these problems

### Dicts

```python
d = {}
d["key"] = value              # set
value = d["key"]              # get, raises KeyError if missing
value = d.get("key", default) # get with default
"key" in d                    # membership check
del d["key"]                  # remove
for k, v in d.items():        # iterate pairs
    ...
```

**Dict comprehensions** (know these cold):
```python
{k: v for k, v in items}
{u.user_id: u for u in users}  # index users by ID
{u.user_id: u for u in users if u.active}  # with filter
```

**Grouping by a key** (common interview need):
```python
from collections import defaultdict

groups = defaultdict(list)
for emp in employees:
    groups[emp.department].append(emp)
# groups is now {"Eng": [...], "Sales": [...]}
```

`defaultdict(list)` auto-creates an empty list when you access a missing key. Saves the `if key not in d: d[key] = []` boilerplate.

### Sets

```python
s = set()
s = {1, 2, 3}
s.add(x)
s.remove(x)       # raises if missing
s.discard(x)      # doesn't raise
x in s            # O(1) membership
s1 | s2           # union
s1 & s2           # intersection
s1 - s2           # difference
```

**When to use**: membership checking, deduplication, permissions lookups. Anywhere you'd write `if x in list` with a large list, consider a set instead.

### Lists

Known stuff, but worth the refresh on idioms:

```python
lst.append(x)
lst.extend(other_list)
lst.pop()         # remove and return last
lst.pop(0)        # remove and return first (O(n), avoid if possible)
sorted(lst, key=lambda x: x.salary, reverse=True)
[x for x in lst if x.active]   # filter
[x.name for x in lst]          # map
```

### Counter

```python
from collections import Counter

c = Counter(["a", "b", "a", "c", "a"])
# Counter({'a': 3, 'b': 1, 'c': 1})
c.most_common(2)  # [('a', 3), ('b', 1)]
```

Useful for "find top N" aggregations.

---

## Part 4: Common patterns for these interview problems

### Pattern 1: Load JSON → instantiate classes → build lookup

```python
def load_employees(path):
    with open(path) as f:
        data = json.load(f)
    
    employees = [Employee.from_dict(d) for d in data]
    by_id = {e.employee_id: e for e in employees}
    return employees, by_id
```

Return both a list (for iteration) and a dict (for O(1) lookup). Interview interviewers love this because it shows you think about access patterns.

### Pattern 2: Filter by multiple optional criteria

```python
def filter_events(events, user_id=None, action=None, status=None):
    result = events
    if user_id is not None:
        result = [e for e in result if e.user_id == user_id]
    if action is not None:
        result = [e for e in result if e.action == action]
    if status is not None:
        result = [e for e in result if e.status == status]
    return result
```

Why this shape: each filter is independent, easy to read, easy to extend. Don't try to be clever with a single big predicate.

### Pattern 3: Aggregation with defaultdict

```python
from collections import defaultdict

def failure_rate_by_user(events):
    totals = defaultdict(int)
    failures = defaultdict(int)
    
    for e in events:
        totals[e.user_id] += 1
        if e.status == "failure":
            failures[e.user_id] += 1
    
    return {
        user_id: failures[user_id] / totals[user_id]
        for user_id in totals
    }
```

Two-pass counting into defaultdicts, then a dict comprehension for the final result.

### Pattern 4: Datetime parsing and windowing

```python
from datetime import datetime, timedelta

def parse_iso(s):
    # Handle "2026-04-20T10:15:00Z" (Z suffix)
    return datetime.fromisoformat(s.replace("Z", "+00:00"))

def sliding_window_count(events, window_minutes):
    # events sorted by time
    events = sorted(events, key=lambda e: e.timestamp)
    result = []
    for i, anchor in enumerate(events):
        count = 0
        for j in range(i, len(events)):
            if events[j].timestamp - anchor.timestamp <= timedelta(minutes=window_minutes):
                count += 1
            else:
                break
        result.append((anchor, count))
    return result
```

O(n²) in the worst case. For an interview, mention "this could be optimized with a deque for O(n), but let's get correctness first."

### Pattern 5: Round-trip serialization

```python
class ControlLibrary:
    @classmethod
    def load(cls, path):
        with open(path) as f:
            data = json.load(f)
        lib = cls()
        for fw_data in data.get("frameworks", []):
            lib.add_framework(Framework.from_dict(fw_data))
        for c_data in data.get("controls", []):
            lib.add_control(Control.from_dict(c_data))
        return lib
    
    def save(self, path):
        data = {
            "frameworks": [fw.to_dict() for fw in self.frameworks.values()],
            "controls": [c.to_dict() for c in self.controls.values()],
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
```

Symmetric structure: `load` reads dict → objects, `save` writes objects → dict. A good interviewer will verify round-tripping ("if I load and save, do I get the same JSON?"). Plan for it.

---

## Part 5: Error handling and validation

### When to raise

Raise exceptions when the operation can't meaningfully proceed:

```python
def add_evidence(self, control_id, evidence_data):
    if control_id not in self.controls:
        raise ValueError(f"Unknown control: {control_id}")
    evidence = Evidence.from_dict(evidence_data)
    self.evidence.append(evidence)
```

**Which exception**:
- `ValueError`: bad input data
- `KeyError`: missing dictionary key (usually auto-raised, don't raise manually unless mimicking)
- `TypeError`: wrong type passed
- Custom: for domain errors, `class ControlNotFoundError(Exception): pass`

### When to return None or empty

When "not found" is a normal case, not an error:

```python
def find_user(self, user_id):
    return self.users.get(user_id)  # None if missing, caller decides
```

### Validation in `__init__`

```python
@dataclass
class Employee:
    name: str
    salary: float
    
    def __post_init__(self):
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
```

`__post_init__` runs after the auto-generated `__init__` in a dataclass. Useful for validation.

---

## Part 6: Talking about your code (interview-specific)

### Things to say out loud while coding

- "I'm going to use a dataclass here to avoid writing boilerplate."
- "I'm indexing by ID into a dict for O(1) lookup."
- "I'll use `.get()` here because this field is optional in the spec."
- "Let me start with correctness and we can optimize after if there's time."
- "For datetime, I'll parse to a `datetime` object internally and convert to ISO string on output."

### Things to ask before coding

- "Are the IDs guaranteed unique?"
- "What should happen if a required field is missing — raise or skip?"
- "Is this loaded once or do we need to support live updates?"
- "Should the output JSON match the input format exactly for round-tripping?"
- "What's the expected data volume? Does it fit in memory?"

### Design trade-offs to raise

When designing classes, articulate why you made a choice:

- **List vs dict for lookup**: "I used a dict keyed by ID because we look up controls frequently; the load cost is a one-time O(n)."
- **Composition vs inheritance**: "I made Framework a separate object rather than an enum because we want to store metadata per framework."
- **Mutable vs immutable**: "I'm using a frozen dataclass here because these should be value objects."

These one-liners are what separates a solid intern from a "just writes code" intern.

---

## Part 7: Final checklist before you start a problem

1. Read the prompt twice. Identify: input format, output format, required operations.
2. List the entities. These are your classes.
3. List the relationships. These tell you if you need composition or just references.
4. Write the dataclass definitions first. Stub methods with `pass`.
5. Write `from_dict` and `to_dict` for each class that's loaded/saved.
6. Write the loader function. Test mentally against the example input.
7. Implement operations one at a time, simplest first.
8. After each operation, trace through the example to verify.
9. If time: add validation, raise on bad input, consider edge cases.
10. If asked: talk through what you'd do differently with more time.

---

## Minimum competency self-test

If you can answer all of these without looking, you're ready:

1. Difference between `json.load` and `json.loads`?
2. How do you serialize a `datetime`?
3. What does `@dataclass` give you for free?
4. Why use `field(default_factory=list)` instead of `= []`?
5. How do you write a classmethod and why use one for `from_dict`?
6. Difference between `__repr__` and `__str__`?
7. How do you call a parent class method from a child?
8. How do you group a list of objects by some attribute?
9. How do you check if a key exists in a dict safely?
10. What's the time complexity of `x in set` vs `x in list`?

If any of those are shaky, re-read the relevant section. Don't skip.