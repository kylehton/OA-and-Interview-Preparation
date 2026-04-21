from typing import List, Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# we can reuse the lists input, where each input is the head of a linked list
# what we can do is run a merge on each pairing of linked lists, popping and reinserting
# back into the lists list itself. we repeat until the final length of lists == 1
# we then return that

class Solution:    
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        def mergeLists(node1, node2):
            newHead = ListNode()
            temp = newHead
            while node1 and node2:
                if node1.val < node2.val:
                    temp.next = node1
                    node1 = node1.next
                else:
                    temp.next = node2
                    node2 = node2.next
                temp = temp.next
            
            if node1:
                temp.next = node1
            elif node2:
                temp.next = node2
            
            return newHead.next


        while len(lists) > 1:
            for i in range(0, len(lists), 2):
                list1 = lists.pop()
                list2 = lists.pop()
                lists.append(mergeLists(list1, list2))
        
        if len(lists) > 0:
            return lists[0]

        
