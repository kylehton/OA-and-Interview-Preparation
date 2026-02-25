# Okta SRE Intern Technical Prep

This repository is a structured, intensive preparation set for a mixed-format SRE technical interview.

The target interview format:
- ~45 minutes live coding
- Combination of:
  - Practical coding (log parsing, file I/O, REST-like logic)
  - Data structures and algorithms
  - Object-oriented design
  - Systems reasoning
- Remaining time: behavioral + Q&A

This problem set simulates that environment as closely as possible.

---

# Prep Design Brief

Topics and concepts:
- Streaming file processing
- Robust parsing (handling malformed input)
- Error-rate and SLO logic
- Sliding windows
- Heaps and sorting
- Graph traversal
- OOP design
- REST-style pagination
- Rate limiting
- Retry logic
- OS file manipulation
- Thread safety

Every problem:
- Has a detailed specification
- Requires defensive programming
- Includes edge-case-heavy pytest coverage
- Is designed for ~30–45 minutes of work

---

# Problem Set Concept Coverage

P01 — Log Error Rate Aggregator

**Concepts:**
Streaming file I/O, defensive parsing, dictionary aggregation, floating-point rounding, sorting with multi-key rules.
Why it matters: Simulates real-world service error tracking and log-based reliability metrics.

P02 — Top-K IPs

**Concepts:**
Frequency counting, heap usage (heapq), tie-breaking sorting rules, memory-efficient streaming.
Why it matters: Tests your ability to compute top-K efficiently without full in-memory sorting.

P03 — Rolling SLO Breach Detector

**Concepts:**
Sliding window algorithm, deque usage, timestamp parsing (datetime), rolling metrics, strict inequality logic.
Why it matters: Directly mirrors SRE-style SLO monitoring and alerting systems.

P04 — REST Pagination + Deduplication

**Concepts:**
Iterative API traversal, cycle detection, deduplication using sets, order preservation, defensive API handling.
Why it matters: Models real-world REST client logic and production pagination bugs.

P05 — Rate Limiter (OOP)

**Concepts:**
Sliding window logic, amortized O(1) operations, timestamp math, queue/deque management, stateful object design.
Why it matters: Classic SRE infrastructure logic (rate limiting, request throttling).

P06 — Retry with Exponential Backoff

**Concepts:**
Exception handling, retry loops, exponential growth patterns, injected dependencies (sleep_fn), jitter logic.
Why it matters: Real-world distributed system reliability pattern.

P07 — Dependency Outage Graph

**Concepts:**
Graph construction from file input, reverse dependency traversal (BFS/DFS), cycle detection (DFS coloring or visited sets).
Why it matters: Models service dependency graphs and blast-radius reasoning.

P08 — P95 Latency

**Concepts:**
Percentile calculation (nearest-rank method), sorting logic, grouping by key, heap optimization discussion.
Why it matters: Common reliability metric computation in monitoring systems.

P09 — Merge Downtime Intervals

**Concepts:**
Interval sorting and merging, edge case handling (adjacent intervals), per-key grouping.
Why it matters: Models downtime aggregation and incident window consolidation.

P10 — Streaming Unique Users

**Concepts:**
Memory-aware streaming, set usage, frequency counting, top-K with custom sorting.
Why it matters: Tests handling large event streams efficiently.

P11 — File Cleanup (OS + Datetime)

**Concepts:**
os.walk, file metadata (os.stat), epoch timestamp math, recursive traversal, safe deletion logic.
Why it matters: Practical SRE scripting + Linux familiarity.

P12 — Service Monitor (OOP + Thread Safety)

**Concepts:**
Encapsulation, internal state management, multi-criteria sorting, rounding consistency, thread synchronization (locks).
Why it matters: Simulates production monitoring components and concurrency awareness.

P13 — HTTP Route Normalization

**Concepts:**
String parsing, path normalization, pattern detection (numeric segments), HTTP status bucketing, aggregation.
Why it matters: Realistic API analytics processing task.

P14 — API Rate Limit Simulation
**Concepts:**
Multi-file joins, timestamp arithmetic, deduplication rules, stable sorting, stateful simulation.
Why it matters: Combines REST reasoning with log-based event scheduling.


Each problem folder contains:
- `README.md` — full problem description
- `solution.py` — starter implementation
- `tests/` — comprehensive pytest suite

---

# How To Use This Repo (Strict Interview Mode)

### 1. Pick One Problem

Choose a single problem.
Do **not** open tests first.

### 2. Simulate Interview Conditions

- Set a timer: 30–45 minutes
- No AI
- No looking at tests until done
- Think out loud (literally, if possible)
- Discuss:
  - Edge cases
  - Time complexity
  - Space complexity
  - Tradeoffs

### 3. Run Tests

pytest -q

---

# 1 Week Preparation Plan

## Day 1–2
- P01
- P02
- P05
- P03

## Day 3–4
- P04
- P06
- P07

## Day 5
- P08
- P09

## Day 6
- P10
- P11

## Day 7
- P12
- P13
- P14
- Full mock combining two problems back-to-back

---

# Core Skills Being Tested

## File I/O
- Streaming large files
- Handling malformed lines
- Multiple file joins
- Defensive parsing

## Data Structures
- Hash maps
- Heaps
- Sliding windows
- Deques
- Graph traversal
- Interval merging

## Systems Thinking
- Rolling SLO breach detection
- Rate limiting logic
- Retry with exponential backoff
- Deduplication across pagination
- Cycle detection in graphs

## OOP
- Encapsulation
- State management
- Sorting logic
- Thread safety

## OS / Linux
- os.walk
- File mtimes
- Recursive traversal
- Safe deletion

---

# Interview Simulation Tips

1. Clarify input format before coding.
2. Ask about edge cases:
   - Empty file?
   - Invalid lines?
   - Duplicate IDs?
3. State complexity.
4. Write clean, readable code.
5. Avoid overengineering.
6. Mention production considerations:
   - Streaming vs loading whole file
   - Memory footprint
   - Fault tolerance
   - Defensive parsing

---

# Behavioral Prep Themes (SRE-Specific)

Be ready to discuss:

- A time you debugged a production issue
- A time you automated something repetitive
- Handling ambiguity
- Learning something quickly under pressure
- Improving reliability
- Incident ownership
- Tradeoffs between speed and safety

---

## **Notes After Completion:**

### Review: p06, p07, p09

p06: Had difficulty with getting different errors, need to remember all non exit errors fall under exceptions, so use try-catch

p07: Need to review DFS/BFS. Had difficulty with has_cycle function

p09: Took a while to get a working solution with interval merging. Need to review algorithm and get better and problem splitting
to make the problem easier to track progress and solve
