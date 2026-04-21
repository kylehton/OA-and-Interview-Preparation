from typing import List

# this is still same house robber problem, but with one extra
# first and last houses are next to each other
# we cannot rob both in one sequence, must pick one
# we should compare the two and keep the larger
# this is only an issue if they are in the same sequence

class Solution:
    def rob(self, nums: List[int]) -> int:
        def robHouses(arr):
            curr = 0
            prev = 0
            for num in arr:
                curr_max = max(num+curr, prev)
                curr = prev
                prev = curr_max
            return prev
        if len(nums) == 1:
            return nums[0]
        return max(robHouses(nums[:-1]), robHouses(nums[1:]))
        