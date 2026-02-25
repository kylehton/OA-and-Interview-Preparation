from __future__ import annotations

from typing import List, Optional


def list_old_files(root_dir: str, older_than_days: int, now_ts: Optional[float] = None) -> List[str]:
    import os
    import time
    # we need to go through all paths in root directory
    # we want to only include files -> use .isfile(path)
    # we add all valid files into a list, sorted lexicographically O(n log n)
    old_files = []
    curr_time = now_ts if now_ts is not None else time.time()
    for root, dir, files in os.walk(root_dir):
        for file in files:
            curr_path = f"{root}/{file}"
            print(curr_path)
            if not os.path.islink(curr_path) and os.path.isfile(curr_path):
                mtime = os.path.getmtime(curr_path)
                if (curr_time - mtime) > (older_than_days * 84600):
                    old_files.append(curr_path)
        
    old_files.sort()
    return old_files


def delete_old_files(root_dir: str, older_than_days: int, dry_run: bool = True, now_ts: Optional[float] = None) -> List[str]:
    import os
    old_files = list_old_files(root_dir, older_than_days, now_ts)
    if not dry_run:
        for file in old_files:
            os.remove(file)
    return old_files

