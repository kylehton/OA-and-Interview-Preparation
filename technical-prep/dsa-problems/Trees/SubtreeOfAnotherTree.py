from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:   
    def isSubtree(self, root: Optional[TreeNode], subRoot: Optional[TreeNode]) -> bool:
        allNodes = []
        subNodes = []
        def dfs(node, node_list):
            if not node:
                node_list.append(None)
                return
            node_list.append(node.val)
            dfs(node.left, node_list)
            dfs(node.right, node_list)
            return
        
        dfs(root, allNodes)
        dfs(subRoot, subNodes)
        if len(allNodes) < len(subNodes):
            return False
        print(allNodes, subNodes)
        for i in range(len(allNodes)):
            x = i
            y = 0
            if allNodes[x] == subNodes[y]:
                while y < len(subNodes) and allNodes[x] == subNodes[y]:
                    x += 1
                    y += 1
                if y == len(subNodes):
                    return True

        return False
        
