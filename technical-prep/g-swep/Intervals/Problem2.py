'''
Given a string s, find the length of the longest substring without duplicate characters.

Example 1:
Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3. Note that "bca" and "cab" are also correct answers.

Example 2:
Input: s = "bbbbb"
Output: 1
Explanation: The answer is "b", with the length of 1.

Example 3:
Input: s = "pwwkew"
Output: 3
Explanation: The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.
'''

# we can use a sliding window with a current count of the largest char
# this runs a total of 

def lengthOfLongestSubstring(s: str) -> int:
    window = set()
    curr_max = 0
    l, r = 0, 1
    window.add(s[l])
    while r < len(s):
        if s[r] not in window:
            window.add(s[r])
        else:
            while s[r] in window:
                window.remove(s[l])
                l += 1
            window.add(s[r])
        r += 1
        curr_max = max(curr_max, len(window))
    return curr_max


s1 = "abcabcbb" # result: 3
s2 = "bbbbb" # result: 1
s3  = "pwwkew" # result: 3

print(lengthOfLongestSubstring(s1))
print(lengthOfLongestSubstring(s2))
print(lengthOfLongestSubstring(s3))