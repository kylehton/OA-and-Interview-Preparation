from typing import List

# we can use two pointers to track iteration by iteration bounds
# we would explore each possible distance/jump at each iteration
# where the amount of possible steps in each iteration is dependent
# on the values in each
# we can find the maximum length traveled per item viewed per iteration


class Solution:
    def jump(self, nums: List[int]) -> int:
        result = l = r = 0

        while r < len(nums)-1:
            farthestDistance = 0
            for i in range(l, r+1): # from l-r
                farthestDistance = max(farthestDistance, i + nums[i])
            l = r+1
            r = farthestDistance
            result += 1

        return result
        