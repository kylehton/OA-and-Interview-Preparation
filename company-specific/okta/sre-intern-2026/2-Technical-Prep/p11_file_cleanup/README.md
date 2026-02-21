# P11 — File Cleanup (os/path + datetime + Safety)

Implement utilities to find and optionally delete old files.

---

## Task 1 — List Old Files

Implement:

```python
list_old_files(root_dir: str, older_than_days: int, now_ts: float | None = None) -> list[str]
```

### Rules

- Recursively walk `root_dir` using `os.walk`
- Include **only regular files**
  - Ignore directories
  - Ignore symlinks
- A file is "old" if:

  ```
  (now_ts - mtime) > older_than_days * 86400
  ```

- If `now_ts` is provided, use it
- Otherwise use `time.time()`
- Return **absolute paths**
- Return sorted lexicographically

---

## Example Runthrough

**Input:**
```python
# assume:
# now_ts = 1_000_000
# older_than_days = 1
# 1 day = 86400 seconds

# file mtimes:
# /tmp/a.txt -> 900_000      (100_000 seconds old)
# /tmp/b.txt -> 999_000      (1_000 seconds old)
# /tmp/sub/c.txt -> 800_000  (200_000 seconds old)

root_dir = "/tmp"
older_than_days = 1
now_ts = 1_000_000
```

**Output:**
```python
[
  "/tmp/a.txt",
  "/tmp/sub/c.txt"
]
# threshold = 86400 seconds
# a.txt age = 100_000 > 86400 → included
# b.txt age = 1_000 → excluded
# c.txt age = 200_000 > 86400 → included
# sorted lexicographically
```

---

## Task 2 — Delete Old Files

Implement:

```python
delete_old_files(
    root_dir: str,
    older_than_days: int,
    dry_run: bool = True,
    now_ts: float | None = None
) -> list[str]
```

### Rules

- Identify the same files as `list_old_files`
- If `dry_run=True`:
  - Do NOT delete
  - Just return the list
- If `dry_run=False`:
  - Delete the files
- Return list of affected files (sorted)

---

## Example Runthrough (Delete)

**Input:**
```python
root_dir = "/tmp"
older_than_days = 1
dry_run = False
now_ts = 1_000_000
```

**Output:**
```python
[
  "/tmp/a.txt",
  "/tmp/sub/c.txt"
]
# same files identified as old
# deleted because dry_run=False
```

---

## Notes

- Use `os.path.abspath()` to ensure absolute paths.
- Use `os.path.isfile()` and check `not os.path.islink()`.
- Always compute:

  ```
  threshold_seconds = older_than_days * 86400
  ```

- Must be testable:
  - Use `now_ts` when provided
  - Only call `time.time()` if `now_ts is None`
- Be careful not to delete directories.