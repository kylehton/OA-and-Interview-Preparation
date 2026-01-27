
class Interval(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end


# we can sort based on the start attribute of object Interval
# we can iterate through the entire sorted list,
# comparing a given object end time with the next start time
# upon conflict, we return False
# else, we return True after all checked

class Solution:
    def canAttendMeetings(self, intervals: list[Interval]) -> bool:
        intervals.sort(key=lambda x: x.start)
        for i in range(len(intervals)-1):
            curr = intervals[i]
            next = intervals[i+1]
            if next.start < curr.end:
                return False
        return True