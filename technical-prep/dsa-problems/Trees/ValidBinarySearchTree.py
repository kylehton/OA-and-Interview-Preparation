from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# we need to traverse in order to check ordering values
# for each node, check l and r, return False if wrong
# base case return back up if root is None

class Solution:

    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def dfs(curr, leftBound, rightBound):
            if not curr:
                return True
            if curr.val >= rightBound or curr.val <= leftBound:
                return False
            return dfs(curr.left, leftBound, curr.val) and dfs(curr.right, curr.val, rightBound)
    
        return dfs(root, float("-inf"), float("inf"))
        
