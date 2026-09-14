# convert int to string and store sign
# reverse string and convert back to int
# check 32 bit boundaries and return result

class Solution:
    def reverse(self, x: int) -> int:
        sign = 1 if x > 0 else -1
        string = str(abs(x))[::-1]
        result = int(string) * sign
        if result < (-2**31) or result > (2**31 - 1):
            return 0
        return result
        