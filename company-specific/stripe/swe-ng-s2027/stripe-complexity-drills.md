# Stripe Interview: Code Complexity Drills

22 practical, Stripe-flavored snippets (payments, ledgers, webhooks, fraud, rate limiting). Each is a realistic chunk of code you might write in the interview. Your job is to read it and give the full spoken answer.

## How to use this

For every problem, say out loud (or write) the answer exactly as you would to an interviewer:

1. **Define your variables.** "Let n be the number of entries, a the number of distinct accounts..." Never say "n" without saying what it is.
2. **Time complexity**, and whether it is worst case, average, or amortized.
3. **Space complexity**, including the output and the recursion stack.
4. **What dominates**, and one sentence on how you would improve it.

Then check the **Answer Key** at the bottom. Aim for about 2 to 3 minutes per problem. All code is Python.

**Watch for these traps:** hidden O(n) operations (slicing, `insert`, `in` on a list, string concatenation), amortized vs worst case, output size counting toward space, recursion depth, and distinct-key counts that differ from n.

---

## Problems

### Problem 1: Net balances
```python
def net_balances(entries):
    """entries: list of (account_id, amount_cents)"""
    totals = {}
    for account, amount in entries:
        totals[account] = totals.get(account, 0) + amount
    nonzero = {acct: bal for acct, bal in totals.items() if bal != 0}
    return sorted(nonzero.items(), key=lambda kv: kv[1])
```

### Problem 2: Duplicate charge detection
```python
from collections import defaultdict

def find_duplicates(charges, window):
    """charges: list of (timestamp, customer_id, amount)"""
    by_key = defaultdict(list)
    for ts, cust, amt in charges:
        by_key[(cust, amt)].append(ts)

    dups = []
    for key, times in by_key.items():
        times.sort()
        for i in range(1, len(times)):
            if times[i] - times[i - 1] <= window:
                dups.append((key, times[i - 1], times[i]))
    return dups
```

### Problem 3: Sliding-window rate limiter
```python
from collections import defaultdict, deque

class RateLimiter:
    def __init__(self, limit, window):
        self.limit = limit
        self.window = window
        self.hits = defaultdict(deque)

    def allow(self, user, now):
        q = self.hits[user]
        while q and q[0] <= now - self.window:
            q.popleft()
        if len(q) < self.limit:
            q.append(now)
            return True
        return False
```
Give the cost of one `allow()` call (worst case and amortized) and the total space for U users.

### Problem 4: Batch processing a queue
```python
def process_all(items, batch_size, handler):
    """handler(batch) is O(len(batch)) and returns a list the same length."""
    results = []
    while items:
        batch = items[:batch_size]
        items = items[batch_size:]
        results.extend(handler(batch))
    return results
```
Let n = len(items), b = batch_size. How would you fix it?

### Problem 5: Minimum payouts to reach an amount
```python
from functools import lru_cache

def min_payouts(amount, denominations):
    @lru_cache(maxsize=None)
    def solve(remaining):
        if remaining == 0:
            return 0
        best = float("inf")
        for d in denominations:
            if d <= remaining:
                best = min(best, 1 + solve(remaining - d))
        return best

    return solve(amount)
```
Let A = amount, D = len(denominations). Is there anything worrying if A is in cents?

### Problem 6: Currency conversion
```python
from collections import defaultdict, deque

def convert(rates, src, dst, amount):
    """rates: list of (from_ccy, to_ccy, rate)"""
    graph = defaultdict(list)
    for a, b, r in rates:
        graph[a].append((b, r))
        graph[b].append((a, 1 / r))

    queue = deque([(src, amount)])
    seen = {src}
    while queue:
        cur, val = queue.popleft()
        if cur == dst:
            return val
        for nxt, r in graph[cur]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, val * r))
    return None
```
If this function is called Q times with the same `rates`, what is the total cost and what would you change?

### Problem 7: Payment pipeline ordering
```python
from collections import defaultdict

def run_order(steps, deps):
    """steps: list of names; deps: dict step -> list of prerequisite steps"""
    indegree = {s: 0 for s in steps}
    children = defaultdict(list)
    for step, prereqs in deps.items():
        for p in prereqs:
            children[p].append(step)
            indegree[step] += 1

    ready = [s for s in steps if indegree[s] == 0]
    order = []
    while ready:
        s = ready.pop()
        order.append(s)
        for c in children[s]:
            indegree[c] -= 1
            if indegree[c] == 0:
                ready.append(c)

    if len(order) != len(steps):
        raise ValueError("cycle detected")
    return order
```

