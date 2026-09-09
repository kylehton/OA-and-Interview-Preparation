from typing import List

# not optimal, exists way to do O(1) space complexity

class Solution:
    def setZeroes(self, matrix: List[List[int]]) -> None:
        r_z = set()
        c_z = set()
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if matrix[r][c] == 0:
                    r_z.add(r)
                    c_z.add(c)
        for r in range(len(matrix)):
            for c in range(len(matrix[0])):
                if r in r_z or c in c_z:
                    matrix[r][c] = 0
        
        