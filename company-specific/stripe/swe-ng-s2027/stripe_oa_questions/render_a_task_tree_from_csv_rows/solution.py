from typing import List

# THIS IS ESSENTIALLY THE BUILD A TASK AND SUBTASK HIERARCHY WITH MORE THAN ONE SUBLEVEL

# root has 4 fields, sub has 5
# all tasks retain input order
# need to build this to accomodate subtasks of subtasks
# we can have function to print a root and all its
# subtasks, in which we can call recursively
# constraints show that all graphs are acyclic so no need for
# seen check

class Solution:
  def renderTaskTree(self, rows: List[str]) -> List[str]:

    # this function only runs for subtasks, so instantiates with
    # prefix = "|- "
    def getTaskTree(tid, i, prefix, arr):
      subtask_array = subtaskDict[tid]
      taskId, taskName = subtask_array[i]
      task_string = None
      
      if i == len(subtask_array)-1:
        task_string = prefix[:len(prefix)-3] + "\- " + taskId + " " + taskName
      else:
        task_string = prefix + taskId + " " + taskName
        
      arr.append(task_string)
      if taskId in subtaskDict:
        recur_arr = subtaskDict[taskId]
        for i in range(len(recur_arr)):
          getTaskTree(taskId, i, "  " + prefix, arr)
    
      return arr
      
    rootTasks = []
    subtaskDict = {}

    for row in rows:
      parts = row.strip().split(',')
      operation = parts[1].strip()
      
      if operation == 'task':
        _, _, taskId, taskName = parts
        rootTasks.append((taskId, taskName))
      elif operation == 'subtask':
        _, _, parentId, taskId, taskName = parts
        if parentId not in subtaskDict:
          subtaskDict[parentId] = []
        subtaskDict[parentId].append((taskId, taskName))

    result = []
    for task in rootTasks:
      taskId, taskName = task
      task_string = taskId + " " + taskName
      result.append(task_string)
      if taskId in subtaskDict:
        for i in range(len(subtaskDict[taskId])):
          getTaskTree(taskId, i, "|- ", result)

    return result
      