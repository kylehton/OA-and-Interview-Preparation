# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# we can go down in sublevel recursively
# for each parent node, we sum the lengths of the left and right subtree
# we compare that to a global max variable
# return the max global variable at end of func

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        total_max = 0
        
        def tree_recur(curr):
            nonlocal total_max
            if not curr:
                return 0
            left_sum = tree_recur(curr.left)
            right_sum = tree_recur(curr.right)
            total_sum = left_sum + right_sum
            total_max = max(total_max, total_sum)
            return max(left_sum, right_sum) + 1
        
        tree_recur(root)
        return total_max