### Problem 8: Top-K merchants by volume
```python
import heapq
from collections import Counter

def top_merchants(payments, k):
    """payments: list of (merchant_id, amount)"""
    volume = Counter()
    for merchant, amount in payments:
        volume[merchant] += amount

    heap = []
    for merchant, total in volume.items():
        heapq.heappush(heap, (total, merchant))
        if len(heap) > k:
            heapq.heappop(heap)
    return sorted(heap, reverse=True)
```
Let n = number of payments, m = number of distinct merchants.

### Problem 9: Webhook delivery with backoff
```python
import time

def deliver_webhook(event, send, max_retries=8, base=1):
    for attempt in range(max_retries):
        if send(event):
            return True
        time.sleep(base * 2 ** attempt)
    return False
```
Let R = max_retries. Give the CPU time, the number of `send` calls, and the worst-case wall-clock time. What changes if this is called in a loop for N events?

### Problem 10: Flatten a nested config
```python
def flatten(obj, prefix=""):
    out = {}
    for key, val in obj.items():
        path = prefix + "." + key if prefix else key
        if isinstance(val, dict):
            out.update(flatten(val, path))
        else:
            out[path] = val
    return out
```
Let L = number of leaf values, d = max nesting depth, k = average key length. Be precise about the hidden costs.

### Problem 11: Ledger reconciliation
```python
def reconcile(ours, theirs):
    """each: list of (txn_id, amount)"""
    ours_map = dict(ours)
    theirs_map = dict(theirs)

    missing = [t for t in ours_map if t not in theirs_map]
    extra = [t for t in theirs_map if t not in ours_map]
    mismatched = [
        t for t in ours_map
        if t in theirs_map and ours_map[t] != theirs_map[t]
    ]
    return sorted(missing), sorted(extra), sorted(mismatched)
```
Let n = len(ours), m = len(theirs).

### Problem 12: Card BIN lookup
```python
class BinTrie:
    def __init__(self):
        self.root = {}

    def add(self, prefix, brand):
        node = self.root
        for ch in prefix:
            node = node.setdefault(ch, {})
        node["$"] = brand

    def lookup(self, card_number):
        node, brand = self.root, None
        for ch in card_number:
            if ch not in node:
                break
            node = node[ch]
            if "$" in node:
                brand = node["$"]
        return brand
```
Let P = number of prefixes, L = average prefix length, c = length of the card number. Give the cost of `add`, `lookup`, and total build.

### Problem 13: Idempotency key cache
```python
from collections import OrderedDict

class IdempotencyCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.store = OrderedDict()

    def get(self, key):
        if key not in self.store:
            return None
        self.store.move_to_end(key)
        return self.store[key]

    def put(self, key, response):
        self.store[key] = response
        self.store.move_to_end(key)
        if len(self.store) > self.cap:
            self.store.popitem(last=False)
```

### Problem 14: Time-ordered ledger
```python
import bisect

class SortedLedger:
    def __init__(self):
        self.times = []
        self.entries = []

    def add(self, ts, entry):
        i = bisect.bisect_right(self.times, ts)
        self.times.insert(i, ts)
        self.entries.insert(i, entry)

    def between(self, lo, hi):
        i = bisect.bisect_left(self.times, lo)
        j = bisect.bisect_right(self.times, hi)
        return self.entries[i:j]
```
Give the cost of `add`, `between` (r results), and of calling `add` n times. Someone says "it uses binary search, so it's O(log n)". Are they right?

### Problem 15: Longest spend window within budget
```python
def longest_within_budget(daily_spend, budget):
    """daily_spend: list of non-negative ints"""
    best = left = 0
    total = 0
    for right, spend in enumerate(daily_spend):
        total += spend
        while total > budget:
            total -= daily_spend[left]
            left += 1
        best = max(best, right - left + 1)
    return best
```
There is a `while` inside a `for`. Justify your answer.

### Problem 16: Card velocity alerts
```python
def velocity_alerts(txns, window, max_count):
    """txns: list of (timestamp, card_id), sorted by timestamp"""
    alerts = []
    n = len(txns)
    for i in range(n):
        count = 1
        for j in range(i + 1, n):
            if txns[j][0] - txns[i][0] > window:
                break
            if txns[j][1] == txns[i][1]:
                count += 1
        if count >= max_count:
            alerts.append(txns[i])
    return alerts
```
The inner loop has an early `break`. Is this O(n)? Define what the real cost depends on, give best and worst case, and say how you'd rewrite it.

