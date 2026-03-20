# we know that the left parentheses and asterick come before
# need to validate left - right, and that asterick comes
# after left parenthesis index to check
class Solution:
    def checkValidString(self, s: str) -> bool:
        left = []
        asterick = []
        right = []
        for i in range(len(s)):
            char = s[i]
            if char == '(':
                left.append(i)
            elif char == '*':
                asterick.append(i)
            else:
                if len(left) > 0:
                    left.pop()
                elif len(asterick) > 0:
                    asterick.pop()
                else:
                    return False

        while left and asterick:
            l = left.pop()
            a = asterick.pop()
            if l > a:
                return False

        return len(left) == 0