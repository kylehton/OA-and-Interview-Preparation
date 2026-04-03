'''
Given a list of timestamp ranges, each range represents a user using a Google service. Write a 
function that returns all users using the Google services at specific query timestamp.
A range can be represented as: [starting, ending], e.g., [1, 3] or [0, 10] and so on.

For instance, given a list of ranges:
[0, 5]
[6, 8]
[2, 9]
[4, 10]
[3, 5]

Searching through the above with a query timestamp of 3 should return:
[0, 2, 4]
because [0, 5], [2, 9], [3, 5] contain timestamp 3.
'''

def users_at_timestamp(ranges: list, timestamp: int) -> list:
    result = []
    for i in range(len(ranges)):
        if ranges[i][0] <= timestamp <= ranges[i][1]:
            result.append(i)
    return result

ranges = [[0, 5], [6, 8], [2, 9], [4, 10], [3, 5]]
timestamp = 3
print(users_at_timestamp(ranges, timestamp))