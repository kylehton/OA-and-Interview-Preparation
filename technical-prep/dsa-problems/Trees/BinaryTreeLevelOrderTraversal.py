# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# we should use a BFS -> queue

from collections import deque

class Solution:

    def levelOrder(self, root: Optional[TreeNode]) -> list[list[int]]:
            if not root:
                return []

            tree_q = deque()
            tree_q.append(root)

            result = []

            while tree_q:
                curr = []
                for i in range(len(tree_q)):
                    if len(tree_q) > 0:
                        currNode = tree_q.pop()
                    else:
                        break
                    if currNode is None:
                        continue
                    else:
                        curr.append(currNode.val)
                        tree_q.appendleft(currNode.left)
                        tree_q.appendleft(currNode.right)
                if curr:
                    result.append(curr)
            
            return result
            
