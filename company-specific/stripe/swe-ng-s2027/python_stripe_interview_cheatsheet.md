# Python Interview Cheatsheet

Quick-reference Python basics for Stripe-style practical coding interviews.

## Lists

```python
arr = [1, 2, 3]

arr.append(4)          # add to end
x = arr.pop()          # remove + return last
x = arr.pop(0)         # remove index 0, O(n)
arr.insert(1, 10)      # insert at index

len(arr)
arr[0]                 # first
arr[-1]                # last

arr[1:3]               # slice
arr[::-1]              # reversed copy

arr.reverse()          # reverse in place
arr.sort()             # sort in place
sorted_arr = sorted(arr)
```

Looping:

```python
for x in arr:
    print(x)

for i, x in enumerate(arr):
    print(i, x)

for i in range(len(arr)):
    print(arr[i])
```

Comprehensions:

```python
squares = [x * x for x in arr]
evens = [x for x in arr if x % 2 == 0]
```

## Dictionaries

Probably the most important structure for Stripe-style problems.

```python
d = {}

d["alice"] = 100

value = d["alice"]          # KeyError if missing
value = d.get("alice", 0)   # default if missing

if "alice" in d:
    ...

del d["alice"]
```

Looping:

```python
for key in d:
    print(key)

for key, value in d.items():
    print(key, value)

for value in d.values():
    print(value)
```

Useful patterns:

```python
d.setdefault("alice", []).append(10)

counts = {}
for x in arr:
    counts[x] = counts.get(x, 0) + 1
```

## `defaultdict`

```python
from collections import defaultdict

counts = defaultdict(int)
counts["alice"] += 1

groups = defaultdict(list)
groups["team_a"].append("alice")

seen_by_key = defaultdict(set)
seen_by_key["alice"].add("tx1")
```

## `Counter`

```python
from collections import Counter

counts = Counter(["a", "b", "a"])
# Counter({"a": 2, "b": 1})

counts["a"]

counts.most_common()
counts.most_common(2)
```

## Sets

```python
s = set()

s.add("alice")
s.remove("alice")       # error if missing
s.discard("alice")      # safe if missing

if "alice" in s:
    ...

len(s)
```

Operations:

```python
a | b       # union
a & b       # intersection
a - b       # difference
a ^ b       # symmetric difference
```

Remove duplicates:

```python
unique = set(arr)
```

## Strings

```python
s = "  hello,world  "

s.strip()               # remove surrounding whitespace
s.lower()
s.upper()

parts = s.split(",")
joined = ",".join(parts)

s.startswith("hello")
s.endswith("world")

s.replace("old", "new")

"abc" in s
```

Useful parsing:

```python
line = "alice,charge,100"

name, action, amount = line.strip().split(",")
amount = int(amount)
```

## Sorting

```python
nums = [3, 1, 2]

sorted(nums)            # new list
nums.sort()             # in place

sorted(nums, reverse=True)
```

Sort tuples:

```python
items = [
    ("alice", 10),
    ("bob", 5),
]

items.sort(key=lambda x: x[1])
```

Multiple keys:

```python
items.sort(key=lambda x: (x[1], x[0]))
```

Descending score, ascending name:

```python
items.sort(key=lambda x: (-x[1], x[0]))
```

Sort dictionaries:

```python
users = [
    {"name": "alice", "score": 10},
    {"name": "bob", "score": 15},
]

users.sort(key=lambda x: (-x["score"], x["name"]))
```

## Tuples

```python
point = (1, 2)

x, y = point

# Useful as dictionary/set keys
seen = set()
seen.add((x, y))
```

## `range`

```python
range(5)          # 0,1,2,3,4
range(2, 5)       # 2,3,4
range(0, 10, 2)   # 0,2,4,6,8

for i in range(5):
    ...
```

Reverse:

```python
for i in range(len(arr) - 1, -1, -1):
    ...
```

## `enumerate` and `zip`

```python
for i, value in enumerate(arr):
    ...
```

```python
names = ["alice", "bob"]
scores = [10, 20]

for name, score in zip(names, scores):
    ...
```

## Min / Max / Sum

```python
min(arr)
max(arr)
sum(arr)
```

With a key:

```python
best = max(users, key=lambda x: x["score"])
```

## Boolean Helpers

```python
all(x > 0 for x in arr)
any(x > 0 for x in arr)
```

## Type Conversion

