# each increment of time rots the surrounding fruit, so we run bfs
# and keep track of the amount of cycles it takes for all values
# to be visited/rotted
# we first need to find all initial rotting oranges
# from there, we run bfs on the set of initial
# we should take the current length of queue for each level as well,
# so when we append new nodes for next bfs level, they do not change

from collections import deque

class Solution:
    def orangesRotting(self, grid: list[list[int]]) -> int:

        rotting_q = deque()

        def rot_nearby(row, col):
            if 0 <= row+1 < len(grid) and 0 <= col < len(grid[0]):
                if grid[row+1][col] == 1:
                    grid[row+1][col] = 2
                    rotting_q.append((row+1, col))
            if 0 <= row-1 < len(grid) and 0 <= col < len(grid[0]):
                if grid[row-1][col] == 1:
                    grid[row-1][col] = 2
                    rotting_q.append((row-1, col))
            if 0<= row < len(grid) and 0 <= col+1 < len(grid[0]):
                if grid[row][col+1] == 1:
                    grid[row][col+1] = 2
                    rotting_q.append((row, col+1))
            if 0 <= row < len(grid) and 0 <= col-1 < len(grid[0]):
                if grid[row][col-1] == 1:
                    grid[row][col-1] = 2
                    rotting_q.append((row, col-1))

        fruit_cnt = 0 # edge case if all 0s
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == 2:
                    rotting_q.append((row, col))
                if grid[row][col] > 0:
                    fruit_cnt += 1
        
        if fruit_cnt == 0:
            return 0
        
        currTime = 0
        while rotting_q:
            currTime += 1
            for i in range(len(rotting_q)):
                r, c = rotting_q.popleft()
                rot_nearby(r, c)
        
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 1:
                    return -1
        
        return currTime-1

        
