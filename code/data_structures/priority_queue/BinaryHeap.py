

class BinaryHeap:
    def __init__(self):
        # we will use an array (a list in python)
        # to write our Binary Heap
        self.heap = []

    def __init__(self, sz):
        # If we initialize it with a chosen size
        # we will create a list of that length
        self.heap = [None] * sz

    def __init__(self, elems):
        self.heap = elems[:]
        for i in range(max(0, len(self.heap) // 2 - 1), -1, -1):
            self.sink(i)

    def isEmpty(self):
        return self.size() == 0

    def clear(self):
        self.heap.clear()

    def size(self):
        return len(self.heap)

    def peek(self):
        if self.isEmpty():
            return None
        return self.heap[0]

    def poll(self):
        return self.removeAt(0)

    def contains(self, elem):
        return elem in self.heap

    def add(self, elem):
        if elem is None:
            raise ValueError("Element cannot be None")
        self.heap.append(elem)
        indexOfLastElem = self.size() - 1
        self.swim(indexOfLastElem)

    def less(self, i, j):
        return self.heap[i] <= self.heap[j]

    def swim(self, k):
        # BUBBLE UP, swapping with parent node
        parent = (k - 1) // 2
        while k > 0 and self.less(k, parent):
            self.swap(parent, k)
            k = parent
            parent = (k - 1) // 2

    def sink(self, k):
        # BUBBLE DOWN, swapping with children node
        # choosing the correct one depending on
        # the type of heap we have
        heapSize = self.size()
        while True:
            left = 2 * k + 1
            right = 2 * k + 2
            smallest = left
            if right < heapSize and self.less(right, left):
                smallest = right
            if left >= heapSize or self.less(k, smallest):
                break
            self.swap(smallest, k)
            k = smallest

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def remove(self, element):
        if element is None:
            return False
        for i, elem in enumerate(self.heap):
            if elem == element:
                self.removeAt(i)
                return True
        return False

    def removeAt(self, i):
        if self.isEmpty():
            return None
        indexOfLastElem = self.size() - 1
        removed_data = self.heap[i]
        self.swap(i, indexOfLastElem)
        self.heap.pop()
        if i == indexOfLastElem:
            return removed_data
        elem = self.heap[i]
        self.sink(i)
        if self.heap[i] == elem:
            self.swim(i)
        return removed_data

    def isMinHeap(self, k):
        heapSize = self.size()
        if k >= heapSize:
            return True
        left = 2 * k + 1
        right = 2 * k + 2
        if left < heapSize and not self.less(k, left):
            return False
        if right < heapSize and not self.less(k, right):
            return False
        return self.isMinHeap(left) and self.isMinHeap(right)

    def __str__(self):
        return str(self.heap)
