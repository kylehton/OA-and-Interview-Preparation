# NOT in NC 150

from typing import Optional, List

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# preorder builds: root -> left -> right
# in order builds: left -> root -> right
# for every subtree, size of inorder//2 = root

#                           1
#           2                               3
#    4             5                6               7
# 8     9      10     11        12     13       14      15

# preorder = [1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, 7, 14, 15]
# inorder = [8, 4, 9, 2, 10, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15]

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        inorder_index = {}
        for index, value, in enumerate(inorder):
            inorder_index[value] = index
        
        curr_root_index = 0

        def build_dfs(left, right):
            nonlocal curr_root_index
            if right < left:
                return
            print(curr_root_index)
            curr_root = preorder[curr_root_index]
            curr_root_index += 1
            curr_mid = inorder_index[curr_root]
            new_root = TreeNode()
            new_root.val = curr_root
            new_root.left = build_dfs(left, curr_mid-1)
            new_root.right = build_dfs(curr_mid+1, right)
            return new_root
        
        return build_dfs(0, len(inorder)-1)
            
