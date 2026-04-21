from typing import List

# essentially, water flows in from all sides, where top and left are pacific
# and bottom and right are atlantic. we want all indices where the box can be
# filled with water from both the pacific and atlantic
# we basically need to run a dfs from all borders and mark reachable squares in a set
# and repeat for pacific and atlantic. from that, we can then run through all indices
# and return a list of those that are present in both sets

from collections import deque

class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        def addToSet(water, row, col, reachable):
            if row < 0 or row >= len(heights) or col < 0 or col >= len(heights[0]) or heights[row][col] < water or (row, col) in reachable:
                return
            reachable.add((row, col))
            for dr, dc in DIRECTION:
                addToSet(heights[row][col], row+dr, col+dc, reachable)

        pacific, atlantic = set() , set()
        DIRECTION = [(1,0), (0,1), (-1,0), (0,-1)]
        
        for r in range(len(heights)):
            addToSet(heights[r][0], r, 0, pacific)
            addToSet(heights[r][len(heights[0])-1], r, len(heights[0])-1, atlantic)
        
        for c in range(len(heights[0])):
            addToSet(heights[0][c], 0, c, pacific)
            addToSet(heights[len(heights)-1][c], len(heights)-1, c, atlantic)
        
        result = []
        for row in range(len(heights)):
            for col in range(len(heights[0])):
                if (row, col) in pacific and (row, col) in atlantic:
                    result.append([row, col])
            
        return result
