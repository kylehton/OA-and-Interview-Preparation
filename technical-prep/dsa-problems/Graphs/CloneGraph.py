from typing import Optional

# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        new_map = {}

        def dfs(curr):
            if curr in new_map:
                return new_map[curr]
            if curr:
                node_copy = Node()
                new_map[curr] = node_copy
                node_copy.val = curr.val
                for neighbor in curr.neighbors:
                    node_copy.neighbors.append(dfs(neighbor))
                return node_copy
            return None

        return dfs(node)