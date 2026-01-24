# we can use a greedy algorithm, checking the local maximum jump dist.
# we track a current maximum jump, and compute the possible jump dist.
# from a current index, and we take the maximum reached index
# after looping through all possible jumps within range of
# the current maximum, we compare

class Solution:
    def canJump(self, nums: list[int]) -> bool:
        curr_max = 0
        for i in range(len(nums)-1):
            if i > curr_max:
                return False
            curr_max = max(curr_max, i + nums[i])

        return (curr_max >= len(nums)-1)
