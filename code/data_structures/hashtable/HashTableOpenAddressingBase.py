


from collections.abc import Iterable
from typing import List

class HashTableOpenAddressingBase(Iterable):

    TOMBSTONE = object()

    def __init__(self, capacity=7, load_factor=0.65):
        if capacity <= 0:
            raise ValueError("Illegal capacity: " + str(capacity))

        if load_factor <= 0 or load_factor == float("nan") or load_factor == float("inf"):
            raise ValueError("Illegal loadFactor: " + str(load_factor))

        self.load_factor = load_factor
        self.capacity = max(7, capacity)
        self.adjust_capacity()
        self.threshold = int(self.capacity * load_factor)

        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

        self.used_buckets = 0
        self.key_count = 0
        self.modification_count = 0

    def setup_probing(self, key):
        pass

    def probe(self, x):
        pass

    def adjust_capacity(self):
        pass

    def increase_capacity(self):
        self.capacity = 2 * self.capacity + 1

    def clear(self):
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.key_count = 0
        self.used_buckets = 0
        self.modification_count += 1

    def size(self):
        return self.key_count

    def get_capacity(self):
        return self.capacity

    def is_empty(self):
        return self.key_count == 0

    def put(self, key, value):
        return self.insert(key, value)

    def add(self, key, value):
        return self.insert(key, value)

    def contains_key(self, key):
        return self.has_key(key)

    def keys(self) -> List:
        return [key for key in self.keys if key is not None and key != self.TOMBSTONE]

    def values(self) -> List:
        return [value for value in self.values if value is not None]

    def resize_table(self):
        self.increase_capacity()
        self.adjust_capacity()

        self.threshold = int(self.capacity * self.load_factor)

        old_key_table = self.keys
        old_value_table = self.values

        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity

        self.key_count = 0
        self.used_buckets = 0

        for i in range(len(old_key_table)):
            if old_key_table[i] is not None and old_key_table[i] != self.TOMBSTONE:
                self.insert(old_key_table[i], old_value_table[i])
                old_key_table[i] = None
                old_value_table[i] = None

    def normalize_index(self, key_hash):
        return (key_hash & 0x7FFFFFFF) % self.capacity

    @staticmethod
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def insert(self, key, val):
        if key is None:
            raise ValueError("Null key")
        if self.used_buckets >= self.threshold:
            self.resize_table()

        self.setup_probing(key)
        offset = self.normalize_index(hash(key))

        for x in range(1, self.capacity + 1):
            i = self.normalize_index(offset + self.probe(x))

            if self.keys[i] == self.TOMBSTONE:
                if j == -1:
                    j = i
            elif self.keys[i] is not None:
                if self.keys[i] == key:
                    old_value = self.values[i]
                    if j == -1:
                        self.values[i] = val
                    else:
                        self.keys[i] = self.TOMBSTONE
                        self.values[i] = None
                        self.keys[j] = key
                        self.values[j] = val
                    self.modification_count += 1
                    return old_value
            else:
                if j == -1:
                    self.used_buckets += 1
                    self.key_count += 1
                    self.keys[i] = key
                    self.values[i] = val
                else:
                    self.key_count += 1
                    self.keys[j] = key
                    self.values[j] = val
                self.modification_count += 1
                return None

    def has_key(self, key):
        if key is None:
            raise ValueError("Null key")

        self.setup_probing(key)
        offset = self.normalize_index(hash(key))

        for x in range(1, self.capacity + 1):
            i = self.normalize_index(offset + self.probe(x))

            if self.keys[i] == self.TOMBSTONE:
                if j == -1:
                    j = i
            elif self.keys[i] is not None:
                if self.keys[i] == key:
                    if j != -1:
                        self.keys[j] = self.keys[i]
                        self.values[j] = self.values[i]
                        self.keys[i] = self.TOMBSTONE
                        self.values[i] = None
                    return True
            else:
                return False

    def get(self, key):
        if key is None:
            raise ValueError("Null key")

        self.setup_probing(key)
        offset = self.normalize_index(hash(key))

        for x in range(1, self.capacity + 1):
            i = self.normalize_index(offset + self.probe(x))

            if self.keys[i] == self.TOMBSTONE:
                if j == -1:
                    j = i
            elif self.keys[i] is not None:
                if self.keys[i] == key:
                    if j != -1:
                        self.keys[j] = self.keys[i]
                        self.values[j] = self.values[i]
                        self.keys[i] = self.TOMBSTONE
                        self.values[i] = None
                        return self.values[j]
                    else:
                        return self.values[i]
            else:
                return None

    def remove(self, key):
        if key is None:
            raise ValueError("Null key")

        self.setup_probing(key)
        offset = self.normalize_index(hash(key))

        for x in range(1, self.capacity + 1):
            i = self.normalize_index(offset + self.probe(x))

            if self.keys[i] == self.TOMBSTONE:
                continue

            if self.keys[i] is None:
                return None

            if self.keys[i] == key:
                self.key_count -= 1
                self.modification_count += 1
                old_value = self.values[i]
                self.keys[i] = self.TOMBSTONE
                self.values[i] = None
                return old_value

    def __str__(self):
        return "{" + ", ".join([str(self.keys[i]) + " => " + str(self.values[i]) for i in range(self.capacity)
                                if self.keys[i] is not None and self.keys[i] != self.TOMBSTONE]) + "}"

    def __iter__(self):
        class Iterator:
            def __init__(self, hashtable):
                self.index = 0
                self.keys_left = hashtable.key_count
                self.MODIFICATION_COUNT = hashtable.modification_count

            def __iter__(self):
                return self

            def __next__(self):
                if self.MODIFICATION_COUNT != self.hashtable.modification_count:
                    raise RuntimeError("Concurrent modification detected")
                while self.hashtable.keys[self.index] is None or self.hashtable.keys[self.index] == self.hashtable.TOMBSTONE:
                    self.index += 1
                self.keys_left -= 1
                return self.hashtable.keys[self.index]

        return Iterator(self)