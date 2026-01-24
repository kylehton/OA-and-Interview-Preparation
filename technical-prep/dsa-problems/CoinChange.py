# we can use an array corresponding to change values as index
# using this array, we store whatever minimum # of coins for each index
# we reuse that in later computations
# we must set to a variable that cannot be less than any possible # of coins
# given the smallest coin (1), the largest amount of coins is amount itself
# we need change from 0 - amount inclusive, so alloc. amount+1 indices

class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        change_arr = [amount+1] * (amount+1)
        change_arr[0] = 0 # base case or else 0 -> amount+1
        for amt in range(1, amount+1): # find ways to make this amount
            for coin in coins:
                if amt-coin >= 0: # if can be subtracted to reach amount
                    # update cache with any value less than the impossible one
                    # if cache call fails, it will stay at imposs. amount
                    # gets relayed for all larger amt calls, keeping it at imposs.
                    change_arr[amt] = min(change_arr[amt], 1+change_arr[amt-coin])

        # if changed, return that count
        return change_arr[amount] if change_arr[amount] != (amount + 1) else -1