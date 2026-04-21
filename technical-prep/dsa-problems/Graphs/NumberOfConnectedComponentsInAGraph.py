from typing import List

# we can create an adjacency list to traverse each component
# keeping track of each traversed node with a visited set
# while the current traversal runs, we check it against the len
# of the current set compared the the total number of nodes
# we then iterate through the dict checking nonvisited nodes and
# running our traversal through that

from collections import defaultdict, deque

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        visited = set()
        adjList = defaultdict(list)
        for edge in edges:
            adjList[edge[0]].append(edge[1])
            adjList[edge[1]].append(edge[0])
        
        count  = 0
        for node in range(n):
            if node not in visited:
                visited.add(node)
                queue = deque()
                queue.append(node)
                while queue:
                    top = queue.popleft()
                    for neighbor in adjList[top]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)
                count += 1
        
        return count

