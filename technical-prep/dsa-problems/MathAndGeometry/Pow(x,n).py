# 2^5 = 2^3 * 2^2
# use memoization for optimization

class Solution:
    def myPow(self, x: float, n: int) -> float:
        cache = {}
        def recurSq(num: float, exp: int) -> float:
            if exp in cache:
                return cache[exp]
            if exp == 1:
                return num
            if exp == 0:
                return 1
            temp = exp//2
            cache[exp] = recurSq(num, temp) * recurSq(num, exp-temp)
            return cache[exp]
        
        if n < 0:
            return 1/recurSq(x, -n)
        return recurSq(x, n)