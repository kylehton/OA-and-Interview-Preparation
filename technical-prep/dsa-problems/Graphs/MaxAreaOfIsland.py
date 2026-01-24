# this is essentially a build onto number of islands
# rather than tracking num of islands, we can create an inner function
# we need to return sum of area upward to initial position to correctly
# count area amongst all recursive branches from one init.

class Solution:
    def maxAreaOfIsland(self, grid: list[list[int]]) -> int:
        max_area = 0
        def area_dfs(row, col):
            if 0 <= row < len(grid) and 0 <= col < len(grid[0]):
                local_sum = 0
                if grid[row][col] == 1:
                    grid[row][col] = 0
                    local_sum += area_dfs(row+1, col)
                    local_sum += area_dfs(row-1, col)
                    local_sum += area_dfs(row, col+1)
                    local_sum += area_dfs(row, col-1)
                    return 1+local_sum
                else:
                    return 0
            else:
                return 0
        
        for r in range(len(grid)):
            for c in range(len(grid[0])):
                if grid[r][c] == 1:
                    island_area = area_dfs(r, c)
                    max_area = max(max_area, island_area)
        
        return max_area
                