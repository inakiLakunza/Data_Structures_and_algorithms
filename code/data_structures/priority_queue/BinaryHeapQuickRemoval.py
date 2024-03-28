

from collections import defaultdict
from typing import List, Dict, Set, Optional
#from heapq import heappush, heappop


# NOW WE ARE USING A HASHTABLE FOR FASTER REMOVAL
# The code is quite the same as earlier, but now
# we will also use a dictionary as a Hashtable
# so we will be updating and looking it 
class BinaryHeapQuickRemovals:
    def __init__(self):
        self.heap = []
        self.map: Dict[int, Set[int]] = defaultdict(set)

    def __init__(self, sz: int):
        self.heap = [None] * sz
        self.map = defaultdict(set)

    def __init__(self, elems: List[int]):
        self.heap = elems[:]
        self.map = defaultdict(set)
        for i, elem in enumerate(self.heap):
            self.map[elem].add(i)

        for i in range(max(0, len(self.heap) // 2 - 1), -1, -1):
            self.sink(i)

    def __init__(self, elems: List[int]):
        self.heap = list(elems)
        self.map = defaultdict(set)
        for i, elem in enumerate(self.heap):
            self.map[elem].add(i)

        for i in range(max(0, len(self.heap) // 2 - 1), -1, -1):
            self.sink(i)

    def isEmpty(self) -> bool:
        return len(self.heap) == 0

    def clear(self) -> None:
        self.heap.clear()
        self.map.clear()

    def size(self) -> int:
        return len(self.heap)

    def peek(self) -> Optional[int]:
        if self.isEmpty():
            return None
        return self.heap[0]

    def poll(self) -> Optional[int]:
        return self.removeAt(0)

    def contains(self, elem: int) -> bool:
        return elem in self.map

    def add(self, elem: int) -> None:
        self.heap.append(elem)
        indexOfLastElem = self.size() - 1
        self.map[elem].add(indexOfLastElem)
        self.swim(indexOfLastElem)

    def less(self, i: int, j: int) -> bool:
        return self.heap[i] <= self.heap[j]

    def swim(self, k: int) -> None:
        parent = (k - 1) // 2
        while k > 0 and self.less(k, parent):
            self.swap(parent, k)
            k = parent
            parent = (k - 1) // 2

    def sink(self, k: int) -> None:
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

    def swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.map[self.heap[i]].remove(i)
        self.map[self.heap[j]].remove(j)
        self.map[self.heap[i]].add(j)
        self.map[self.heap[j]].add(i)

    def remove(self, element: int) -> bool:
        if element not in self.map:
            return False
        index = next(iter(self.map[element]))
        self.removeAt(index)
        return True

    def removeAt(self, i: int) -> Optional[int]:
        if self.isEmpty():
            return None
        indexOfLastElem = self.size() - 1
        removed_data = self.heap[i]
        self.swap(i, indexOfLastElem)
        self.heap.pop()
        self.map[removed_data].remove(indexOfLastElem)
        if len(self.map[removed_data]) == 0:
            del self.map[removed_data]
        if i == indexOfLastElem:
            return removed_data
        elem = self.heap[i]
        self.sink(i)
        if self.heap[i] == elem:
            self.swim(i)
        return removed_data

    def isMinHeap(self, k: int) -> bool:
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

    def __str__(self) -> str:
        return str(self.heap)
