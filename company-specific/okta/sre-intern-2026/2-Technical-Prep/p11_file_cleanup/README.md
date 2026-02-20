# P11 — File Cleanup (os/path + datetime + Safety)

Implement:

    list_old_files(root_dir: str, older_than_days: int, now_ts: float | None = None) -> list[str]

Return a list of **absolute paths** to files under `root_dir` (recursive)
whose modification time (mtime) is strictly older than `older_than_days` days.

- If now_ts is provided, treat it as "current time" (seconds since epoch).
- Only include regular files (ignore directories, symlinks).
- Return paths sorted lexicographically.

## Follow-up

Implement:

    delete_old_files(root_dir: str, older_than_days: int, dry_run: bool = True, now_ts: float | None = None) -> list[str]

Delete the same set of files if dry_run=False.

Return the list of files that would be (or were) deleted, sorted.

Constraints:
- Use os.walk
- Must be testable (do not call time.time directly unless now_ts is None)
