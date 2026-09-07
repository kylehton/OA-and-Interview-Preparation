from typing import List

# we want to loop through smallest card, building a group of size
# groupSize and removing the counts fromm total count dict
# if the next consec. value DNE, return False
# if we are able to build all and the total card count == 0
# we can return True

# non optimal, since opens based on largest val, not count

class Solution:
    def isNStraightHand(self, hand: List[int], groupSize: int) -> bool:
        largest = 0
        for val in hand:
            if val > largest:
                largest = val
        bucket = [0 for _ in range(largest+1)]
        for val in hand:
            bucket[val] += 1
        index = 0
        while index < len(bucket):
            if bucket[index] != 0:
                curr = index
                for _ in range(groupSize):
                    if curr >= len(bucket) or bucket[curr] == 0:
                        return False
                    bucket[curr] -= 1
                    curr += 1
            
            if bucket[index] == 0:
                index += 1

        return True