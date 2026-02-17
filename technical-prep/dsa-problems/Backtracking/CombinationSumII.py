class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        def recur(curr_sum, curr_arr, index, res):
            if curr_sum == target:
                res.append(curr_arr[:])
                return
            if index < len(candidates):
                curr_sum += candidates[index]
                curr_arr.append(candidates[index])

                recur(curr_sum, curr_arr, index+1, res)

                curr_sum -= candidates[index]
                curr_arr.pop()
                while index+1 < len(candidates) and candidates[index] == candidates[index+1]:
                    index += 1
                recur(curr_sum, curr_arr, index+1, res)
            return
        
        candidates.sort()
        result = []
        recur(0, [], 0, result)
        return result
        