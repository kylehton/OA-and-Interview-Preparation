from __future__ import annotations

from typing import List, Optional


def list_old_files(root_dir: str, older_than_days: int, now_ts: Optional[float] = None) -> List[str]:
    raise NotImplementedError


def delete_old_files(
    root_dir: str,
    older_than_days: int,
    dry_run: bool = True,
    now_ts: Optional[float] = None,
) -> List[str]:
    raise NotImplementedError
