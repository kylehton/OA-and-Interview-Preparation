class Solution:
    def searchMatrix(self, matrix: list[list[int]], target: int) -> bool:
        low = 0
        high = len(matrix) * len(matrix[0])-1

        while low <= high:
            mid = (low+high)//2
            index = mid % len(matrix[0])
            array = mid // len(matrix[0])
            if matrix[array][index] == target:
                return True
            if matrix[array][index] < target:
                low = mid+1
            else:
                high = mid-1
        
        return False
        