# we need to store multiple values for same key, as specific time stamps
# retrieve value for key at a given timestamp
# since set() is called in increaing timestamp, we just append to end to maintain sorted
# order, per key in a dict of lists
# for get(), we want the most recent timestamp for that key, given that set was called on it.
# the latter part is wording for 'exists in key's list', and since we have the list in order
# we can run binary search on the list to find the closest point less than or equal to
# the timestamp parameter

from collections import defaultdict

class TimeMap:

    def __init__(self):
        self.store = defaultdict(list)

    def set(self, key: str, value: str, timestamp: int) -> None:
        self.store[key].append((value, timestamp))

    def get(self, key: str, timestamp: int) -> str:
        print(key, timestamp)
        if key in self.store:
            values = self.store[key]
            l, r = 0, len(values)-1
            while l <= r:
                mid = (l+r)//2
                if values[mid][1] == timestamp:
                    return values[mid][0]
                elif values[mid][1] > timestamp:
                    r = mid-1
                else:
                    l = mid+1
            if values[r][1] <= timestamp:
                return values[r][0]
        return ""
        
