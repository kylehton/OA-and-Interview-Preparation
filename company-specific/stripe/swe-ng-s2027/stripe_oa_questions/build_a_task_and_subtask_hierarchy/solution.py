from typing import List

# to store, we can use a min-heap to keep the (date, id) sorting 
# as we pop from min heap, which will be populated ONLY with tasks
# we can check each id against a map of all subtasks keyed by the parent task
# this will have a value as a min heap, following the same as above

import heapq

class Solution:
  def printTaskHierarchy(self, lines: List[str]) -> List[str]:
    tasks = []
    subtasks = {}
    result = []

    for line in lines:
      parts = line.strip().split(',')
      item_type = parts[1].strip()
      if item_type == 'task':
        date, _, taskId, name = parts
        heapq.heappush(tasks, (date, taskId, name))
      elif item_type == 'subtask':
        date, _, subtaskId, parentId, name = parts
        if parentId not in subtasks:
          subtasks[parentId] = []
        heapq.heappush(subtasks[parentId], (date, subtaskId, name))

    while tasks:
      _, taskId, name = heapq.heappop(tasks)
      result.append(name)
      if taskId in subtasks:
        subtaskHeap = subtasks[taskId]
        while subtaskHeap:
          _, _, name = heapq.heappop(subtaskHeap)
          if len(subtaskHeap) > 0:
            result.append("|- "+ name)
          else:
            result.append("\- "+ name)

    return result
      