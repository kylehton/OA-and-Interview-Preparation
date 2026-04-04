'''
Q1. Imagine we own a parking garage. All day, cars enter and exit. When a car enters, it takes a ticket 
from the gate machine. When a car exits, it returns the ticket to the gate machine. The machine prints 
the entry and exit time on each ticket. Now, it's the end of the day and we've got a big pile of 
tickets, and we want to figure out how many cars were in the garage at each time of the day.
Write a function that takes as input an integer N and a list tickets of size L, and returns a list 
result such that len(result) == N and result[i] == the number of elements of tickets such that 
entry <= i <= exit.

Example:
N = 5
tickets = [(1, 3), (2, 4)]
result = [0, 1, 2, 2, 1]
'''

# we can iterate by ticket, going through each range and adding 1 for each car -> O(n^2)

# can use result[i], can use same array to count entry and exit; ith time -> n num of entries, n+1

from collections import deque

def count_cars(n :int, tickets: list) -> list:
    result = [0 for _ in range(n)]
    enter = deque()
    exit = deque()
    curr = 0
    for ticket in tickets:
        enter.append(ticket[0])
        exit.append(ticket[1])
    for i in range(n):
        if enter and (i == enter[0]):
            curr += 1
            result[i] = curr
            enter.popleft()
        if exit and (i == exit[0]):
            result[i] = curr
            curr -= 1
            exit.popleft()
    return result

print(count_cars(5, [(1, 3), (2, 4)]))