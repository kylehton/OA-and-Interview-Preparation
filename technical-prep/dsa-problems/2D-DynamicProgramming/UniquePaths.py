class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        cache = {}
        def recur(x, y, cache):
            if (x, y) in cache:
                return cache[(x, y)]
            if x == m-1 and y == n-1:
                return 1
            elif x >= m or y >= n:
                return 0
            cache[(x, y)] = recur(x+1, y, cache) + recur(x, y+1, cache)
            return cache[(x, y)]

        return recur(0, 0, cache)