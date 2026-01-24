# we need to find two numbers that sum to target
# we know they are nondecreasing, and that there exists one valid sol.


class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        l = 0
        r = len(numbers)-1
        while l <= r:
            total = numbers[l] + numbers[r]
            if total == target and l != r:
                return [l+1, r+1]
            elif total < target:
                l += 1
            else:
                r -= 1
        

        