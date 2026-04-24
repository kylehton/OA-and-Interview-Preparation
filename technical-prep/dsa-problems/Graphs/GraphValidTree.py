from typing import List

# detect cycles in graph
# run dfs from one node given an adjacency list, skipping its previous parent
# check against visited set, and if node alreayd visited, a cycle exists
# set cycle variable to True indicating a cycle, and one connected component 
# checked through validating len(visited) against n number of nodes

from collections import defaultdict, deque

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        def dfs(node, parent):
            nonlocal visited, adjList, cycle
            if node not in visited:
                visited.add(node)
                for neighbor in adjList[node]:
                    if neighbor != parent:
                        dfs(neighbor, node)
            else:
                cycle = True 

        adjList = defaultdict(list)
        for u, v in edges:
            adjList[u].append(v)
            adjList[v].append(u)
        
        visited = set()
        cycle = False
        if edges:
            dfs(edges[0][0], -1)
        else:
            return True

        return (len(visited) == n) and not cycle
    
        
                