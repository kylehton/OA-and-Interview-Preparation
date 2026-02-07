# we can use a count of nonmatching chars in a specific sequence
# we can keep increasing size of subwindow as long as nonmatch
# count is less than or equal to k
# we take that length of subwindow and possibly update global max
# to maintain count of most occurring char, we can use a dict

from collections import defaultdict

class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        charDict = defaultdict(int)
        maxStrLen = 0
        l = r = 0
        curr_count = 0
        while l <= r and r < len(s):
            charDict[s[r]] += 1
            print(charDict)
            curr_count = max(curr_count, charDict[s[r]])
            print(curr_count)
            if (r - l + 1) - curr_count <= k:
                maxStrLen = max(maxStrLen, (r-l+1))
            else:
                charDict[s[l]] -= 1
                l += 1
            r += 1
        
        return maxStrLen