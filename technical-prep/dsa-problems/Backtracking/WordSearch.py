from typing import List

# we can use a backtracking solution
# we only explore possible words that may be valid

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        visited = set()
        def backtrack(r, c, letter):
            nonlocal visited
            if (r, c) in visited or 0 > r or r >= len(board) or 0 > c or c >= len(board[0]) or board[r][c] != word[letter]:
                return False
            elif board[r][c] == word[letter] and letter == len(word)-1:
                return True
            visited.add((r, c))
            left = backtrack(r-1, c, letter+1)
            right = backtrack(r+1, c, letter+1)
            up = backtrack(r, c-1, letter+1)
            down = backtrack(r, c+1, letter+1)
            visited.remove((r, c))
            return (left or right or up or down)
        
        for i in range(len(board)):
            for j in range(len(board[0])):
                possible = backtrack(i, j, 0)
                if possible:
                    return True
        return False
