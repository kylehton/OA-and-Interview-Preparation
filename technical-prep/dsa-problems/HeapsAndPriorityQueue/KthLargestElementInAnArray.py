# we can use a heap to store all values passing in O(n)
# if we manipulate it to be a max-heap, we ppop k values
# and return the kth value, which should be the kth largest

import heapq

class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        heap = []
        heapq.heapify(heap)
        for num in nums:
            heapq.heappush(heap, -num)
        curr = 0
        for i in range(k):
            curr = heapq.heappop(heap)
        
        return -curr