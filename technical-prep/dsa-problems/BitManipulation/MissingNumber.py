from typing import List

# bit manipulation solution
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        xor = len(nums) # to include n in xor comparison
        for i in range(len(nums)):
            xor ^= (i ^ nums[i]) # xor -> cancel out pairings of valid index-value from 0-n
        return xor

# non bit manipulation solution
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        exp_sum = 0
        for i in range(len(nums)+1):
            exp_sum += i

        actual_sum = 0
        for num in nums:
            actual_sum += num

        return exp_sum - actual_sum