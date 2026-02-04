class Solution:
    def plusOne(self, digits: list[int]) -> list[int]:
        i = len(digits)-1
        curr_sum = 0

        for digit in digits:
            curr_sum += digit*(10**i)
            i -= 1
        
        curr_sum += 1

        result = []
        while curr_sum > 0:
            result.append(curr_sum%10)
            curr_sum //= 10

        return result[::-1]