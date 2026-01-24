

class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        res = []
        def build_subset(self, index, curr_arr, result):
            if index >= len(nums):
                result.append(curr_arr[:])
                return
            build_subset(self, index+1, curr_arr, result)
            curr_arr.append(nums[index])
            build_subset(self, index+1, curr_arr, result)
            curr_arr.pop()
        
        build_subset(self, 0, [], res)
        return res