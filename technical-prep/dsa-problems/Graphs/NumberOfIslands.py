# we can use dfs to search through an entire island, marking it as visited
# we can iterate through the entire grid to find any valid islands

class Solution:
    def numIslands(self, grid: list[list[str]]) -> int:
        def grid_dfs(r, c):
            if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
                if grid[r][c] == '1':
                    grid[r][c] = 0
                else:
                    return
                grid_dfs(r+1, c)
                grid_dfs(r-1, c)
                grid_dfs(r, c+1)
                grid_dfs(r, c-1)
            else:
                return
        count = 0
        for row in range(len(grid)):
            for col in range(len(grid[0])):
                if grid[row][col] == "1":
                    count += 1
                    grid_dfs(row, col)
        
        return count
        
            