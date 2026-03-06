from collections import deque
from typing import List
# we can use a visited set 
# we loop through each edge, checking it against the visited node set
# for nodes that are unvisited, we keep going until invalid,
# adding them into the visited set. after all possible ones are added
# we increment count by one, then continue. the condition to begin
# another count is the starting vertex in an edge NOT in visited set

# edge case: isolated vertices will show in n, but not in edge set
# use that to supplement edge-path component counting

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        edge_dict = {}
        for edge in edges:
            if edge[0] not in edge_dict:
                edge_dict[edge[0]] = []
            if edge[1] not in edge_dict:
                edge_dict[edge[1]] = []
            edge_dict[edge[0]].append(edge[1])
            edge_dict[edge[1]].append(edge[0])
        
        visited = set()
        queue = deque()
        count = 0
        for val in edge_dict.keys():
            if val not in visited:
                queue.append(val)
                visited.add(val)
                while queue:
                    node = queue.popleft()
                    for neighbor in edge_dict[node]:
                        if neighbor not in visited:
                            queue.append(neighbor)
                            visited.add(neighbor)
                count += 1
        if len(visited) < n:
            count += n-len(visited)
        return count

