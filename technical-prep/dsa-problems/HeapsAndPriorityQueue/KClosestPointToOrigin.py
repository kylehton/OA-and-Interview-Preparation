from typing import List

# heap, manage size of k -> return any order
# track len heap, replace on len > k

import heapq
import math

class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        heap = []

        for point in points:
            distance = math.sqrt((point[0]**2) + (point[1]**2))
            if len(heap) == k:
                if -distance > heap[0][0]:
                    heapq.heapreplace(heap, (-distance, point))
            else:
                heapq.heappush(heap, (-distance, point))
        
        result = []
        for item in heap:
            result.append(item[1])
        return result