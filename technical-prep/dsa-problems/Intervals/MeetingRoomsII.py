from typing import List

class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

# we want the earliest availability for each check
# we can use a heap to store the end times of each meeting
# and for each insert, we compare with the earliest
# if its free, we update that top heap val with the current

import heapq

class Solution:
    def minMeetingRooms(self, intervals: List[Interval]) -> int:
        intervals.sort(key=lambda x: x.start)
        heap = []
        for interval in intervals:
            if not heap:
                heapq.heappush(heap, interval.end)
            elif interval.start >= heap[0]:
                    heapq.heapreplace(heap, interval.end)
            else:
                heapq.heappush(heap, interval.end)
        
        return len(heap)