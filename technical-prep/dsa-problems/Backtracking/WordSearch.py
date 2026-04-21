from typing import List

# we can use a backtracking solution
# we only explore possible words that may be valid

class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        def search(r: int, c: int, index: int, visited: set):
            if r < 0 or r >= len(board) or c < 0 or c >= len(board[0]) or index == len(word):
                return (index == len(word))
            if (r, c) in visited:
                return False
            if board[r][c] == word[index]:
                index += 1
                visited.add((r, c))
                wordFound = search(r+1, c, index, visited) or search(r-1, c, index, visited) or search(r, c+1, index, visited) or search(r, c-1, index, visited)
                index -= 1
                visited.remove((r, c))
                return wordFound
            else:
                return False

        for r in range(len(board)):
            for c in range(len(board[0])):
                if board[r][c] == word[0]:
                    found = search(r, c, 0, set())
                    if found:
                        return True
        return False

