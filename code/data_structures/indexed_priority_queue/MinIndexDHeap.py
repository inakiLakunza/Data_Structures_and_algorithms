from math import min
from typing import Any, List, Union

from collections.abc import NoSuchElementException


class MinIndexedDHeap:
    def __init__(self, degree: int, maxSize: int):
        if maxSize <= 0:
            raise ValueError("maxSize <= 0")

        self.D = max(2, degree)
        self.N = max(self.D + 1, maxSize)

        # Create unfilled inverse and position maps
        # and the values array. We also create arrays
        # where we will store how to reach of the child 
        # and parent nodes for each node.
        self.im = [-1] * self.N
        self.pm = [-1] * self.N
        self.child = [0] * self.N
        self.parent = [0] * self.N
        self.values = [None] * self.N

        for i in range(self.N):
            self.parent[i] = (i - 1) // self.D
            self.child[i] = i * self.D + 1

        # Size of the heap, the number of nodes it contains
        self.sz = 0

    def size(self) -> int:
        return self.sz

    def isEmpty(self) -> bool:
        return self.sz == 0

    # We will check if the key index of the wanted
    # element is not -1 
    def contains(self, ki: int) -> bool:
        self.keyInBoundsOrThrow(ki)
        return self.pm[ki] != -1

    def peekMinKeyIndex(self) -> int:
        self.isNotEmptyOrThrow()
        return self.im[0]

    def pollMinKeyIndex(self) -> int:
        minki = self.peekMinKeyIndex()
        self.delete(minki)
        return minki

    def peekMinValue(self) -> Any:
        self.isNotEmptyOrThrow()
        return self.values[self.im[0]]

    def pollMinValue(self) -> Any:
        minValue = self.peekMinValue()
        self.delete(self.peekMinKeyIndex())
        return minValue

    # We first insert the new node at the bottom right position,
    # which is conveniently given by the size of the heap. Insert
    # it there and then bubble up the node until we preserve the
    # heap invariance. When we swap nodes we have to take into
    # account that we have to change the values in the position
    # and inverse maps. 
    def insert(self, ki: int, value: Any) -> None:
        if self.contains(ki):
            raise ValueError("index already exists; received: " + str(ki))
        self.valueNotNullOrThrow(value)
        self.pm[ki] = self.sz
        self.im[self.sz] = ki
        self.values[ki] = value
        self.swim(self.sz)
        self.sz += 1

    def valueOf(self, ki: int) -> Any:
        self.keyExistsOrThrow(ki)
        return self.values[ki]

    # For deletion, we first swap our node with
    # the lower right node of the heap and then
    # delete it. Then we have to preserve the heap
    # invariant, so we have to bubble up or bubble down
    # the node which previously was on the lower right.
    # We use both, sink and swim. If it can swim it will,
    # otherwise it will sink, and otherwise it will mean
    # that when doing the change we already satisfied
    # the heap invariant
    def delete(self, ki: int) -> Any:
        self.keyExistsOrThrow(ki)
        i = self.pm[ki]
        self.swap(i, self.sz - 1)
        self.sz -= 1
        self.sink(i)
        self.swim(i)
        value = self.values[ki]
        self.values[ki] = None
        self.pm[ki] = -1
        self.im[self.sz] = -1
        return value
    
    # We can update the valuesof our elements, so, when doing
    # this we have to adapt the values, pm and im arrays
    def update(self, ki: int, value: Any) -> Any:
        self.keyExistsAndValueNotNullOrThrow(ki, value)
        i = self.pm[ki]
        oldValue = self.values[ki]
        self.values[ki] = value
        self.sink(i)
        self.swim(i)
        return oldValue

    def decrease(self, ki: int, value: Any) -> None:
        self.keyExistsAndValueNotNullOrThrow(ki, value)
        if self.less(value, self.values[ki]):
            self.values[ki] = value
            self.swim(self.pm[ki])

    def increase(self, ki: int, value: Any) -> None:
        self.keyExistsAndValueNotNullOrThrow(ki, value)
        if self.less(self.values[ki], value):
            self.values[ki] = value
            self.sink(self.pm[ki])

    def sink(self, i: int) -> None:
        while True:
            j = self.minChild(i)
            if j == -1:
                break
            self.swap(i, j)
            i = j

    def swim(self, i: int) -> None:
        while i > 0 and self.less(i, self.parent[i]):
            self.swap(i, self.parent[i])
            i = self.parent[i]

    def minChild(self, i: int) -> int:
        index = -1
        from_idx = self.child[i]
        to_idx = min(self.sz, from_idx + self.D)
        for j in range(from_idx, to_idx):
            if self.less(j, i):
                index = i = j
        return index

    def swap(self, i: int, j: int) -> None:
        self.pm[self.im[j]] = i
        self.pm[self.im[i]] = j
        self.im[i], self.im[j] = self.im[j], self.im[i]

    def less(self, i: int, j: int) -> bool:
        return self.values[self.im[i]] < self.values[self.im[j]]

    def isMinHeap(self) -> bool:
        return self.isMinHeapRecursive(0)

    def isMinHeapRecursive(self, i: int) -> bool:
        from_idx = self.child[i]
        to_idx = min(self.sz, from_idx + self.D)
        for j in range(from_idx, to_idx):
            if not self.less(i, j):
                return False
            if not self.isMinHeapRecursive(j):
                return False
        return True

    def isNotEmptyOrThrow(self) -> None:
        if self.isEmpty():
            raise NoSuchElementException("Priority queue underflow")

    def keyExistsAndValueNotNullOrThrow(self, ki: int, value: Any) -> None:
        self.keyExistsOrThrow(ki)
        self.valueNotNullOrThrow(value)

    def keyExistsOrThrow(self, ki: int) -> None:
        if not self.contains(ki):
            raise NoSuchElementException("Index does not exist; received: " + str(ki))

    def valueNotNullOrThrow(self, value: Any) -> None:
        if value is None:
            raise ValueError("value cannot be null")

    def keyInBoundsOrThrow(self, ki: int) -> None:
        if ki < 0 or ki >= self.N:
            raise ValueError("Key index out of bounds; received: " + str(ki))
