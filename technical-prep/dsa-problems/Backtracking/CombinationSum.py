# we need all combinations of numbers where the sum = target
# we can run a recursive backtracking alg that a certain amount
# and keeps track of a sum, returning back up if equals or exceeds
# upon equals, we add it to the total result array
# need to pass: result array, current sum array, curr sum, i

class Solution:
    def combinationSum(self, nums: list[int], target: int) -> list[list[int]]:
        res = []
        def find_combos(self, result, curr_arr, curr_sum, index):
            if curr_sum == target:
                result.append(curr_arr[:])
                return
            for i in range(index, len(nums)):
                if curr_sum + nums[i] > target:
                    break
                curr_arr.append(nums[i])
                curr_sum += nums[i]
                find_combos(self, result, curr_arr, curr_sum, i)
                curr_arr.pop()
                curr_sum -= nums[i]
        
        nums.sort()
        find_combos(self, res, [], 0, 0)
        return res