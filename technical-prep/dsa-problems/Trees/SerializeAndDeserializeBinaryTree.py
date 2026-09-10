from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# combine into string for level order
# use null for no node placeholder
# delimiter for val separation, split on that
# increment each by 2 for each parent + two children

from collections import deque

class Codec:
    
    # Encodes a tree to a single string.
    def serialize(self, root: Optional[TreeNode]) -> str:
        encoding = ""
        queue = deque()
        queue.append(root)
        while queue:
            curr = queue.popleft()
            if curr:
                encoding += str(curr.val) + "&"
                queue.append(curr.left)
                queue.append(curr.right)
            else:
                encoding += "null" + "&"
        return encoding
    
        
    # Decodes your encoded data to tree.
    def deserialize(self, data: str) -> Optional[TreeNode]:
        nodes = data.strip().split('&')
        queue = deque()
        root = None
        index = 0
        if nodes[index] != '' and nodes[index] != 'null':
            root = TreeNode()
            root.val = nodes[index] # type: ignore
            queue.append(root)
        while queue and index < len(nodes)-2:
            parent = queue.popleft()
            left = nodes[index+1]
            right = nodes[index+2]
            if parent != "null":
                if left != '':
                    if left != 'null':
                        parent.left = TreeNode()
                        parent.left.val = left # type: ignore
                        queue.append(parent.left)
                if right != '':
                    if right != 'null':
                        parent.right = TreeNode()
                        parent.right.val = right # type: ignore
                        queue.append(parent.right)
            index += 2
        
        return root
        