```python
int("123")
float("3.14")
str(123)

list("abc")        # ['a', 'b', 'c']
set([1, 1, 2])     # {1, 2}
```

## `deque`

Use for queues instead of `list.pop(0)`.

```python
from collections import deque

q = deque()

q.append(1)
q.append(2)

x = q.popleft()

q.appendleft(0)
x = q.pop()
```

## Heap

Useful occasionally, though less Stripe-specific.

```python
import heapq

heap = []

heapq.heappush(heap, 5)
heapq.heappush(heap, 2)

smallest = heapq.heappop(heap)
```

Max heap using negatives:

```python
heapq.heappush(heap, -value)
largest = -heapq.heappop(heap)
```

## JSON

Very useful for practical/API-style problems.

```python
import json

raw = '{"name": "alice", "score": 10}'

data = json.loads(raw)

name = data["name"]
```

Convert Python object to JSON:

```python
raw = json.dumps(data)
```

Reading a JSON file:

```python
with open("data.json") as f:
    data = json.load(f)
```

## Files

```python
with open("file.txt") as f:
    contents = f.read()
```

Line by line:

```python
with open("file.txt") as f:
    for line in f:
        line = line.strip()
```

## Functions

```python
def add(a, b):
    return a + b
```

Default arguments:

```python
def process(items, limit=10):
    ...
```

Multiple returns:

```python
def get_values():
    return 1, 2

a, b = get_values()
```

## Classes

You usually do not need elaborate OOP.

```python
class Transaction:
    def __init__(self, tx_id, amount):
        self.tx_id = tx_id
        self.amount = amount
        self.refunded = False
```

Usage:

```python
tx = Transaction("tx1", 100)

print(tx.amount)
tx.refunded = True
```

## Exceptions

```python
try:
    value = int(raw)
except ValueError:
    value = 0
```

For interviews, avoid wrapping everything in broad `try/except` unless needed.

## Useful Math

```python
abs(x)

round(x, 2)

divmod(10, 3)
# (3, 1)

10 // 3     # 3
10 % 3      # 1
10 / 3      # 3.333...
```

## Infinity

```python
INF = float("inf")

minimum = float("inf")
maximum = float("-inf")
```

## Common Stripe-Style State Pattern

```python
transactions = {}

for raw_event in events:
    parts = raw_event.strip().split(",")

    action = parts[0]
    tx_id = parts[1]

    if action == "charge":
        amount = int(parts[2])

        if tx_id not in transactions:
            transactions[tx_id] = {
                "amount": amount,
                "refunded": 0,
                "disputed": False,
            }

    elif action == "refund":
        amount = int(parts[2])

        if tx_id in transactions:
            tx = transactions[tx_id]

            if tx["refunded"] + amount <= tx["amount"]:
                tx["refunded"] += amount
```

The important idea is:

```text
parse input
→ validate
→ look up state
→ modify state
→ produce output
```

## Useful Helper-Function Pattern

```python
def parse_event(raw):
    parts = raw.strip().split(",")
    return parts


def apply_event(state, event):
    ...


def format_results(state):
    ...
```

This makes progressive Stripe requirements easier to add without rewriting everything.

## Edge Cases to Check Before Submitting

Always ask:

```text
Empty input?
Duplicate IDs?
Missing IDs?
Zero values?
Negative values?
Duplicate operations?
Invalid state transition?
Whitespace?
Ties when sorting?
Correct secondary sort?
Events arriving in unexpected order?
Already-refunded/reversed/disputed item?
```

## Complexity Basics

Common operations:

| Operation | Average |
|---|---:|
| `dict[key]` | O(1) |
| `key in dict` | O(1) |
| `x in set` | O(1) |
| `list.append()` | O(1) |
| `list.pop()` | O(1) |
| `list.pop(0)` | O(n) |
| `x in list` | O(n) |
| `sorted(arr)` | O(n log n) |
| `deque.popleft()` | O(1) |

For Stripe, prioritize **correct, readable code that handles requirements and edge cases** over unnecessary optimization.

## 60-Second Pre-Submit Check

```text
1. Did I read every requirement?
2. Did I accidentally assume IDs always exist?
3. Did I handle duplicates?
4. Is my sorting exactly correct?
5. Are ties handled correctly?
6. Did I mutate state incorrectly?
7. Are numeric types correct?
8. Do empty inputs work?
9. Can later operations reference earlier data?
10. Can I simplify any obviously buggy code without a rewrite?
```
