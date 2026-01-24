# if we use normal recursion, we have a lot of duplicate calculations/
# recursive calls
# ex) n = 6 -> n = 5, n = 4 -> n = 4, n = 3, n = 3, n = 2 -> n = 3
# n = 2, n = 2, n = 1, n = 1, n = 0 -> n = 1, n = 2
# we can use a cache to store calculations based on n to use prev. res.
# MUST return result at each n upward for summation up recursive tree
# this way, we essentially compute once per n, reducing time complexity
# to O(n)
# base case: if n == 1: return 1, if n == 0: return 0

from collections import defaultdict

class Solution:
    def climbStairs(self, n: int) -> int:
        def findWays(i, cache):
            if i == 1:
                return 1
            elif i == 2:
                return 2
            elif i in cache:
                return cache[i]
            # sum all ways to climb stairs at a given n
            cache[i] = findWays(i-1, cache) + findWays(i-2, cache)
            return cache[i]

        cache = {}
        return findWays(n, cache)

        