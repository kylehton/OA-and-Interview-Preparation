# since we want the heaviest stones, we can use a minHeap
# and tweak using negative values

import heapq

class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        for i in range(len(stones)):
            stones[i] *= -1
        heapq.heapify(stones)
        while len(stones) > 1:
            stone1 = heapq.heappop(stones)
            stone2 = heapq.heappop(stones)
            if stone1 < stone2: # real -> stone1 < stone2
                heapq.heappush(stones, stone1-stone2)
        if len(stones) == 0:
            return 0
        return -1*(stones[0])