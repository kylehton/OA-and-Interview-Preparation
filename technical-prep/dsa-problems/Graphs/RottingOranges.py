from typing import List

# we should run a bfs, where we go layer by layer beginning from
# any position where the grid is 2. on each iteration, we set the
# visited position = 0 to prevent duplicate counting

from collections import deque

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        DIRECTION = [(1,0), (0,1), (-1,0), (0,-1)]
        queue = deque()
        countMinutes = 0
        freshCount = 0
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 2:
                    queue.append((r, c))
                elif grid[r][c] == 1:
                    freshCount += 1

        while queue and freshCount > 0:
            for _ in range(len(queue)):
                top = queue.popleft()
                for dr, dc in DIRECTION:
                    i, j = top[0]+dr, top[1]+dc
                    if i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0]):
                        if grid[i][j] == 1:
                            queue.append((i, j))
                            grid[i][j] = 0
                            freshCount -= 1
            countMinutes += 1

        if freshCount != 0:
            return -1
        return countMinutes
