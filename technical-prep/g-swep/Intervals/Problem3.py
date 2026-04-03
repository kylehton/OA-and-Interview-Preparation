'''
Given a binary array nums and an integer goal, return the number of non-empty subarrays with a sum 
goal.
- A subarray is a contiguous part of the array.


Example 1:
Input: nums = [1,0,1,0,1], goal = 2
Output: 4

Explanation: The 4 subarrays are bolded and underlined below:
[1,0,1,x,x]
[1,0,1,0,x]
[x,0,1,0,1]
[x,x,1,0,1]

Example 2:
Input: nums = [0,0,0,0,0], goal = 0
Output: 15
'''

# we want to iterate through the entire array and use a sliding window, keeping track
# of running sum and comparing that to the current goal. we add for each equality
# this equates to a runtime of O(2n) for both pointers, reducing down to O(n) asymptotically
from collections import defaultdict

def non_empty_subarrays(nums: list, goal: int) -> int:
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1  # empty prefix
    curr_sum = 0
    count = 0
    for num in nums:
        curr_sum += num
        count += prefix_counts[curr_sum - goal]
        prefix_counts[curr_sum] += 1
    return count



#Input: nums = [1,0,1,0,1], goal = 2
print(non_empty_subarrays([1,0,1,0,1], 2))

#Input: nums = [0,0,0,0,0], goal = 0
print(non_empty_subarrays([0,0,0,0,0], 0))