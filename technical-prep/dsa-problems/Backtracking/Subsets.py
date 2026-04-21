from typing import List

# we can use a backtracking algorithm, where we recursively add/don't add a particular
# elem, adding forward (to avoid duplicates)

class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        result = []
        def backtrack(index, arr):
            nonlocal result
            if index == len(nums):
                result.append(arr[:])
            else:
                arr.append(nums[index])
                backtrack(index+1, arr)
                arr.pop()
                backtrack(index+1, arr)
            return arr
        
        backtrack(0, [])
        return result