# go by each place and square, summing total
# store this result in a set 
# repeat process, if result in prev, we check:
# return True: if result == 1, or if result in set, where there is not 
# a single 1 in any of the places

class Solution:
    def isHappy(self, n: int) -> bool:
        seen = set()
        curr = n
        while True:
            temp = curr
            curr_sum = 0
            while temp != 0:
                curr_sum += (temp%10)**2
                temp //= 10
            if curr_sum == 1:
                return True
            if curr_sum in seen:
                return False
            else:
                seen.add(curr_sum)
            curr = curr_sum
        return True
        