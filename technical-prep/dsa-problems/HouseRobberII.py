# this is still same house robber problem, but with one extra
# first and last houses are next to each other
# we cannot rob both in one sequence, must pick one
# we should compare the two and keep the larger
# this is only an issue if they are in the same sequence
# -> basically if there is an odd number of houses

class Solution:
    def rob(self, nums: list[int]) -> int:
        def rob_path(num_arr):
            path1 = 0
            path2 = 0
            for num in num_arr:
                curr_max = max(path1+num, path2)
                path1 = path2
                path2 = curr_max
            return path2

        if len(nums) == 0:
            return 0
        elif len(nums) == 1:
            return nums[0]
        elif len(nums) == 2:
            return max(nums[0], nums[1])

        profit1 = profit2 = 0
        # we must remove one or the other no matter what
        # regardless of even or odd, it must be impossible
        # for them to be added into the same rob path
        profit1 = rob_path(nums[:len(nums)-1])
        profit2 = rob_path(nums[1:])
        
        return max(profit1, profit2)
        
        