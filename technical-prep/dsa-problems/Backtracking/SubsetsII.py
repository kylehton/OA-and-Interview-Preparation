from typing import List

# we can create subsets based on index, to avoid duplicate index
# elements. we use backtracking to add/no add and on index reaching
# length of nums, we add to result array and return recursively

class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        result = []
        nums.sort()
        def backtrack(arr, index):
            result.append(arr[:])
            for i in range(index, len(nums)):
                if i > index and nums[i] == nums[i-1]:
                    continue
                arr.append(nums[i])
                backtrack(arr, i+1)
                arr.pop()
        
        backtrack([], 0)
        return result