from typing import List

# we can sort then iterate backward, removing any entries that would
# result in a merge
# we can then take the original length minus the new length,
# which is the number of intervals removed to make the rest of the
# intervals non-overlapping

# del/removing entries is O(n), resulting in an overall O(n^2)
# instead, we can move the interval down, effectively 'skipping'
# the overlapping interval

# the sort algorithm would result in a time complexity of O(n log n),
# and a space complexity of O(n). the loop would add an additional O(n),
# which generalizes/reduces to an asymptotic time complexity of O(nlogn)

class Solution:
    def eraseOverlapIntervals(self, intervals: List[List[int]]) -> int:
        intervals.sort()
        i = len(intervals)-1
        count = 0
        while i > 0:
            while i > 0 and i < len(intervals) and intervals[i][0] < intervals[i-1][1]:
                print(i, intervals)
                intervals[i-1] = intervals[i]
                count += 1
                i -= 1
            i -= 1
        
        return count
        