# we can use a stack to hold numbers
# upon seeing an operator, we pop the top 2 elements from the stack
# we perform the operation on those two elements, and push result
# to stack again. 

class Solution:
    def evalRPN(self, tokens: list[str]) -> int:
        stack = []
        for elem in tokens:
            if elem not in {"+", "-", "*", "/"}:
                stack.append(int(elem))
            else:
                elem2 = stack.pop()
                elem1 = stack.pop()
                print(type(elem2), type(elem1))
                if elem == '+':
                    stack.append(elem1 + elem2)
                elif elem == '-':
                    stack.append(elem1 - elem2)
                elif elem == '*':
                    stack.append(elem1 * elem2)
                elif elem == '/':
                    stack.append(int(elem1 / elem2))
        final_res = stack.pop()
        return int(final_res)