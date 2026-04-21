from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


# we need to clone each and every node, along with its deep copied neighbors
# we can build the nodes themselves first, then iterate through again and 
# connect its neighbors. 
# the input node is also always going to have 1 as the value, and the
# nodes are numbered 1 to n. as such, they are unique

# we can use a queue to go from each node, and add its neighbors

from collections import deque

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None
        
        node_copy = {}
        queue = deque()
        queue.append(node)
        node_copy[node.val] = Node(node.val)

        while queue:
            curr = queue.popleft()
            for neighbor in curr.neighbors:
                if neighbor.val not in node_copy:
                    node_copy[neighbor.val] = Node(neighbor.val)
                    queue.append(neighbor)
                node_copy[curr.val].neighbors.append(node_copy[neighbor.val])

        return node_copy[node.val]

            