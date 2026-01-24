from collections import defaultdict

class Solution:

    def str_to_dict(s: str) -> dict:
        str_dict = defaultdict(str)
        for char in s:
            str_dict[char] += 1
        return str_dict


    def isAnagram(self, s: str, t: str) -> bool:

        def str_to_dict(s: str) -> dict:
            str_dict = defaultdict(int)
            for char in s:
                str_dict[char] += 1
            return str_dict

        if len(s) != len(t):
            return False
        s_dict = str_to_dict(s)
        t_dict = str_to_dict(t)

        for char, _ in s_dict.items():
            if char in t_dict:
                if s_dict[char] != t_dict[char]:
                    return False
            else:
                return False
        
        return True