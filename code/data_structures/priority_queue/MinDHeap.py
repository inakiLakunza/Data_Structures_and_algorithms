

class MinDHeap:
    def __init__(self, degree, maxNodes):
        self.d = max(2, degree)
        self.n = max(self.d, maxNodes)

        self.heap = [None] * self.n
        self.child = [0] * self.n
        self.parent = [0] * self.n
        for i in range(self.n):
            self.parent[i] = (i - 1) // self.d
            self.child[i] = i * self.d + 1

        self.sz = 0

    def size(self):
        return self.sz

    def isEmpty(self):
        return self.sz == 0

    def clear(self):
        self.heap = [None] * self.n
        self.sz = 0

    def peek(self):
        if self.isEmpty():
            return None
        return self.heap[0]

    def poll(self):
        if self.isEmpty():
            return None
        root = self.heap[0]
        self.heap[0] = self.heap[self.sz - 1]
        self.heap[self.sz - 1] = None
        self.sz -= 1
        self.sink(0)
        return root

    def add(self, elem):
        if elem is None:
            raise ValueError("No null elements please :)")
        self.heap[self.sz] = elem
        self.swim(self.sz)
        self.sz += 1

    def sink(self, i):
        while True:
            j = self.minChild(i)
            if j == -1:
                break
     
