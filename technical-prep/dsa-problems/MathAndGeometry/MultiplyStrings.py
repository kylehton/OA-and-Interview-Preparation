# not optimal solution

class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        char_to_num = {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "0": 0}

        n1, n2 = len(num1)-1, len(num2)-1
        digit1, digit2 = 0, 0
        exp = 0
        while n1 >= 0:
            digit1 += char_to_num[num1[n1]] * (10**exp)
            exp += 1
            n1 -= 1

        exp = 0

        while n2 >= 0:
            digit2 += char_to_num[num2[n2]] * (10**exp)
            exp += 1
            n2 -= 1

        print(digit1, digit2)
        return str(digit1 * digit2)
        