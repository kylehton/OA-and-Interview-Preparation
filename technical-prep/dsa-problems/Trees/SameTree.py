from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        p_list = []
        q_list = []
        def dfs(node, node_list):
            if not node:
                node_list.append('null')
                return

            node_list.append(node.val)
            dfs(node.left, node_list)
            dfs(node.right, node_list)
            return

        dfs(p, p_list)
        dfs(q, q_list)
        print(p_list, q_list)

        if len(p_list) != len(q_list):
            return False
        for i in range(len(p_list)):
            if p_list[i] != q_list[i]:
                return False
        
        return True