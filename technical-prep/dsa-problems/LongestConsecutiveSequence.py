# we are searching for longest subseq.
# in generating a subseq, we can save time complexity by starting at
# only items that do not have its previous element in list
# for O(n), we can insert all into a hashmap/set

class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        item_set = set()
        for num in nums:
            item_set.add(num)

        max_len = 0
        for num in nums:
            if num-1 not in item_set:
                curr_len = 1
                temp = num
                while temp+1 in item_set:
                    curr_len += 1
                    temp += 1
                max_len = max(max_len, curr_len)
        return max_len
                