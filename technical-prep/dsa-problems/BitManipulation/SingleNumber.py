# we can use exclusive or in bit representation of int
# two xor of the same number cancels it out, meaning
# every pair eventually gets cancelled out
# whats left is the xor with the singular number which has nothing
# to cancel out, leaving it as the result

class Solution:
    def singleNumber(self, nums: list[int]) -> int:
        curr = 0
        for num in nums:
            curr = curr ^ num
        return curr