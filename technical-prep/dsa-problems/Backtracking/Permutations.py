from typing import List

# we can use backtracking to add a particular element
# from this, the base case would be upon any list of len(nums)

class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        result = []
        def backtrack(arr, added): # arr = current array, added = prev. added
            if len(arr) >= len(nums):
                result.append(arr[:])
                return arr

            for i in range(len(added)):
                if not added[i]:
                    arr.append(nums[i])
                    added[i] = True
                    backtrack(arr, added)
                    arr.pop()
                    added[i] = False
            
            return arr
        
        backtrack([], [False for _ in range(len(nums))])
        return result