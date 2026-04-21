from typing import List

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        def removeIsland(i, j):
            if 0 > i or i >= len(grid) or 0 > j or j >= len(grid[0]) or grid[i][j] == '0':
                return
            grid[i][j] = '0'
            removeIsland(i+1, j)
            removeIsland(i-1, j)
            removeIsland(i, j+1)
            removeIsland(i, j-1)
            return

        count = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == '1':
                    count += 1
                    removeIsland(r, c)
        
        return count
