# in order to optimize the order the tasks are in, we should start with
# and distribute the task with most occurrences, so we can use a 
# max heap to store all occurrence values
# we dont want to update the maxheap immediately since that would not
# follow the n time after constraint, so we can use a queue
# for timed updates into the max heap

import heapq
from collections import deque

class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        task_dict = {}
        for task in tasks:
            task_dict[task] = task_dict.get(task,0) + 1
        
        heap = []
        for task, count in task_dict.items():
            heapq.heappush(heap, -count)
        
        curr_time = 0
        queue = deque()
        while heap or queue:
            curr_time += 1
            if heap:
                count = heapq.heappop(heap) + 1
                if count != 0:
                    queue.append((count, curr_time+n))
            if queue and queue[0][1] == curr_time:
                heapq.heappush(heap, queue.popleft()[0])
            
        return curr_time
