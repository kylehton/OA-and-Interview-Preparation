from typing import List

# we have an array of numbers = nums, and an int target
# we need all combinations of numbers that sum up to target, excluding duplicates

# we should first sort to avoid duplicates
# we can backtrack in adding numbers, with a return base case of:
# sum equalling or exceeding target. we add to result on equal

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        result = []
        def backtrack(arr: list[int], currSum: int, index: int):
            nonlocal result
            if currSum >= target:
                if currSum == target:
                    result.append(arr[:])
                return arr
            
            for i in range(index, len(nums)):
                arr.append(nums[i])
                backtrack(arr, currSum+nums[i], i)
                arr.pop()
        
            return arr
        
        backtrack([], 0, 0)
        return result