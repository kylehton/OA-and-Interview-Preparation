from typing import List

# we need to create an object where:
# we can have a set of followers for each user, supporting an O(1) add and delete
# we also need a dict of all posts by each user, where we append to the end
# for all posts so it remains in order

# when finding the 10 most recent tweets, we can use a heap. since we use an int index to
# track time, we want the largest time (most recent) at the top
# we can insert them as negative time into the heap

from collections import defaultdict
import heapq

class Twitter:

    def __init__(self):
        self.timeCount = 0
        self.userToFollows = defaultdict(set)
        self.userToPosts = defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.userToPosts[userId].append((self.timeCount, tweetId))
        self.timeCount -= 1

    def getNewsFeed(self, userId: int) -> List[int]:
        heap = []
        result = []
        self.userToFollows[userId].add(userId) # look through self feed 
        for user in self.userToFollows[userId]:
            index = len(self.userToPosts[user])-1 # most recent
            # we want to use the above index to look through
            # the next most recent tweet each time we add this most
            # recent one to heap and result
            if index >= 0:
                time, tid = self.userToPosts[user][index]
                heapq.heappush(heap, (time, tid, user, index-1))
        
        # heap initialized with most recent tweet per user in following
        while heap and len(result) < 10:
            top = heapq.heappop(heap)
            result.append(top[1]) # add tweet id
            if top[3] >= 0: # valid index for tweet
                user, index = top[2], top[3]
                time, tid = self.userToPosts[user][index]
                heapq.heappush(heap, (time, tid, user, index-1))
    
        return result

    def follow(self, followerId: int, followeeId: int) -> None:
        self.userToFollows[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.userToFollows[followerId]:
            self.userToFollows[followerId].remove(followeeId)
