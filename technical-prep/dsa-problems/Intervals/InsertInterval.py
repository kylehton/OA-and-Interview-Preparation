class Solution:
    def insert(self, intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
        # find insert
        i = 0
        while i < len(intervals) and newInterval[0] > intervals[i][0]:
            i += 1
        intervals.insert(i, newInterval)

        # merge with next intervals
        j = i
        while j + 1 < len(intervals) and intervals[j][1] >= intervals[j+1][0]:
            intervals[j][1] = max(intervals[j][1], intervals[j+1][1])
            del intervals[j+1]
        
        # merge with previous interval
        while i > 0 and intervals[i][0] <= intervals[i-1][1]:
            intervals[i-1][1] = max(intervals[i-1][1], intervals[i][1])
            intervals[i-1][0] = min(intervals[i-1][0], intervals[i][0])
            del intervals[i]
            i -= 1
        
        return intervals