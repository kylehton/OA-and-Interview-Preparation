# we need some char count structure to store all char counts within
# a given window. we keep a window of length of s1, comparing counts
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        def checkMatchDict(dict1, dict2):
            if len(dict2.keys()) < len(dict1.keys()):
                return False
            for key in dict1:
                if key not in dict2:
                    return False
                if dict2[key] != dict1[key]:
                    return False
            return True

        s1_count = {}
        for char in s1:
            s1_count[char] = s1_count.get(char, 0) + 1
        window = {}
        l, r = 0, 0
        while r < len(s2):
            while r < len(s2) and (r-l+1) <= len(s1):
                window[s2[r]] = window.get(s2[r], 0) + 1
                r += 1
            if checkMatchDict(s1_count, window):
                return True
            window[s2[l]] = window.get(s2[l]) - 1 # type: ignore
            l += 1
        return False

                
            
