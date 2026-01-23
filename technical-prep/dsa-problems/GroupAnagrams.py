# we can create a dict, where keys are the lettering and values are
# the string; key can be an array of 26 spaces

from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        count_dict = defaultdict(list)

        # add all strings into dict
        for s in strs:
            alphabet = [0] * 26
            for char in s:
                c_index = ord(char) - ord('a') # given: all lower
                alphabet[c_index] += 1
            ab_key = tuple(alphabet)
            count_dict[ab_key].append(s)
        
        result = []
        for _, s_list in count_dict.items():
            result.append(s_list)
        
        return result