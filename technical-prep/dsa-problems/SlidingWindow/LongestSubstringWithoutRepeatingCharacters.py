# we can use a sliding window implementation
# using the window, we build it up as long as no new chars are in set
# if in set, we remove that char from the set and increment l pointer

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        l = r = 0
        currMax = 0
        seen = set()

        while r < len(s):
            while s[r] in seen:
                currMax = max(currMax, len(seen))
                seen.remove(s[l])
                l += 1
            seen.add(s[r])
            r += 1

        return max(currMax, len(seen))
            
        