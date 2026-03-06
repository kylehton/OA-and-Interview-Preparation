from collections import deque
from typing import List

# we can use traversal to explore from each starting course w no prereq
# we first should iterate through all and add them into some sort of 
# adjacency list, where key = prereq, val = list of eligible courses
# we can run a dfs or bfs on this, adding them to a visited set.
# ideally we want to end on a course that is NOT a key, but if we find it
# in the visited set, we know there exists a cycle
 
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        course_dict = {}
        max_count = 0
        for pair in prerequisites:
            prereq = pair[1]
            depend = pair[0]
            if prereq not in course_dict:
                course_dict[prereq] = []
            course_dict[prereq].append(depend)
        
        queue = deque()
        all_visited = set()
        for prereq in course_dict.keys():
            count = 0
            if prereq not in all_visited:
                all_visited.add(prereq)
                visited = set()
                queue.append(prereq)
                while queue:
                    item = queue.popleft()
                    if item not in visited:
                        visited.add(item)
                        if item in course_dict:
                            for dep in course_dict[item]:
                                if dep not in all_visited:
                                    queue.append(dep)
                                elif dep in visited:
                                    return False
                    count += 1
            max_count = max(max_count, count)
        
        return (max_count <= numCourses)