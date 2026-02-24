from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[1])
        for i in range(len(intervals)-1, 0, -1):
            if intervals[i][0] <= intervals[i-1][1]:
                new_start = min(intervals[i][0], intervals[i-1][0])
                new_end = max(intervals[i][1], intervals[i-1][1])
                intervals[i-1] = [new_start, new_end]
                intervals.pop(i)
        
        return intervals