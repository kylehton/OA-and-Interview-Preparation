class Solution:
    def getSum(self, a: int, b: int) -> int:
        result = 0
        carry = 0
        for i in range(32):
            prev = carry
            if ((a & 1) & (b & 1)) | ((a & 1) & carry) | ((b & 1) & carry):
                carry = 1
            else:
                carry = 0

            result |= ((a & 1) ^ (b & 1) ^ prev) << i
            
            a >>= 1
            b >>= 1
        
        if result < (1 << 31):
            return result

        return result - (1 << 32)