# for O(logn) we should use binary search alg.
# given the three vars: l, r, mid, we can compare the values at l and r
# to see where to move. we look between l-mid and mid-r
# ex) [3 4 5 6 1 2] -> 3 > 2 -> [6 1 2] -> 6 > 2 -> [1 2]
# 1 < 2, so do normal bin search = 1

class Solution:
    def findMin(self, nums: list[int]) -> int:

        l = 0
        r = len(nums)-1

        if nums[l] < nums[r]: # if already sorted
            return nums[l]

        result = nums[0]

        while l <= r:
            mid = (l+r)//2
            result = min(result, nums[l])
            print("nums l r:", nums[l], nums[r])
            if nums[l] > nums[r]:
                l = mid+1
            else:
                r = mid-1
                if nums[l] > nums[l-1]:
                    l -= 1
        
        return result
            

