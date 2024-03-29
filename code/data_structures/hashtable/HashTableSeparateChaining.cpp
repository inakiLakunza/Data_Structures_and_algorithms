

#include <iostream>
#include <vector>
#include <list>
#include <algorithm>

template<typename K, typename V>
class Entry {
public:
    int hash;
    K key;
    V value;

    Entry(K key, V value) : key(key), value(value), hash(std::hash<K>()(key)) {}

    bool operator==(const Entry<K, V>& other) const {
        return hash == other.hash && key == other.key;
    }

    friend std::ostream& operator<<(std::ostream& os, const Entry<K, V>& entry) {
        os << entry.key << " => " << entry.value;
        return os;
    }
};

template<typename K, typename V>
class HashTableSeparateChaining {
private:
    static const int DEFAULT_CAPACITY = 3;
    static const double DEFAULT_LOAD_FACTOR;

    double maxLoadFactor;
    int capacity, threshold, size;
    std::vector<std::list<Entry<K, V>>> table;

    int normalizeIndex(int keyHash) const {
        return (keyHash & 0x7FFFFFFF) % capacity;
    }

    void resizeTable() {
        capacity *= 2;
        threshold = static_cast<int>(capacity * maxLoadFactor);

        std::vector<std::list<Entry<K, V>>> newTable(capacity);

        for (auto& bucket : table) {
            for (auto& entry : bucket) {
                int bucketIndex = normalizeIndex(entry.hash);
                newTable[bucketIndex].push_back(entry);
            }
        }

        table = std::move(newTable);
    }

public:
    HashTableSeparateChaining(int capacity = DEFAULT_CAPACITY, double maxLoadFactor = DEFAULT_LOAD_FACTOR)
        : maxLoadFactor(maxLoadFactor), capacity(std::max(DEFAULT_CAPACITY, capacity)), size(0) {
        if (capacity < 0)
            throw std::invalid_argument("Illegal capacity");
        if (maxLoadFactor <= 0 || std::isnan(maxLoadFactor) || std::isinf(maxLoadFactor))
            throw std::invalid_argument("Illegal maxLoadFactor");

        threshold = static_cast<int>(this->capacity * maxLoadFactor);
        table.resize(this->capacity);
    }

    int getSize() const {
        return size;
    }

    bool isEmpty() const {
        return size == 0;
    }

    bool containsKey(const K& key) const {
        return hasKey(key);
    }

    bool hasKey(const K& key) const {
        int bucketIndex = normalizeIndex(std::hash<K>()(key));
        auto& bucket = table[bucketIndex];
        return std::find_if(bucket.begin(), bucket.end(), [&](const Entry<K, V>& entry) { return entry.key == key; }) != bucket.end();
    }

    V put(const K& key, const V& value) {
        return insert(key, value);
    }

    V add(const K& key, const V& value) {
        return insert(key, value);
    }

    V insert(const K& key, const V& value) {
        if (key == nullptr)
            throw std::invalid_argument("Null key");

        Entry<K, V> newEntry(key, value);
        int bucketIndex = normalizeIndex(newEntry.hash);
        auto& bucket = table[bucketIndex];

        auto it = std::find_if(bucket.begin(), bucket.end(), [&](const Entry<K, V>& entry) { return entry.key == key; });
        if (it != bucket.end()) {
            V oldValue = it->value;
            it->value = value;
            return oldValue;
        } else {
            bucket.push_back(newEntry);
            ++size;
            if (size > threshold)
                resizeTable();
            return nullptr;
        }
    }

    V get(const K& key) const {
        int bucketIndex = normalizeIndex(std::hash<K>()(key));
        auto& bucket = table[bucketIndex];
        auto it = std::find_if(bucket.begin(), bucket.end(), [&](const Entry<K, V>& entry) { return entry.key == key; });
        return (it != bucket.end()) ? it->value : nullptr;
    }

    V remove(const K& key) {
        int bucketIndex = normalizeIndex(std::hash<K>()(key));
        auto& bucket = table[bucketIndex];
        auto it = std::find_if(bucket.begin(), bucket.end(), [&](const Entry<K, V>& entry) { return entry.key == key; });
        if (it != bucket.end()) {
            V value = it->value;
            bucket.erase(it);
            --size;
            return value;
        }
        return nullptr;
    }

    std::vector<K> keys() const {
        std::vector<K> keys;
        for (auto& bucket : table) {
            for (auto& entry : bucket) {
                keys.push_back(entry.key);
            }
        }
        return keys;
    }

    std::vector<V> values() const {
        std::vector<V> values;
        for (auto& bucket : table) {
            for (auto& entry : bucket) {
                values.push_back(entry.value);
            }
        }
        return values;
    }

    class Iterator {
    private:
        const HashTableSeparateChaining<K, V>& hashTable;
        int currentIndex;
        typename std::list<Entry<K, V>>::const_iterator currentBucketIterator;

        void findNext() {
            while (currentIndex < hashTable.capacity) {
                if (currentBucketIterator == hashTable.table[currentIndex].end()) {
                    ++currentIndex;
                    if (currentIndex < hashTable.capacity)
                        currentBucketIterator = hashTable.table[currentIndex].begin();
                } else {
                    break;
                }
            }
        }

    public:
        Iterator(const HashTableSeparateChaining<K, V>& hashTable) : hashTable(hashTable), currentIndex(0) {
            if (hashTable.size > 0) {
                currentBucketIterator = hashTable.table[0].begin();
                findNext();
            }
        }

        bool hasNext() const {
            return currentIndex < hashTable.capacity && currentBucketIterator != hashTable.table[currentIndex].end();
        }

        K next() {
            if (!hasNext())
                throw std::out_of_range("No more elements to iterate over");
            K key = currentBucketIterator->key;
            ++currentBucketIterator;
            findNext();
            return key;
        }
    };

    Iterator iterator() const {
        return Iterator(*this);
    }

    friend std::ostream& operator<<(std::ostream& os, const HashTableSeparateChaining& hashTable) {
        os << "{";
        for (const auto& bucket : hashTable.table) {
            for (const auto& entry : bucket) {
                os << entry << ", ";
            }
        }
        os << "}";
        return os;
    }
};

template<typename K, typename V>
const double HashTableSeparateChaining<K, V>::DEFAULT_LOAD_FACTOR = 0.75;

int main() {
    HashTableSeparateChaining<std::string, std::string> hashTable;
    hashTable.put("key1", "value1");
    hashTable.put("key2", "value2");
    hashTable.put("key3", "value3");

    std::cout << "Size: " << hashTable.getSize() << std::endl;
    std::cout << "Is empty: " << std::boolalpha << hashTable.isEmpty() << std::endl;
    std::cout << "Keys: ";
    for (const auto& key : hashTable.keys()) {
        std::cout << key << ", ";
    }
    std::cout << std::endl;
    std::cout << "Values: ";
    for (const auto& value : hashTable.values()) {
        std::cout << value << ", ";
    }
    std::cout << std::endl;
    std::cout << "Get value for key1: " << hashTable.get("key1") << std::endl;
    std::cout << "Contains key 'key4': " << std::boolalpha << hashTable.containsKey("key4") << std::endl;
    std::cout << "Hashtable: " << hashTable << std::endl;

    return 0;
}
