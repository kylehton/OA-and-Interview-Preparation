from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# if we run through dfs normally on a BST, we will always go from smallest to largest
# as such, we can keep a running count after recursive returns upward, and when the count
# equals k, we set some global variable to return that value

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        kthValue = 0
        count = 0
        def dfs(node):
            nonlocal kthValue, count
            if not node:
                return
            dfs(node.left)
            count += 1
            if count == k:
                kthValue = node.val
            dfs(node.right)
            return
        
        dfs(root)
        return kthValue