### Problem 17: Invoice combinations
```python
def invoice_combos(invoices, target):
    """invoices: list of positive ints. Find all subsets summing to target."""
    results = []

    def backtrack(start, path, total):
        if total == target:
            results.append(path[:])
            return
        if total > target:
            return
        for i in range(start, len(invoices)):
            path.append(invoices[i])
            backtrack(i + 1, path, total + invoices[i])
            path.pop()

    backtrack(0, [], 0)
    return results
```
Let n = len(invoices). Does the `total > target` pruning change the worst-case bound?

### Problem 18: Paginated API: list vs generator
```python
def fetch_all_charges(client):
    charges, cursor = [], None
    while True:
        page = client.list(limit=100, starting_after=cursor)
        charges.extend(page.data)
        if not page.has_more:
            break
        cursor = page.data[-1].id
    return charges

def stream_charges(client):
    cursor = None
    while True:
        page = client.list(limit=100, starting_after=cursor)
        yield from page.data
        if not page.has_more:
            break
        cursor = page.data[-1].id
```
Let n = total charges, p = page size. Compare the two on time, space, and number of API calls.

### Problem 19: Fraud ring detection
```python
from collections import defaultdict

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path halving
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)

def fraud_rings(logins):
    """logins: list of (account_id, device_id)"""
    uf = UnionFind()
    for account, device in logins:
        uf.union("a:" + account, "d:" + device)

    groups = defaultdict(set)
    for account, _ in logins:
        groups[uf.find("a:" + account)].add(account)
    return [g for g in groups.values() if len(g) > 1]
```
Let n = len(logins). Careful: this uses path halving but no union by rank or size. Be precise about the bound.

### Problem 20: Worst endpoints by error rate
```python
from collections import defaultdict

def worst_endpoints(lines, k):
    """each line: 'timestamp method path status'"""
    stats = defaultdict(lambda: [0, 0])
    for line in lines:
        parts = line.split()
        path, status = parts[2], int(parts[3])
        stats[path][0] += 1
        if status >= 500:
            stats[path][1] += 1

    rates = [(errs / total, path) for path, (total, errs) in stats.items()]
    rates.sort(reverse=True)
    return rates[:k]
```
Let N = number of lines, L = average line length, E = number of distinct endpoints.

### Problem 21: Job retry scheduler
```python
import heapq

def run_scheduler(jobs, execute, max_attempts):
    """jobs: list of (run_at, job_id)"""
    heap = [(t, j, 1) for t, j in jobs]
    heapq.heapify(heap)
    done, failed = [], []

    while heap:
        run_at, job_id, attempt = heapq.heappop(heap)
        if execute(job_id):
            done.append(job_id)
        elif attempt < max_attempts:
            heapq.heappush(heap, (run_at + 2 ** attempt, job_id, attempt + 1))
        else:
            failed.append(job_id)
    return done, failed
```
Let n = len(jobs), R = max_attempts. Treat `execute` as O(1).

### Problem 22: Payout batching
```python
def batch_payouts(payouts, batch_limit):
    """payouts: list of (payout_id, amount), each amount <= batch_limit"""
    batches = []  # each: [total, [ids]]
    for payout_id, amount in sorted(payouts, key=lambda p: -p[1]):
        for batch in batches:
            if batch[0] + amount <= batch_limit:
                batch[0] += amount
                batch[1].append(payout_id)
                break
        else:
            batches.append([amount, [payout_id]])
    return batches
```
Let n = len(payouts), b = number of batches produced. Give the worst case and say how you'd speed it up.

---

## Answer Key

Each answer is written the way you would say it in the interview: variables, time, space, then the key insight or improvement.

**1. Net balances.** Time O(n + a log a), space O(a), where a = distinct accounts. The loop is O(n) with O(1) dict operations; the sort is over at most a items. Worst case a = n gives O(n log n). Note that a can be much smaller than n, so say it.

**2. Duplicate charges.** Time O(n log n), space O(n). Grouping is O(n). Sorting each group costs O(g log g), and since the group sizes sum to n the total is at most O(n log n) (worst case: everything in one group). Space is the grouped lists plus the output, both O(n). Improvement: if input is already time-sorted, groups stay sorted and you get O(n).

**3. Rate limiter.** `allow()` is **amortized O(1)**: each timestamp is appended once and popped at most once. A single call can be O(limit) in the worst case if a burst expires at once. Space is O(U · limit) for U active users, since each deque holds at most `limit` timestamps (it only appends when len < limit). If you only need approximate limits, a fixed-window counter is O(1) per user.

