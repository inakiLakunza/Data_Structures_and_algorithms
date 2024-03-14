class Array:
    def __init__(self, capacity=16):
        if capacity < 0:
            raise ValueError("Illegal Capacity: " + str(capacity))
        self.capacity = capacity
        self.arr = [None] * capacity
        self.len = 0

    def size(self):
        return self.len

    def is_empty(self):
        return self.size() == 0

    def get(self, index):
        return self.arr[index]

    def set(self, index, elem):
        self.arr[index] = elem

    def clear(self):
        for i in range(self.capacity):
            self.arr[i] = None
        self.len = 0

    def add(self, elem):
        if self.len + 1 >= self.capacity:
            if self.capacity == 0:
                self.capacity = 1
            else:
                self.capacity *= 2  # double the size
            new_arr = [None] * self.capacity
            for i in range(self.len):
                new_arr[i] = self.arr[i]
            self.arr = new_arr
        self.arr[self.len] = elem
        self.len += 1

    def remove_at(self, rm_index):
        if rm_index >= self.len or rm_index < 0:
            raise IndexError()
        data = self.arr[rm_index]
        new_arr = [None] * (self.len - 1)
        for i in range(self.len):
            if i == rm_index:
                continue
            new_arr[i if i < rm_index else i - 1] = self.arr[i]
        self.arr = new_arr
        self.capacity = self.len - 1
        self.len -= 1
        return data

    def remove(self, obj):
        for i in range(self.len):
            if self.arr[i] == obj:
                self.remove_at(i)
                return True
        return False

    def index_of(self, obj):
        for i in range(self.len):
            if self.arr[i] == obj:
                return i
        return -1

    def contains(self, obj):
        return self.index_of(obj) != -1

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index < self.len:
            result = self.arr[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def __str__(self):
        if self.len == 0:
            return "[]"
        else:
            return "[" + ", ".join(str(self.arr[i]) for i in range(self.len)) + "]"