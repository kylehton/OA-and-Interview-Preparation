from typing import List

# we can use a two pointer window approach

# we use the two bounds, calculating per iteration towards each other.
# on each stage, we either move left or right pointer, where we use that
# to subtract the area that cannot store water. we use a left and right maximum val
# variables to store the current maximums, so we can compare lesser columns and subtract
# out area
        

class Solution:
    def trap(self, height: List[int]) -> int:
        l, r = 0, len(height)-1
        area = 0
        lMax, rMax = 0, 0
        while l < r:
            lMax = max(lMax, height[l])
            rMax = max(rMax, height[r])
            if lMax < rMax:
                area += lMax - height[l]
            else:
                area += rMax - height[r]

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        
        return area
        


