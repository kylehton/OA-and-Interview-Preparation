from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# we can recursively go down to leaves, as base case
# we return upward for each node the local max path sum for left subtree
# right subtree, and excluding both (just the node value)
# we max all of those with 0, returning upwards the maximum
# we compare this to a global maximum variable

class Solution:
    def maxPathSum(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        globalMax = root.val
        def calcPathSum(node):
            nonlocal globalMax
            if not node:
                return 0
            left = calcPathSum(node.left)
            right = calcPathSum(node.right)
            localMax = node.val + max(0, left, right)
            # we check local root sum since we cannot return upward, since it spans
            # both left and right subtrees, validating the current node as root
            localRootSum = node.val+left+right 
            globalMax = max(globalMax, localMax, localRootSum)  

            return localMax

        calcPathSum(root)
        return globalMax