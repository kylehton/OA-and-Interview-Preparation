from typing import List

# we should go ring by ring, but it is not mxm
# we need two counters, one for m and one for n
# we can have four different loops for each side
# where the full stopping condition is either exceeding m or n
# r = 0, c = 0

# 1  2  3  4
# 5  6  7  8
# 9 10 11 12
# result -> matrix[r][all c]
# result -> matrix[all r+1 until r+1 = len(matrix)-r-1]

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        r = c = 0
        result = []
        while r < len(matrix)-r and c < len(matrix[0])-c:
            # top
            print(r, c)
            for i in range(c, len(matrix[0])-c):
                result.append(matrix[r][i])
            print(result)

            # right
            for i in range(r+1, len(matrix)-r):
                result.append(matrix[i][len(matrix[0])-c-1])
            print(result)

            if r < len(matrix)-r-1 and c < len(matrix[0])-c-1:
                # bottom
                for i in range(len(matrix[0])-c-2, c-1, -1):
                    result.append(matrix[len(matrix)-r-1][i])

                # left
                for i in range(len(matrix)-r-2, r, -1):
                    result.append(matrix[i][c])

            r += 1
            c += 1

        return result