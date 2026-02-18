# Basic Review

Review these concepts before heading into solving the problem set.

**Concepts Covered:**
- Linux basics
- Python File I/O 
- OS File System Manipulation
- Commonly used core standard libraries
- Common patterns across problem types

## Linux

### 1. File System Structure

| Directory  | Purpose |
|------------|----------|
| `/var/log` | System logs |
| `/etc`     | Configuration files |
| `/tmp`     | Temporary files / storage |
| `/home`    | User home directories |

### 2. Core Commands

| Command | Purpose |
|------------|----------|
| `ls -la` | List all files (including hidden) |
| `cd path/` | Change directory |
| `pwd` | Print working directory |
| `cat file.txt` | View file contents |
| `grep "error" file.txt` | Search text for keyword |
| `wc -l file.txt` | Count lines in file |
| `find . -name "*.log` | Find file ending in ... |

---

## Python File Input/Output

### 1. Basic File Reading
```python
with open(filepath, "r") as file:
    for line in file:
        line = line.strip().split()
```
**Tips:** Always check token count and validate input.

### 2. Basic File Writing
```python
with open(filepath, "w") as file:
    file.write("Hello World\n")
```

**Appending to a file:**
```python
with open(filepath, "a") as ...
```

---

## OS File System Module

### 1. Check File Type
```python
- os.path.isfile(path)
- os.path.isdir(path)
- os.path.islink(path)
```

### 2. Walking through directories
```python
for root, directories, files in os.walk(base_directory):
    for filename in files:
        full_path = os.path.join(root.name)
```

**Path Deletion:** os.remove(path)

---

## Datetime Library Essentials

### 1. Conversion to ISO timestamp
```python
    from datetime import datetime

    dt = datetime.fromisoformat("2026-02-17T10:00:00")

    # to epoch
    ts = int(dt.timestamp())
```

### 2. Computing differences
```python
from datetime import datetime

t1 = datetime(2026, 2, 1, 12, 0)
t2 = datetime(2026, 2, 3, 15, 30)

delta = t2 - t1  # returns a timedelta
```
*Use:*
delta.days = whole days
delta.seconds = leftover seconds within the day
delta.total_seconds() = full difference in seconds

---

## Common Standard Libraries

### 1. collections Module
**Counter**
```python
from collections import Counter

c = Counter()
c['a'] += 1
```

**defaultdict**
```python
from collection import defaultdict

ddict = defaultdict(int) # key is automatically instantiated as an int
d['a'] += 1
```

**deque**
```python
from collections import deque

queue = deque()
queue.append(x)
queue.popleft()
```

### 2. heapq Module
```python
import heapq

heap = []
heapq.heapify(heap)
heapq.heappush(heap, value)
heapq.heappop(heap)
```
*Tip:* If using tuples, heap ordering is by item, left to right

---

## Lambda Function Sort
```python
sorted(items, key=lambda x: (-x[1], x[0]))
# sorts first descending by value at x[1] (assuming numerical)
# then ascending by value at x[0] (by same assumption)
```

---

## Common Patterns in Interviews

### 1. Sliding Window
```python
from collections import deque

sliding_window = deque()
for item in array:
    while sliding_window and sliding_window[0] < (item - window_size):
        sliding_window.pop_left()
    
    sliding_window.append(item)
```

### 2. Interval Merge
```python
intervals.sort()
merged = []
for start, end in intervals:
    # merged[-1][1] finds the last item in merged and uses its second value (end value)
    if not merged or start > merged[-1][1] + 1:
        merged.append([start, end])
    else:
        merged[-1][1] = max(merged[-1][1], end)
```

### 3. Graph BFS
```python
from collections import deque

queue = deque(start)
visited = set(start)
while queue:
    node = queue.popleft()
    for neighbor in graph[node]:
        if neighbor not in visited:
            queue.append(neighbor)
            visited.add(neighbor)
```

---