from typing import List

# we can use a heap of size k
# we essentially use negative values to ensure storage of the k largest elems
# the top of the heap, since it is minimum, will always be the minimum of the k largest

import heapq

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heap = []
        for num in nums:
            heapq.heappush(heap, num)
            while len(heap) > k:
                heapq.heappop(heap)
        
        return heap[0]