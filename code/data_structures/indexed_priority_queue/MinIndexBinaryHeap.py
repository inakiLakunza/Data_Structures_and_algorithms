
from MinIndexDHeap import MinIndexedDHeap

class MinIndexedBinaryHeap(MinIndexedDHeap):
    def __init__(self, maxSize):
        super().__init__(2, maxSize)
