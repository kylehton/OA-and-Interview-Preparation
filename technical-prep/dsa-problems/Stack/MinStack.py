class MinStack:

    def __init__(self):
        self.stack = []
        self.minimumStack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if len(self.minimumStack) > 0 and val > self.minimumStack[-1]:
            self.minimumStack.append(self.minimumStack[-1])
        else:
            self.minimumStack.append(val)

    def pop(self) -> None:
        self.stack.pop()
        self.minimumStack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.minimumStack[-1]
