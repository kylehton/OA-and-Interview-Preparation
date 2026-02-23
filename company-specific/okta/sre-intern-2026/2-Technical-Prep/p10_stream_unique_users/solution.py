from __future__ import annotations

from typing import List, Tuple


def count_unique_users(filepath: str) -> int:
    seen = set()
    count = 0
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                user = parts[1]
                if user not in seen:
                    seen.add(user)
                    count += 1
    return count

def top_active_users(filepath: str, k: int) -> List[Tuple[str, int]]:
    from collections import defaultdict
    import heapq
    user_dict = defaultdict(int)
    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                user_dict[parts[1]] += 1
    
    return heapq.nsmallest(k, user_dict.items(), key=lambda x: (-x[1], x[0]))
