# we can use a stack to implement a comparison algorithm
# all open brackets get placed in the stack, and upon a closing bracket
# the top element gets popped and compared

class Solution:
    def isValid(self, s: str) -> bool:
        brackets = {'(' : ')', '{' : '}', '[' : ']'}
        stack = []
        for char in s:
            if char in brackets:
                stack.append(char)
            else:
                if not stack:
                    return False
                top = stack.pop()
                if char != brackets[top]:
                    return False     
        return not stack
