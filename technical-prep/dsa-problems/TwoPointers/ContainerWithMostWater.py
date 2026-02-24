from typing import List

# we can use two pointers to dynamically move the window
# we want to go until the pointers pass each other
# we can be greedy by trying to optimize based on pointer height
# we recalculate area on each iteration and compare to max

class Solution:
    def maxArea(self, heights: List[int]) -> int:
        total_max = 0
        l = 0 
        r = len(heights)-1
        while l < r:
            curr_area = (r-l)*(min(heights[l], heights[r]))
            total_max = max(total_max, curr_area)
            if heights[l] > heights[r]:
                r -= 1
            else:
                l += 1
        return total_max