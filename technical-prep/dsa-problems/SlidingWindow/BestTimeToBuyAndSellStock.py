# we can use a sliding window with varying size
# the window gets larger as long as profit goes up
# when it lessens, we decrease window size back down

class Solution:
    def maxProfit(self, prices: list[int]) -> int:
        if len(prices) < 2:
            return 0
        if len(prices) == 2:
            return max(prices[1]-prices[0], 0)
        l = 0
        r = 1
        totalMax = 0
        while l <= r and r < len(prices):
            profit = prices[r] - prices[l]
            if profit < 0:
                l += 1
            else:
                r += 1
            totalMax = max(totalMax, profit)
        return totalMax