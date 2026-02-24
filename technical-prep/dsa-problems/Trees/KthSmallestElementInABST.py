from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:
        curr_index = 0
        val_to_return = 0
        def dfs(node):
            nonlocal curr_index, val_to_return
            #nonlocal all_nodes
            if not node:
                return
            dfs(node.left)
            curr_index += 1
            if curr_index == k:
                val_to_return = node.val
                return
            elif curr_index < k:
                dfs(node.right)
            else:
                return
        
        dfs(root)
        return val_to_return

