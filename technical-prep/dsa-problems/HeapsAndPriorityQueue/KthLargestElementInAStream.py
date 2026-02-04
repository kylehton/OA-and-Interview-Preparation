# we can use a max heap implementation
# while the length of the heap is <= k, we keep adding
# else, we pop the top elem which would be the largest

import heapq

class KthLargest:

    def __init__(self, k: int, nums: list[int]):
        heapq.heapify(nums)
        self.minHeap = nums
        self.length = len(nums)
        self.k = k
        while self.length > self.k:
            heapq.heappop(self.minHeap)
            self.length -= 1

    def add(self, val: int) -> int:
        heapq.heappush(self.minHeap, val)
        self.length += 1
        while self.length > self.k:
            heapq.heappop(self.minHeap)
            self.length -= 1
        return (self.minHeap[0])
