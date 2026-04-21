from typing import List

# we can use a open and close count in backtracking,
# where we enforce open >= close, and upon close == n,
# we check validity and add to result

class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        def checkParenthesis(string: str) -> bool:
            stack = []
            for char in string:
                if char == '(':
                    stack.append(char)
                else:
                    if len(stack) == 0:
                        return False
                    stack.pop()
            if len(stack) > 0:
                return False
            return True
        
        result = []
        def backtrack(string: str):
            nonlocal result, n
            if (len(string)//2) >= n:
                if checkParenthesis(string):
                    result.append(string[:])
                return string
        
            backtrack(string+')')
            backtrack(string+'(')
            
            return string

        backtrack("")
        return result
