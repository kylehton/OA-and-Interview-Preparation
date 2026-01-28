# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# 1 -> 2 -> 3
# prev = 1, curr = 2
# temp = curr.next (temp = 3)
# curr.next = prev (2 -> 1)
# prev = curr
# curr = temp


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        prev = None
        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev
