from typing import List

# we can build the string using backtracking
# we essentially build each string until we account for all possible
# elems in a list

# we can use an index elem usage
# we loop through bool list on each recursive call
# adding each returned True to the curr

class Solution:
    def partition(self, s: str) -> List[List[str]]:
        def isPalindrome(word: str) -> bool:
            for i in range(len(word)//2):
                if word[i] != word[len(word)-i-1]:
                    return False
            return True
        
        result = []
        def backtrack(arr: List[str], index: int):
            nonlocal result, s

            if index == len(s):
                result.append(arr[:])
                return arr
            
            for i in range(index, len(s)):
                substr = s[index:i+1]
                if isPalindrome(substr):
                    arr.append(substr)
                    backtrack(arr, i+1)
                    arr.pop()

            return arr

        backtrack([], 0)
        return result

        