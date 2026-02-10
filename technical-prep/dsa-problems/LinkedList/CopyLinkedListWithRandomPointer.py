from typing import Optional
# Definition for a Node.

class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random


# we need to split the logic for random pointer assignment
# since random has no order, we cannot assign while creating
# the new linked list, since it could point to a current None
# we can use a hashmap to store corresponding copies, so when it is time
# to point to a node in random, we have a quicker lookup time

# newHead needs to point to a new Node with curr.val
# 

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        nodeToNode = {}
        curr = head
        newHead = Node(0)
        temp = newHead
        while curr:
            temp.next = Node(curr.val)
            nodeToNode[curr] = temp.next
            temp = temp.next
            curr = curr.next
        
        # for the current original node in head
        # we need to point the new node to the NEW random
        # use the hashmap to find the new of orig, and 
        # the new of the random
        while head:
            if head.random: # random points to node
                nodeToNode[head].random = nodeToNode[head.random]
            else: # no random pointer val
                nodeToNode[head].random = None
            head = head.next
        
        return newHead.next


