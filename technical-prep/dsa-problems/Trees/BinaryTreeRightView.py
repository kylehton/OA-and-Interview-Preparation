from typing import Optional
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> list[int]:
        result = []
        queue = deque()
        queue.append(root)

        while queue:
            rightNode = None

            for i in range(len(queue)):
                curr = queue.popleft()
                if curr:
                    rightNode = curr
                    queue.append(curr.left)
                    queue.append(curr.right)
            if rightNode is not None:
                result.append(rightNode.val)
                
        return result
        


