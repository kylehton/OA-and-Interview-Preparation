from typing import List

# we can iterate through each num from 1 to n inclusive
# for each number, we loop through its bin rep and count 1s

class Solution:
    def countBits(self, n: int) -> List[int]:
        result = [0 for i in range(n+1)]
        for i in range(1, n+1):
            result[i] = result[(i >> 1)] + (i & 1)
        return result