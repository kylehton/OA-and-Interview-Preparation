from typing import List

# we use an indegree list for counts, adding each 0-dep
# into queue. we then iterate through the length of the queue

from collections import defaultdict, deque

class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        indegree = [0 for _ in range(numCourses)]
        prereq = defaultdict(list)
        for prerequisite in prerequisites:
            prereq[prerequisite[1]].append(prerequisite[0])
            indegree[prerequisite[0]] += 1

        queue = deque()
        coursesTaken = 0
        for i in range(len(indegree)):
            if indegree[i] == 0:
                queue.append(i)
        
        while queue:
            course = queue.popleft()
            coursesTaken += 1
            for dep in prereq[course]:
                indegree[dep] -= 1
                if indegree[dep] == 0:
                    queue.append(dep)

        return coursesTaken == numCourses
