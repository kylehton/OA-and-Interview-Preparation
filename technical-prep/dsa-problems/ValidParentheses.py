# we can use a stack to implement a comparison algorithm
# all open brackets get placed in the stack, and upon a closing bracket
# the top element gets popped and compared

class Solution:
    def isValid(self, s: str) -> bool:
        brackets = {'(': ')', '{': '}', '[': ']'}
        stack = []

        for char in s:
            if char in brackets.keys():
                stack.append(char)
            else:
                if stack:
                    bracket_key = stack.pop()
                    if brackets[bracket_key] != char:
                        return False
                else:
                    return False
        
        if len(stack) == 0:
            return True
        else:
            return False

        