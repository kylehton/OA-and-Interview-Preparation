from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        result = []
        def backtrack(arr: list[int], currSum: int, index: int):
            nonlocal result
            if currSum >= target:
                if currSum == target:
                    result.append(arr[:])
                return arr
            
            i = index
            while i < len(candidates):
                arr.append(candidates[i])
                backtrack(arr, currSum+candidates[i], i+1)
                arr.pop()
                while i < len(candidates)-1 and candidates[i] == candidates[i+1]:
                    i += 1
                i += 1
            
            return arr
        
        backtrack([], 0, 0)
        return result