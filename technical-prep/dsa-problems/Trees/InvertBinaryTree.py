from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        
        def invTree(self, root):
            if not root:
                return
            if root.left and root.right:
                temp = root.left
                root.left = root.right
                root.right = temp
            elif root.left:
                root.right = root.left
                root.left = None
            elif root.right:
                root.left = root.right
                root.right = None
            invTree(self, root.left)
            invTree(self, root.right)
            return
        
        invTree(self, root)
        return root
            