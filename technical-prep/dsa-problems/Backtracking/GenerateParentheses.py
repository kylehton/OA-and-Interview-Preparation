# we could do backtracking and have a check at the end using a stack
# given that we know n is from 1-7, it adds at most, O(7)

class Solution:
    def check_parenthesis(self, s: str):
        stack = []
        for char in s:
            if char == '(':
                stack.append(char)
            else:
                if len(stack) == 0:
                    return False
                stack.pop()
        if len(stack) > 0:
            return False
        return True

    def generateParenthesis(self, n: int) -> list[str]:
        # we need to keep trying combos until len(str) = n
        # base case: len = n, helper func. to check
        # add or not depending on helper res
        # need to pass: string, two sets of calls
        # one set for open, one for close, each have 2 for yes/no?
        result = []
        def genPar(curr_str: str, open_c: int, close_c: int):
            
            if open_c == close_c == n:
                print("curr len", len(curr_str)//2)
                print("curr_str:", curr_str, open_c, close_c)
                result.append(curr_str[:])
            elif open_c > n or close_c > n:
                return

            if open_c <= n:
                curr_str += '('
                genPar(curr_str, open_c+1, close_c)
                curr_str = curr_str[:len(curr_str)-1]
            
            if open_c > close_c:
                curr_str += ')'
                genPar(curr_str, open_c, close_c+1)
                curr_str = curr_str[:len(curr_str)-1]

        init_str = ""
        genPar(init_str, 0, 0)
        return result


