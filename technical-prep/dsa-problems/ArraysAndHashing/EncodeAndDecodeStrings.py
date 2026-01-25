# we can use any character as a delimiter, with a string len count
# for example, we append before the string a #%, where the % indicates
# the completion of the length of the string that is to follow
# regardless of that format being present within the string,
# it gets considered as part of the string that follows since it is
# bounded by its length

class Solution:

    def encode(self, strs: list[str]) -> str:
        encoded_str = ''
        for string in strs:
            encoded_str += str(len(string)) + '%' + string
        return encoded_str

    # need to take in the entire string, keep iterating til delimiter
    # intake before delimiter is casted to int (after full str of int)
    # must keep track of index while iterating to find starting index
    # for curr string.
    # loop must vary based on length of string that is encoded,
    # to ensure we only ever begin at the beginning of an encoding with
    # the proper length-delimiter prefix
    def decode(self, s: str) -> list[str]:
        decoded_strs = []
        i = 0
        while i < len(s):
            s_len = ''
            while s[i] != '%':
                s_len += s[i]
                i += 1
            s_len = int(s_len)
            curr_str = s[i+1:i+1+s_len]
            decoded_strs.append(curr_str)
            i += s_len + 1
        
        return decoded_strs
            


