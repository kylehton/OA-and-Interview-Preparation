from typing import List

# we can go ahead and implement a divide and conquer algorithm
# we split the array in halves recursively, until we

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def merge(arr1: List[int], arr2: List[int]) -> List[int]:
            res = []
            p1, p2 = 0, 0
            while p1 < len(arr1) and p2 < len(arr2):
                if arr2[p2] < arr1[p1]:
                    res.append(arr2[p2])
                    p2 += 1
                else:
                    res.append(arr1[p1])
                    p1 += 1
            
            if p1 != len(arr1):
                for i in range(p1, len(arr1)):
                    res.append(arr1[i])
            elif p2 != len(arr2):
                for i in range(p2, len(arr2)):
                    res.append(arr2[i])
            return res
        
        def mergeSort(arr: List[int]):
            if (len(arr) == 1):
                return arr
            
            mid = (len(arr)//2)
            left = mergeSort(arr[:mid])
            right = mergeSort(arr[mid:])
            return merge(left, right)

        return mergeSort(nums)
        
        