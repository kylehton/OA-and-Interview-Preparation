# in this sort of problem we can use a monotonic stack
# we want to keep the stack in decreasing order
# we store the temperature and index in a stack
# upon reaching a higher temperature, we want to pop all lower temps
# from stack, and update result array using the stored index

class Solution:
    def dailyTemperatures(self, temperatures: list[int]) -> list[int]:
        tempStack = []
        result = [0] * len(temperatures)

        tempStack.append([temperatures[0], 0]) # (temp, index)

        for i in range(1, len(temperatures)):
            while temperatures[i] > tempStack[len(tempStack)-1][0]:
                result[tempStack[-1][1]] = i - tempStack[-1][1]
                tempStack.pop()
                if len(tempStack) == 0:
                    break
            tempStack.append((temperatures[i], i))
        
        return result
            

            
            