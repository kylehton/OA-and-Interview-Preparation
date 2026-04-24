from typing import List

# first, dfs on border Os
# after this, entire border should be marked as a proper border, and all 0s inside
# are then surrounded

# change all existing Os to Xs, then reverse back to Os for all non-surrounded

# Time Complexity: O(R x C)
# Space Complexity: O(R x C) because recursive stack

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        def dfs(r, c):
            if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]) or board[r][c] != 'O':
                return
            board[r][c] = 'I' # I -> invalid
            dfs(r+1, c)
            dfs(r-1, c)
            dfs(r, c+1)
            dfs(r, c-1)

        # traverse by row, check columns
        for i in range(len(board)):
            if board[i][0] == 'O':
                dfs(i, 0)
            if board[i][len(board[0])-1] == 'O':
                dfs(i, len(board[0])-1)
        
        # traverse by col, check row
        for i in range(len(board[0])):
            if board[0][i] == 'O':
                dfs(0, i)
            if board[len(board)-1][i] == 'O':
                dfs(len(board)-1, i)
        
        # change all surrounded regions
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == 'O':
                    board[r][c] = 'X'
        
        # reverse nonsurrounded regions
        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == 'I':
                    board[r][c] = 'O'
