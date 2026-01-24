# we have a 9x9 board, where we need to check if its valid
# valid row and col = in that indexed row/col, no repeats
# no-number items = '.', elems ARE STRINGS
# we need three diff checks: row, col, sub-box

from collections import defaultdict

class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        row_items = defaultdict(set)
        col_items = defaultdict(set)
        box_items = defaultdict(set)
        for row in range(len(board)):
            for col in range(len(board[0])):
                curr_item = board[row][col]
                if curr_item != '.':
                    if curr_item in row_items[row] or curr_item in col_items[col] or curr_item in box_items[(row//3, col//3)]:
                        return False
                    row_items[row].add(curr_item)
                    col_items[col].add(curr_item)
                    box_items[(row//3, col//3)].add(curr_item)
            
        return True
