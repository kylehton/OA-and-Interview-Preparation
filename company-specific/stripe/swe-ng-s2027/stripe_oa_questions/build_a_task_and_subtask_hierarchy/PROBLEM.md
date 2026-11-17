
# Build a Task and Subtask Hierarchy — Tasks 1, 2, and 2b

**Company:** Stripe  
**Difficulty:** Medium  
**Roles:** Full-Time, New Grad, Intern  
**Interview Stage:** Phone Screen  
**Status:** Solved  
**Topics:** String Parsing, Hierarchical Data, Sorting, Tree Traversal, Output Formatting

---

## Problem Statement

Build and print a task hierarchy from unordered task and subtask records.

The problem is divided into three stages:

1. **Task 1:** Build the task hierarchy.
2. **Task 2:** Print subtasks using branch markers.
3. **Task 2b:** Change the marker of each task's last child.

Only the final Task 2b output is judged.

In the original reported interview, candidates were not given a function stub. They had to read standard input until EOF and parse each input line themselves.

For this practice version, the input is provided as an array of strings called `lines`, where each string represents an input line with its line ending removed.

---

## Input Format

The input contains unordered task and subtask records with comma-separated fields.

### Task Record

```text
date,task,taskId,name
```

Fields:

| Field | Description |
|---|---|
| `date` | Task date in YYYY-MM-DD format |
| `task` | Record type identifier |
| `taskId` | Unique task identifier |
| `name` | Task name |

### Subtask Record

```text
date,subtask,subtaskId,parentTaskId,name
```

Fields:

| Field | Description |
|---|---|
| `date` | Subtask date in YYYY-MM-DD format |
| `subtask` | Record type identifier |
| `subtaskId` | Unique subtask identifier |
| `parentTaskId` | ID of the parent task |
| `name` | Subtask name |

### Parsing Rules

- Split each input line using commas only.
- Do not trim field values.
- Do not split on spaces because names can contain spaces.
- The second field determines whether the record is a task or subtask.
- Input records may appear in any order.
- A subtask may appear before its parent task.
- Read all input records before producing output.

---

## Task 1 — Build the Hierarchy

Separate task records from subtask records.

Group each subtask under the task whose `taskId` matches its `parentTaskId`.

The hierarchy contains only two levels:

- Parent tasks
- Direct subtasks

There are no nested subtasks.

### Sorting Requirements

**Tasks:**

Sort tasks by:

```text
(date, taskId)
```

**Subtasks:**

For each parent task, sort its subtasks by:

```text
(date, subtaskId)
```

### Comparison Rules

- Compare dates as plain strings.
- Compare task IDs and subtask IDs as plain strings.
- String comparisons are lexicographical (character by character).
- Do not interpret numeric characters in IDs as numerical values.

For example:

```text
t10 comes before t2
```

This is because the character `1` comes before `2`.

---

## Task 2 — Print Each Child With a Branch Marker

Print each task's name on its own line, followed by the names of its direct subtasks.

Every subtask must be prefixed with:

```text
|- 
```

This prefix consists of:

- A vertical bar (`|`)
- A hyphen (`-`)
- One space

### Output Rules

- Print task names without any prefix.
- Print each subtask immediately after its parent.
- Print only names.
- Do not include IDs or dates.
- Do not add indentation.
- Do not insert blank lines.

### Example

```text
build
|- code
|- review
ship
```

---

## Task 2b — Mark the Last Child

Extend Task 2 by changing the branch marker of each task's final subtask.

After sorting the subtasks, use:

**Non-final subtasks:**

```text
|- 
```

**Final subtask:**

```text
\- 
```

The final-subtask prefix consists of:

- A backslash (`\`)
- A hyphen (`-`)
- One space

### Requirements

1. All subtasks except the final child use `|- `.
2. The final child uses `\- `.
3. A task with exactly one subtask uses `\- ` for that subtask.
4. A task with no subtasks prints only its name.
5. Parent task names never receive branch markers.
6. Determine the last subtask after sorting.
7. Return the Task 2b output as an array containing one string per printed line.

### Example

```text
build
|- code
\- review
ship
```

---

## Function Signature

```text
printTaskHierarchy(lines: String[]) → String[]
```

### Input

**`lines`**

An array of strings representing task and subtask records.

Each string contains one comma-separated record.

### Output

A `String[]` containing the final Task 2b hierarchy.

Each element corresponds to exactly one printed line.

---

## Examples

### Example 1

**Input:**

```python
lines = [
    "2026-01-03,subtask,s2,t1,review",
    "2026-01-02,task,t2,ship",
    "2026-01-01,task,t1,build",
    "2026-01-02,subtask,s1,t1,code"
]
```

**Expected Output:**

```python
[
    "build",
    "|- code",
    "\\- review",
    "ship"
]
```

**Rendered Output:**

```text
build
|- code
\- review
ship
```

**Explanation:**

1. Task `build` has date `2026-01-01`.
2. Task `ship` has date `2026-01-02`.
3. Therefore, `build` prints before `ship`.
4. Under `build`, subtask `code` has date `2026-01-02`.
5. Subtask `review` has date `2026-01-03`.
6. Therefore, `code` prints before `review`.
7. `review` is the final child and uses `\- `.
8. `ship` has no subtasks and prints only its name.

### Example 2

**Input:**

```python
lines = [
    "2026-02-01,task,b,Beta",
    "2026-02-01,subtask,x2,a,write tests",
    "2026-02-01,task,a,Alpha",
    "2026-02-01,subtask,x1,a,draft spec",
    "2026-02-03,subtask,y1,b,deploy"
]
```

**Expected Output:**

```python
[
    "Alpha",
    "|- draft spec",
    "\\- write tests",
    "Beta",
    "\\- deploy"
]
```

**Rendered Output:**

```text
Alpha
|- draft spec
\- write tests
Beta
\- deploy
```

**Explanation:**

1. Both `Alpha` and `Beta` have date `2026-02-01`.
2. Their IDs are compared lexicographically.
3. Task ID `a` comes before `b`, so `Alpha` prints first.
4. Alpha's subtasks `draft spec` and `write tests` share the same date.
5. Their IDs are `x1` and `x2`, respectively.
6. `x1` comes before `x2`, so `draft spec` prints first.
7. `write tests` is Alpha's final child and uses `\- `.
8. Beta has exactly one subtask, `deploy`, which also uses `\- `.

---

## Rehearse the Standard Input Setup

The original reported interview required candidates to read input directly from standard input until EOF.

To reproduce that environment:

1. Create a standalone program.
2. Read from `sys.stdin` line by line, or repeatedly call `input()` until `EOFError`.
3. Remove only the line ending from each input line.
4. Parse the records.
5. Build and format the hierarchy.
6. Print every returned output line.

The FastPrep editorial includes a complete Python implementation of this setup.

**Note:** The judged practice version provides `lines` directly and does not require standard input handling.

---

## Constraints

1. `0 <= lines.length <= 200`.
2. Each line has exactly one of the two supported comma-separated record formats.
3. The second field is exactly `task` or `subtask`.
4. Dates use zero-padded `YYYY-MM-DD` format.
5. All task IDs and subtask IDs are unique.
6. Every `parentTaskId` refers to an existing task in `lines`.
7. IDs contain between 1 and 20 characters.
8. IDs contain only letters, digits, hyphens, or underscores.
9. Names contain between 1 and 50 characters.
10. Names contain only letters, digits, spaces, hyphens, or underscores.
11. Names do not begin or end with a space.
12. No field contains a comma.
13. Only direct task-to-subtask relationships exist.
14. Subtasks cannot contain nested subtasks.
