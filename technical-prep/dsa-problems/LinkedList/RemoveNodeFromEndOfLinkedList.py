# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# we use a fast-slow pointer combination, where we use a stopgap
# approach ebtween two pointers. the slow pointer tracks the actual
# index to remove while the fast pointer tells us when to stop after
# certain number of iterations

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        
        newHead = ListNode()
        newHead.next = head
        slow = newHead
        fast = newHead

        for i in range(n):
            fast = fast.next
    
        while fast.next:
            slow = slow.next
            fast = fast.next

        slow.next = slow.next.next

        return newHead.next
