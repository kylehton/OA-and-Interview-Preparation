# fixed size of 32, so we can loop through 32 times and still be O(1)
# for a given number, we want to extract the rightmost bit
# we OR with rightmost then shift result left once

# CORRECTION: should shift first. an initial left shift with result=0
# does nothing to the final value, and shifting AFTER will cause the final
# result to be shifted left one too many times

class Solution:
    def reverseBits(self, n: int) -> int:
        result = 0
        for i in range(32):
            result = result << 1
            right_bit = (n >> i) & 1
            result = result | right_bit
        return result

