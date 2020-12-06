class Stack():
    def __init__(self, NMAX=10000):
        self.NMAX = NMAX
        self.count = 0
        self.pool = []

    def is_full(self):
        if self.count == self.NMAX:
            return True
    
    def is_empty(self):
        if self.count == 0:
            return True
    
    def show_top(self):
        if not self.is_empty():
            return self.pool[-1]
        else:
            raise Exception("Stack is empty!")
    
    def pop(self):
        if not self.is_empty():
            self.count -= 1
            return self.pool.pop()
        else:
            raise Exception("Stack is empty!")
    
    def push(self, elem):
        if not self.is_full():
            self.count += 1
            self.pool.append(elem)
        else:
            raise Exception("Stack is full!")
