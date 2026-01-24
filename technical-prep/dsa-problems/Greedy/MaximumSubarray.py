# we need the absolute largest sum subarray from nums
# at each iteration we can either:
# 1. continue the current subarray
# 2. start a new subarray

class Solution:
    def maxSubArray(self, nums: list[int]) -> int:
        max_sum = nums[0]
        curr_sum = 0
        for num in nums:
            curr_sum = max(curr_sum, 0)
            curr_sum += num
            max_sum = max(curr_sum, max_sum)
        return max_sum
    
        