**4. Batch processing.** Time **O(n² / b)**, not O(n). Iteration i slices and copies the remaining list, roughly n − i·b elements, over n/b iterations. The handler work adds O(n) total, which is dominated. Space O(n) (the copies are freed each loop, but results are O(n)). Fix: iterate with an index, `for i in range(0, n, b): handler(items[i:i+b])`, which is O(n) time. The same trap applies to `list.pop(0)` and string `+=` in a loop.

**5. Min payouts (memoized DP).** Time O(A · D), space O(A). There are A + 1 distinct subproblems, each doing D work. The cache is O(A) and the recursion stack can reach A / min(denomination) deep. This is **pseudo-polynomial**: it is polynomial in the *value* of A, not its bit length. In cents, A can be 10^7 or more, which means a huge cache and likely a Python recursion-limit crash. Fix: iterative bottom-up DP, or a greedy approach if the denominations are canonical.

**6. Currency BFS.** Time O(V + E), space O(V + E), where V = currencies and E = len(rates). Building the graph is O(E); BFS visits each node once and each edge at most twice (undirected). For Q queries, rebuilding the graph each time costs O(Q · (V + E)). Build the graph once, or precompute all-pairs with Floyd-Warshall O(V³) if V is small. Also mention: BFS finds *a* path, and in a consistent rate graph all paths agree.

