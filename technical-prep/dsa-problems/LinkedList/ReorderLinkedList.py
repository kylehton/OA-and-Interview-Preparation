from typing import Optional

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# we can split into two linked lists, where its the first half
# and second half
# we reverse the second half
# we alternate adding into the head

class Solution:

    def reorderList(self, head: Optional[ListNode]) -> None:
        # find center
        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        # reverse second part of linked list
        reverse = slow.next
        prev = slow.next = None
        # prev 
        # n1 -> n2 -> n3
        # prev = n1, reverse = n2, reverse.next = n3
        # temp = reverse.next
        # reverse.next = prev
        # prev = reverse
        # reverse = temp
        while reverse:
            temp = reverse.next
            reverse.next = prev
            prev = reverse
            reverse = temp

        l1, l2 = head, prev
        while l2:
            temp1 = l1.next
            temp2 = l2.next
            l1.next = l2
            l2.next = temp1
            l1 = temp1
            l2 = temp2
 
        