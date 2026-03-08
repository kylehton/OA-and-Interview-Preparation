from typing import List

class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        # we can iterate through the array, until a specific number is
        # invalid, where we use the current array to store validity
        # for valid numbers, we set their array values to 0, since 0
        # cannot be an actual value in the range [1, n]
        # from that, if we access a valued-index where it already is 0,
        # we know that it has been accessed before by another prev.
        # value, so it is a duplicate.

        index = 0

        while (nums[index] != 0):
            temp = nums[index]
            nums[index] = 0
            index = temp
        
        return index