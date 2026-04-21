# if we used a traditional array, finding the median would require inserting in sorted
# order which would result in O(n) insert time minimum, and O(n^2) at worst

# since we only need one/two middle values, we need some sort of way to maintain those 
# two values. we can use two different heaps, one of which represents the left half
# of a heap with the largest value on top, and the other which represents the right
# half of a heap with the smallest value on top
# we then have a length int to see whether the value needs to be returned or computed 
# first, and from there, we return the median

# on uneven insertions, we want to use the value from the heap with more elements.
# following that, an insertion of an item needs some way to getting sorted to left
# or right. we can use the previous median to do so, where >= median is right, and <
# median is left

import heapq

class MedianFinder:

    def __init__(self):
        self.leftHalf = []
        self.rightHalf = []
        self.median = 0
        self.length = 0

    def addNum(self, num: int) -> None:

        if self.rightHalf and num < self.rightHalf[0]:
            heapq.heappush(self.leftHalf, -num)
        else:
            heapq.heappush(self.rightHalf, num)
        self.length += 1

        # balance here
        while not ((len(self.leftHalf) == len(self.rightHalf)) or (len(self.leftHalf) == len(self.rightHalf)+1) or (len(self.leftHalf)+1 == len(self.rightHalf))):
            if len(self.leftHalf) < len(self.rightHalf):
                heapq.heappush(self.leftHalf, (heapq.heappop(self.rightHalf)*-1))
            else:
                heapq.heappush(self.rightHalf, (heapq.heappop(self.leftHalf)*-1))

        if not self.rightHalf:
            self.median = self.leftHalf[0]*-1
        if not self.leftHalf:
            self.median = self.rightHalf[0]

        if self.length%2 == 1:
            if len(self.leftHalf) > len(self.rightHalf):
                self.median = self.leftHalf[0]*-1
            else:
                self.median = self.rightHalf[0]
        else:
            self.median = ((self.leftHalf[0]*-1) + self.rightHalf[0])/2

    def findMedian(self) -> float:
        return self.median
        