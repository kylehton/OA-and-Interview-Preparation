from __future__ import annotations

from typing import Dict, List, Tuple


def merge_downtime(filepath: str) -> Dict[str, List[Tuple[int, int]]]:
    from collections import defaultdict
    intervals = defaultdict(list)

    with open(filepath, "r") as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                service = parts[0].strip()
                if parts[1].strip().isnumeric() and parts[2].strip().isnumeric() and int(parts[2]) > 0:
                    start = int(parts[1].strip())
                    end = int(parts[2].strip())
                    if (start <= end):
                        intervals[service].append((start, end))

    for service, interval_list in intervals.items():
        interval_list.sort()

    for service, interval_list in intervals.items():
        for i in range(len(interval_list)-1, 0, -1):
            if interval_list[i-1][1]+1 >= interval_list[i][0]:
                new_start = min(interval_list[i-1][0], interval_list[i][0])
                new_end = max(interval_list[i-1][1], interval_list[i][1])
                interval_list[i-1] = (new_start, new_end)
                interval_list.pop(i)
    
    return intervals



def total_downtime_seconds(merged: Dict[str, List[Tuple[int, int]]]) -> Dict[str, int]:
    total_seconds = {}
    for service, interval_list in merged.items():
        curr_sum = 0
        for start, end in interval_list:
            curr_sum += (end - start + 1)
        total_seconds[service] = curr_sum

    return total_seconds