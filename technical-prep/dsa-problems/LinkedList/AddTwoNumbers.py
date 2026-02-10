from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# we can use a base 10 exponent computation to add values together
# we start at e = 0, adding one for each and multiplying up to add

# to convert back, we can convert to string and go piece by piece,
# casting to int for val

class Solution:

    def linkToInt(self, numList):
        exp = 0
        curr_num = 0
        while numList:
            curr_num += numList.val * (10**exp)
            exp += 1
            numList = numList.next
        return curr_num

    def intToLink(self, num):
        numStr = str(num)
        numStr = numStr[::-1]
        newHead = ListNode()
        curr = newHead
        for char in numStr:
            newNode = ListNode()
            newNode.val = char
            curr.next = newNode
            curr = curr.next
        return newHead.next

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        return self.intToLink(self.linkToInt(l1) + self.linkToInt(l2))