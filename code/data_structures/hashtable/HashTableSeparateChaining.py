
# We first define the entry object,
# which will consist of a key-value
# pair and its hash value
# and when comparing two different entries
# we will first compare their hash values
# and if they are equal then we will 
# compare their keys, otherwise
# we directly know that they are not equal
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.hash = hash(key)

    def __eq__(self, other):
        if self.hash != other.hash:
            return False
        return self.key == other.key

    def __str__(self):
        return f"{self.key} => {self.value}"


class HashTableSeparateChaining:

    # Default capacity of our HT
    # and above which load factor 
    # we will extend our HT
    # and when extending we will have
    # to create a new hash function
    # and remap all of our current elements
    DEFAULT_CAPACITY = 3
    DEFAULT_LOAD_FACTOR = 0.75

    def __init__(self, capacity=DEFAULT_CAPACITY, max_load_factor=DEFAULT_LOAD_FACTOR):
        if capacity < 0:
            raise ValueError("Illegal capacity")
        if max_load_factor <= 0 or max_load_factor == float('inf') or max_load_factor != max_load_factor:
            raise ValueError("Illegal maxLoadFactor")
        self.max_load_factor = max_load_factor
        self.capacity = max(self.DEFAULT_CAPACITY, capacity)
        self.threshold = int(self.capacity * max_load_factor)
        self.size = 0
        self.table = [None] * self.capacity

    def size(self):
        return self.size

    def is_empty(self):
        return self.size == 0

    def normalize_index(self, key_hash):
        return key_hash & 0x7FFFFFFF % self.capacity

    def clear(self):
        self.table = [None] * self.capacity
        self.size = 0

    def contains_key(self, key):
        return self.has_key(key)

    def has_key(self, key):
        # we will first get the bucket associated to 
        # the hash value and then look inside the bucket
        bucket_index = self.normalize_index(hash(key))
        return self.bucket_seek_entry(bucket_index, key) is not None

    def put(self, key, value):
        return self.insert(key, value)

    def add(self, key, value):
        return self.insert(key, value)

    def insert(self, key, value):
        # We will first get the hash value of its
        # position and then insert it in the corresponding bucket
        if key is None:
            raise ValueError("Null key")
        new_entry = Entry(key, value)
        bucket_index = self.normalize_index(new_entry.hash)
        return self.bucket_insert_entry(bucket_index, new_entry)

    def get(self, key):
        # Same as with insert but getting an element
        if key is None:
            return None
        bucket_index = self.normalize_index(hash(key))
        entry = self.bucket_seek_entry(bucket_index, key)
        if entry:
            return entry.value
        return None

    def remove(self, key):
        if key is None:
            return None
        bucket_index = self.normalize_index(hash(key))
        return self.bucket_remove_entry(bucket_index, key)

    def bucket_remove_entry(self, bucket_index, key):
        entry = self.bucket_seek_entry(bucket_index, key)
        if entry:
            links = self.table[bucket_index]
            links.remove(entry)
            self.size -= 1
            return entry.value
        return None

    def bucket_insert_entry(self, bucket_index, entry):
        # We first retrive the bucket of that hash value, and
        # if exists, we see if the element is already inside,
        # and if it is not, the we insert it in the bucket
        # and if it is, we actualize its value
        bucket = self.table[bucket_index]
        if bucket is None:
            self.table[bucket_index] = bucket = []
        existent_entry = self.bucket_seek_entry(bucket_index, entry.key)
        if not existent_entry:
            bucket.append(entry)
            self.size += 1
            if self.size > self.threshold:
                self.resize_table()
            return None
        else:
            old_val = existent_entry.value
            existent_entry.value = entry.value
            return old_val

    def bucket_seek_entry(self, bucket_index, key):
        bucket = self.table[bucket_index]
        if bucket:
            for entry in bucket:
                if entry.key == key:
                    return entry
        return None

    def resize_table(self):
        # When we have surpassed the threshold capacity
        # we create a new table with the double size as earlier
        # and we remap all the existing elements
        self.capacity *= 2
        self.threshold = int(self.capacity * self.max_load_factor)
        new_table = [None] * self.capacity

        for bucket in self.table:
            if bucket:
                for entry in bucket:
                    bucket_index = self.normalize_index(entry.hash)
                    if new_table[bucket_index] is None:
                        new_table[bucket_index] = []
                    new_table[bucket_index].append(entry)
        self.table = new_table

    def keys(self):
        keys = []
        for bucket in self.table:
            if bucket:
                for entry in bucket:
                    keys.append(entry.key)
        return keys

    def values(self):
        values = []
        for bucket in self.table:
            if bucket:
                for entry in bucket:
                    values.append(entry.value)
        return values

    def __iter__(self):
        element_count = self.size
        bucket_index = 0
        bucket_iter = iter(self.table[0]) if self.table[0] else None

        def iterator():
            nonlocal bucket_index, bucket_iter
            while bucket_index < self.capacity:
                if element_count != self.size:
                    raise RuntimeError("An item was added or removed while iterating")
                if bucket_iter is None or not hasattr(bucket_iter, '__next__'):
                    while bucket_index < self.capacity:
                        if self.table[bucket_index]:
                            bucket_iter = iter(self.table[bucket_index])
                            break
                        bucket_index += 1
                try:
                    yield next(bucket_iter).key
                except StopIteration:
                    bucket_index += 1
                    bucket_iter = None

        return iterator()

    def __str__(self):
        result = "{"
        for bucket in self.table:
            if bucket:
                for entry in bucket:
                    result += str(entry) + ", "
        result += "}"
        return result


# Example Usage
if __name__ == "__main__":
    hash_table = HashTableSeparateChaining()
    hash_table.put("key1", "value1")
    hash_table.put("key2", "value2")
    hash_table.put("key3", "value3")
    print("Size:", hash_table.size())
    print("Is empty:", hash_table.is_empty())
    print("Keys:", hash_table.keys())
    print("Values:", hash_table.values())
    print("Get value for key1:", hash_table.get("key1"))
    print("Contains key 'key4':", hash_table.contains_key("key4"))
    print("Hashtable:", hash_table)
