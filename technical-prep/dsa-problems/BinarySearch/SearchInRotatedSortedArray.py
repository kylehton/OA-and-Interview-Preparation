# since we don't know the num of rotations, we need to find
# the current orientation of mid in binary search

class Solution:
    def search(self, nums: list[int], target: int) -> int:
        l = 0
        r = len(nums)-1

        while l <= r:
            mid = (l + r) // 2
            
            if nums[mid] == target:
                return mid
            # Left half is sorted
            if nums[l] <= nums[mid]:
                if nums[l] <= target < nums[mid]:
                    r = mid-1
                else:
                    l = mid+1
            # Right half is sorted
            else:
                if nums[mid] < target <= nums[r]:
                    l = mid+1
                else:
                    r = mid-1


        return -1