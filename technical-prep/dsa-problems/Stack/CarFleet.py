import math
from typing import List

class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        car_map = {}
        for i in range(len(position)):
            car_map[position[i]] = speed[i]
        position.sort()
        stack = []
        for i in range(len(position)-1, -1, -1):
            if not stack or stack[-1] < ((target-position[i])/car_map[position[i]]):
                stack.append((target-position[i])/car_map[position[i]])
        return len(stack)