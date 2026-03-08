from typing import List

# the original climbing stairs solution used recursion to track down
# using a cache to store previous results for O(1) lookup
# this is a modifier where we store the minimum of the results

class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        cache = {}
        def recur(i):
            if i < 2:
                return cost[i]
            if i in cache:
                return cache[i]
            cache[i] = cost[i] + min(recur(i-1), recur(i-2))
            return cache[i]
        
        return min(recur(len(cost)-1), recur(len(cost)-2))