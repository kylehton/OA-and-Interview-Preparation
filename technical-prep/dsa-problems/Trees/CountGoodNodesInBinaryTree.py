# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        total_max = 0
        def dfs(curr_node, curr_max):
            nonlocal total_max
            if not curr_node:
                return
            if curr_node.val >= curr_max:
                total_max += 1

            curr_max = max(curr_max, curr_node.val)
            
            dfs(curr_node.left, curr_max)
            dfs(curr_node.right, curr_max)
            return
        
        dfs(root, -float('inf'))
        return total_max