**7. Topological sort (Kahn's).** Time O(V + E), space O(V + E), where V = steps and E = total dependency edges. Each node is pushed and popped once, and each edge is relaxed once. The `len(order) != len(steps)` check detects cycles.

**8. Top-K merchants.** Time **O(n + m log k)** (plus O(k log k) for the final sort), space O(m + k). The Counter pass is O(n). The heap stays at size k, so each of the m pushes costs O(log k). Compared to sorting all merchants, O(m log m), this wins when k is much smaller than m. Space is dominated by the Counter, O(m).

**9. Webhook backoff.** CPU time and calls to `send`: O(R) per event, O(1) extra space. But wall-clock sleep is base · (2^R − 1), which is **exponential in R**. With R = 8 and base = 1s that is 255 seconds for one dead endpoint. Called sequentially for N events it blocks for up to O(N · base · 2^R). Fix: schedule retries asynchronously (a delay queue) instead of sleeping, and add jitter and a cap on the delay. This distinguishes compute complexity from latency.

**10. Flatten.** Roughly O(L · d · k) time and O(L · d · k) space for the output, plus O(d) recursion stack. Two hidden costs: (1) each leaf's path string is built through d concatenations, so its length is up to d · k; (2) `out.update(child)` re-copies every leaf into every ancestor's dict, so each leaf is copied up to d times. Fix: pass a single shared `out` dict down the recursion and append only at leaves, which removes the repeated copying (strings remain O(d · k) each).

**11. Reconciliation.** Time O((n + m) log(n + m)), space O(n + m). Building the maps and the three comprehensions are O(n + m) with O(1) lookups. The three `sorted()` calls dominate (the result lists are bounded by n + m). If sorted output isn't required, it is **linear**, O(n + m). Mention that `dict(ours)` keeps only the last amount for duplicate txn ids, a correctness note worth raising.

**12. BIN trie.** `add` is O(L). Total build is O(P · L), and space is O(P · L) worst case (less with shared prefixes). `lookup` is O(min(c, max prefix length)), which is effectively constant for card numbers (about 6 to 8 digits for BINs) and **independent of P**. The point to make: lookup cost does not grow with the number of prefixes, unlike scanning a list of prefixes, which would be O(P · L).

**13. Idempotency LRU cache.** `get` and `put` are both O(1) average (hash lookup, linked-list move). Space O(capacity), plus the size of the stored responses. Strictly, hashing a key costs O(K) for key length K, which is fine to mention. Note that this is single-process and not thread-safe; in production you'd back it with Redis plus TTLs.

**14. Sorted ledger.** `add` is **O(n)**, not O(log n): `bisect` is O(log n) but `list.insert` shifts elements, so each insert is O(n). n adds cost O(n²) worst case (fast in practice because of memmove, but still quadratic). `between` is O(log n + r). Space O(n). The person is wrong about add. Fixes: a balanced tree or `sortedcontainers.SortedList` (O(log n) insert), or if writes are batched, append and sort once, O(n log n).

**15. Longest window within budget.** Time **O(n)**, space O(1). The nested loop is a trap: `left` only moves forward and never exceeds n, so across the entire run the inner loop executes at most n times. Each element enters the window once and leaves once, so total work is 2n. This is amortized analysis (aggregate method). It requires non-negative values; with negatives the shrink logic is invalid.

**16. Velocity alerts.** Time O(n · w), where w is the max number of transactions inside any single time window. Best case O(n) (sparse data), **worst case O(n²)** (all transactions inside one window, so the `break` never fires). Space O(a), where a is the number of alerts, at most n. Rewrite: group by card with a dict, then run a two-pointer sliding window per card, giving O(n) overall (O(n log n) if you must sort first). Better algorithm plus honest worst case is the strong answer.

**17. Invoice combinations.** Time **O(2^n · n)**, space O(n) for recursion and path, plus O(output). There are up to 2^n subsets, and each valid one costs O(n) to copy. The `total > target` pruning cuts real work but **not the worst case**: with a huge target, nothing is ever pruned. Output itself can be O(2^n · n). Improvement: sort first and `break` instead of `return`, or use DP if you only need a count or existence (O(n · target)).

**18. List vs generator.** Both: O(n) time, n / p API calls. Space: `fetch_all_charges` is **O(n)** (it holds everything); `stream_charges` is **O(p)** (one page at a time). The generator also gives lazy evaluation, so a consumer can stop early and save API calls. The tradeoff: a list allows re-iteration and random access, and a generator can only be consumed once.

**19. Union-Find fraud rings.** Time: path halving alone gives **O(log n) amortized per operation**, so O(n log n) total. Adding union by rank or size would give the famous O(n · α(n)), effectively O(n). Space O(n) for the parent map and groups. The final grouping loop is another O(n) finds. A good interview answer says: "practically near-linear, strictly O(n log n) as written, and union by size gets it to inverse-Ackermann."

**20. Endpoint error rates.** Time O(N · L + E log E), space O(E) plus O(L) per line transiently. `line.split()` is O(L) per line, so parsing is O(N · L), not O(N). The sort is over E endpoints. Improvement: `heapq.nlargest(k, ...)` gives O(E log k) for the ranking step. Also mention a correctness issue: an endpoint with one request and one error has rate 1.0 and outranks a high-traffic failing one, so you may want a minimum-volume threshold.

**21. Retry scheduler.** Time **O(n · R · log n)** worst case, space O(n). `heapify` is O(n). Each job is pushed and popped at most R times, so there are at most n · R heap operations, each O(log n). The heap never holds more than n entries because each job has at most one live entry, so the log factor is log n, not log(n · R). Space is O(n) for the heap plus the done and failed lists. This is also a reasonable model for a delayed-job system; the production version swaps in a persistent queue.

**22. Payout batching.** Time **O(n log n + n · b)**, worst case O(n²) when b grows to about n (e.g. every payout is more than half the limit, so every payout opens a new batch and scans all existing ones). Space O(n). Sorting is the O(n log n) part; the inner scan is the quadratic part. Improvement: keep batches in a structure that supports "find first batch with enough remaining capacity", such as a segment tree (O(n log n) total), or a heap/sorted structure for best-fit. Sorting descending is the classic first-fit-decreasing heuristic, which is near-optimal but not exact (bin packing is NP-hard).

---

## Quick Reference: Complexity Cheat Sheet

Operations that look O(1) but are not, in Python:

| Operation | Real cost |
|---|---|
| `lst[a:b]`, `lst[:]` | O(b − a) copy |
| `lst.insert(i, x)`, `lst.pop(0)` | O(n) |
| `x in lst` | O(n) |
| `x in set` / `x in dict` | O(1) average, O(n) worst |
| `s1 + s2`, `s += c` in a loop | O(len) per op, O(n²) over a loop |
| `sorted(...)`, `.sort()` | O(n log n) time, O(n) space (Timsort) |
| `heappush`, `heappop` | O(log n) |
| `heapify` | O(n) |
| `deque.popleft()`, `append()` | O(1) |
| `dict.update(other)` | O(len(other)) |
| `str.split()`, `join` | O(length of string) |
| `bisect.bisect_*` | O(log n) |
| `bisect.insort` | O(n) (shifting) |

**Stripe-style narration template:**

> Let n be `<what n is>`. The main loop is O(`<cost>`) because `<reason>`. The dominant cost is `<operation>`, so time is O(`<time>`) and space is O(`<space>`), mostly from `<source>`. In the worst case `<worst case>`. If this became a bottleneck, I would `<improvement>`.
