# we can use a bucket sort sol

# we use an array from 0 to total len (end at len(nums)+1)
# we use a dict to count, and by each item in dict, place it at count index
# iterate backward from bucket arr until len = k

from collections import defaultdict

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        bucket = [[] for i in range(len(nums) + 1)]
        count_dict = defaultdict(int)

        for num in nums:
            count_dict[num] += 1
        
        for n, i in count_dict.items():
            bucket[i].append(n)
        
        result = []
        for i in range(len(bucket)-1, -1, -1):
            for val in bucket[i]:
                result.append(val)
            if len(result) == k:
                return result
        
        return [-1]
