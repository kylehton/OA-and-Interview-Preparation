class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        num_dict = {}
        for index, num in enumerate(nums):
            num_dict[num] = index
        
        result = []
        for i, n in enumerate(nums):
            if target-n in num_dict and i != num_dict[target-n]:
                result.append(i)
                result.append(num_dict[target-n])
                break
                    
        result.sort()
        return result