from typing import List

# distance from chest = index1 - index2 + 1
# instead of bfs from each INF, we can do bfs from each treasure chest
# with that, we go through all chests and keep iterating bfs for each one
# we should use a singular queue, using a length based for loop
# if we used a subqueue, it might not find the minimum distance from a chest
# and only compute distance for a specific chest

from collections import deque

class Solution:
    def islandsAndTreasure(self, grid: List[List[int]]) -> None:
        INF = 2147483647
        DIRECTION = [(1,0), (0,1), (-1,0), (0,-1)]

        queue = deque()
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 0:
                    queue.append((r, c))
        
        level = 0
        while queue:
            level += 1
            for _ in range(len(queue)):
                curr = queue.popleft()
                for dr, dc in DIRECTION:
                    row = curr[0] + dr
                    col = curr[1] + dc
                    if row >= 0 and row < len(grid) and col >= 0 and col < len(grid[0]) and grid[row][col] == INF:
                        queue.append((row, col))
                        grid[row][col] = level
        
