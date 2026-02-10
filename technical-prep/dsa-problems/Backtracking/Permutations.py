# we want all possible permutations
# what we can do is use a backtracking algorithm
# we recursively loop through all possible additions
# where the base case is an array of correct length

class Solution:
    def permute(self, nums: list[int]) -> list[list[int]]:
        def buildPermutation(numList, result):
            if len(numList) == len(nums):
                result.append(numList[:])
                return
            for num in nums:
                if num not in numList:
                    numList.append(num)
                    buildPermutation(numList, result)
                    numList.pop()
            return
        
        res = []
        buildPermutation([], res)
        return res
            