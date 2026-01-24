# we can sum both sequences together in one loop
# we can use two variables, and upon summing one with the next avail,
# we swap the two so that the other variable also get summed

# path1 becomes the current adjacent sum
# path2 retains the previous adjacent sum (other sequence)
# curr_max compares the two sums and stores the larger one
# if path1 sums the current num, we update path2 to equal the largest
# sum, to retain the current largest sum

# [2, 9, 8, 3, 6]
# path1 = 0 -> 0 -> 2 -> 9 -> 10 -> 12 -> DONE (current adjacent path sum)
# path2 = 0 -> 2 -> 9 -> 10 -> 12 -> 16 -> DONE (previous adjacent path sum)
# curr_max = 0+2 -> 0+9 -> 2+8 -> 9+3 -> 10+6 -> DONE (maximum of the two path sums at the current index)


class Solution:
    def rob(self, nums: list[int]) -> int:
        path1 = 0
        path2 = 0

        for num in nums:
            curr_max = max(path1 + num, path2)
            path1 = path2
            path2 = curr_max
        
        return path2 # can return path2 since at the end of each loop, path2 is updated to the maximum path sum