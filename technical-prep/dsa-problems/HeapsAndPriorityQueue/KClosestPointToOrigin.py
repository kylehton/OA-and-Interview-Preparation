# we can use a heap to store a tuple, where the first value
# is the Euclidean dist, and the second is the point itself

import heapq
import math

class Solution:
    def kClosest(self, points: list[list[int]], k: int) -> list[list[int]]:
        heap = []
        heapq.heapify(heap)
        for point in points:
            dist = math.sqrt(point[0]**2 + point[1]**2)
            heapq.heappush(heap, (dist, point))

        result = []
        for i in range(k):
            result.append(heapq.heappop(heap)[1])
        return result