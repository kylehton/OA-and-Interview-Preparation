from typing import List

# we can essentially run the same pattern as previous Course Sched.
# where we use an adj list and a count tracking list for validity
# we then maintain a list of courses taken, inserted on order of 
# insertion into queue as a valid course taken

from collections import defaultdict, deque

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        prereq = defaultdict(list)
        indegree = [0 for _ in range(numCourses)]
        for edge in prerequisites:
            prereq[edge[1]].append(edge[0])
            indegree[edge[0]] += 1
        
        queue = deque()
        for i in range(len(indegree)):
            if indegree[i] == 0:
                queue.append(i)
        
        courseList = []
        while queue:
            course = queue.popleft()
            courseList.append(course)
            if course in prereq:
                for dep in prereq[course]:
                    indegree[dep] -= 1
                    if indegree[dep] == 0:
                        queue.append(dep)

        if len(courseList) == numCourses:
            return courseList
        return []
        

