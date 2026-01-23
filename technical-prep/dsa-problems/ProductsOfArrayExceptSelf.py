# use prefix and postfix sum multiplier

class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        prefix = 1
        postfix = 1
        result = [1 for i in range(len(nums))]

        for i in range(len(nums)):
            result[i] = prefix
            prefix *= nums[i]
        
        for i in range(len(nums)-1, -1, -1):
            result[i] *= postfix
            postfix *= nums[i]
    
        return result