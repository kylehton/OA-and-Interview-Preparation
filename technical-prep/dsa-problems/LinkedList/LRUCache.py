# we can use a map to store key-val pairs for O(1) get and delete operations
# the issue here is capacity and lru. we can check the curr len of keys list of the 
# dict, and we perform lru logic upon reaching the insertion of a new pair when len == k

# we need some way to remove something from any position in the cache in O(1)
# if we use a double linked list, we can do so. we need to set either head or tail as 
# front or end of cache, and on each operation, we remove the node of the current key,
# then add it to the back (most recently used). we pop the least recently used as head,
# and delete it from the dict in O(1)

class Node():
    def __init__(self, key=0, val=0, prev=None, next=None):
        self.key = key
        self.val = val
        self.prev = prev
        self.next = next

class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # this will store key-node pairs
        self.front = Node()
        self.back = Node()
        self.front.next = self.back
        self.back.prev = self.front

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.remove(key)
        self.insert(key)
        return self.cache[key].val
 

    def put(self, key: int, value: int) -> None:
        node = Node(key=key, val=value)
        if key in self.cache:
            (self.cache[key]).val = value
            self.remove(key)
        else:
            self.cache[key] = node
        self.insert(key)

        if len(self.cache) > self.capacity:
            self.cache.pop(self.remove(self.front.next.key)) # type: ignore
    
    def remove(self, key):
        node = self.cache[key]
        node.prev.next, node.next.prev = node.next, node.prev
        node.prev, node.next = None, None
        return node.key
    
    def insert(self, key):
        node = self.cache[key]
        temp = self.back.prev
        temp.next = node # type: ignore
        node.prev = temp
        node.next = self.back
        self.back.prev = node

