# we must find the minimum int k where we are able to eat all in h hours
# bananas are in piles (values), where you must eat one pile max per hour
# we can use a binary algorithm to find the suitable eating time

# we begin at a median eating rate, increasing if not within h hours
# we go from 0 to max value in array (can eat each pile in 1 hr)

import math

class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        high = 0
        for pile in piles:
            high = max(pile, high)
        result = 0
        low = 1
        while low <= high:
            mid = (low+high)//2
            hour_sum = 0
            for pile in piles:
                hour_sum += int(math.ceil(pile/mid))
            if hour_sum <= h:
                high = mid-1
                result = mid
            else:
                low = mid+1
        return result