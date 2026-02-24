# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def lowestCommonAncestor(self, root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
        p_set = set()
        q_list = []

        p_head = root
        q_head = root

        while p_head and p_head != p:
            p_set.add(p_head)
            if p_head.val == p.val:
                break
            if p_head.val > p.val:
                p_head = p_head.left
            else:
                p_head = p_head.right
            
        while q_head and q_head != q:
            q_list.append(q_head)
            if q_head.val == q.val:
                break
            if q_head.val > q.val:
                q_head = q_head.left
            else:
                q_head = q_head.right
        
        print("p set:")
        for node in p_set:
            print(node.val)
        print("q list:")
        for node in q_list:
            print(node.val)

        for i in range(len(q_list)-1, -1, -1):
            if q_list[i] in p_set:
                return q_list[i]
    