from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# we use a pointer to iterate through the list
# we can append each k-grouping reverse linked list to a dummy node
# through each k-length iteration, we keep track of head and tail
# of sub-linked list, in which we point newNode to and set equal to


class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        def reverseList(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            while node:
                temp = node.next
                node.next = prev
                prev = node
                node = temp
            return prev

        curr = head
        returnHead = None
        newHead = ListNode()
        prevHead = head
        length = 1
        while curr:
            while curr and length < k:
                curr = curr.next
                length += 1
            if not returnHead:
                returnHead = curr
            if curr and length == k:
                nextHead = curr.next
                curr.next = None
                newHead.next = reverseList(prevHead) # type: ignore
                newHead = prevHead
                prevHead = nextHead
                curr = nextHead
                length = 1
            else:
                newHead.next = prevHead # type: ignore
                break

        return returnHead
            


        
