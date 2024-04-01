

#include <iostream>
#include <vector>
#include <stdexcept>

template <typename K, typename V>
class HashTableOpenAddressingBase {
protected:
    double loadFactor;
    int capacity, threshold, modificationCount;
    int usedBuckets, keyCount;
    std::vector<K> keys;
    std::vector<V> values;
    const K TOMBSTONE;

    static constexpr int DEFAULT_CAPACITY = 7;
    static constexpr double DEFAULT_LOAD_FACTOR = 0.65;

public:
    HashTableOpenAddressingBase() : HashTableOpenAddressingBase(DEFAULT_CAPACITY, DEFAULT_LOAD_FACTOR) {}

    HashTableOpenAddressingBase(int capacity) : HashTableOpenAddressingBase(capacity, DEFAULT_LOAD_FACTOR) {}

    HashTableOpenAddressingBase(int capacity, double loadFactor) : loadFactor(loadFactor), capacity(std::max(DEFAULT_CAPACITY, capacity)), TOMBSTONE(nullptr) {
        if (capacity <= 0)
            throw std::invalid_argument("Illegal capacity: " + std::to_string(capacity));

        if (loadFactor <= 0 || std::isnan(loadFactor) || std::isinf(loadFactor))
            throw std::invalid_argument("Illegal loadFactor: " + std::to_string(loadFactor));

        adjustCapacity();
        threshold = static_cast<int>(this->capacity * loadFactor);
        keys.resize(this->capacity);
        values.resize(this->capacity);
    }

    virtual ~HashTableOpenAddressingBase() = default;

    virtual void setupProbing(const K& key) = 0;

    virtual int probe(int x) = 0;

    virtual void adjustCapacity() {
        capacity = (2 * capacity) + 1;
    }

    void increaseCapacity() {
        capacity = (2 * capacity) + 1;
    }

    void clear() {
        for (int i = 0; i < capacity; i++) {
            keys[i] = nullptr;
            values[i] = nullptr;
        }
        keyCount = usedBuckets = 0;
        modificationCount++;
    }

    int size() const {
        return keyCount;
    }

    int getCapacity() const {
        return capacity;
    }

    bool isEmpty() const {
        return keyCount == 0;
    }

    V put(const K& key, const V& value) {
        return insert(key, value);
    }

    V add(const K& key, const V& value) {
        return insert(key, value);
    }

    bool containsKey(const K& key) const {
        return hasKey(key);
    }

    std::vector<K> keys() const {
        std::vector<K> hashtableKeys;
        hashtableKeys.reserve(size());
        for (int i = 0; i < capacity; i++)
            if (keys[i] != nullptr && keys[i] != TOMBSTONE)
                hashtableKeys.push_back(keys[i]);
        return hashtableKeys;
    }

    std::vector<V> values() const {
        std::vector<V> hashtableValues;
        hashtableValues.reserve(size());
        for (int i = 0; i < capacity; i++)
            if (keys[i] != nullptr && keys[i] != TOMBSTONE)
                hashtableValues.push_back(values[i]);
        return hashtableValues;
    }

    void resizeTable() {
        increaseCapacity();
        adjustCapacity();
        threshold = static_cast<int>(capacity * loadFactor);
        std::vector<K> oldKeyTable(capacity);
        std::vector<V> oldValueTable(capacity);
        oldKeyTable.swap(keys);
        oldValueTable.swap(values);
        keyCount = usedBuckets = 0;
        for (int i = 0; i < oldKeyTable.size(); i++) {
            if (oldKeyTable[i] != nullptr && oldKeyTable[i] != TOMBSTONE)
                insert(oldKeyTable[i], oldValueTable[i]);
        }
    }

    int normalizeIndex(int keyHash) const {
        return (keyHash & 0x7FFFFFFF) % capacity;
    }

    static int gcd(int a, int b) {
        if (b == 0) return a;
        return gcd(b, a % b);
    }

    V insert(const K& key, const V& val) {
        if (key == nullptr)
            throw std::invalid_argument("Null key");
        if (usedBuckets >= threshold)
            resizeTable();

        setupProbing(key);
        int offset = normalizeIndex(key.hashCode());

        for (int i = offset, j = -1, x = 1; ; i = normalizeIndex(offset + probe(x++))) {
            if (keys[i] == TOMBSTONE) {
                if (j == -1) j = i;
            } else if (keys[i] != nullptr) {
                if (keys[i] == key) {
                    V oldValue = values[i];
                    if (j == -1) {
                        values[i] = val;
                    } else {
                        keys[i] = TOMBSTONE;
                        values[i] = nullptr;
                        keys[j] = key;
                        values[j] = val;
                    }
                    modificationCount++;
                    return oldValue;
                }
            } else {
                if (j == -1) {
                    usedBuckets++;
                    keyCount++;
                    keys[i] = key;
                    values[i] = val;
                } else {
                    keyCount++;
                    keys[j] = key;
                    values[j] = val;
                }
                modificationCount++;
                return nullptr;
            }
        }
    }

    bool hasKey(const K& key) const {
        if (key == nullptr)
            throw std::invalid_argument("Null key");

        setupProbing(key);
        int offset = normalizeIndex(key.hashCode());

        for (int i = offset, j = -1, x = 1; ; i = normalizeIndex(offset + probe(x++))) {
            if (keys[i] == TOMBSTONE) {
                if (j == -1) j = i;
            } else if (keys[i] != nullptr) {
                if (keys[i] == key) {
                    if (j != -1) {
                        keys[j] = keys[i];
                        values[j] = values[i];
                        keys[i] = TOMBSTONE;
                        values[i] = nullptr;
                    }
                    return true;
                }
            } else {
                return false;
            }
        }
    }

    V get(const K& key) const {
        if (key == nullptr)
            throw std::invalid_argument("Null key");

        setupProbing(key);
        int offset = normalizeIndex(key.hashCode());

        for (int i = offset, j = -1, x = 1; ; i = normalizeIndex(offset + probe(x++))) {
            if (keys[i] == TOMBSTONE) {
                if (j == -1) j = i;
            } else if (keys[i] != nullptr) {
                if (keys[i] == key) {
                    if (j != -1) {
                        keys[j] = keys[i];
                        values[j] = values[i];
                        keys[i] = TOMBSTONE;
                        values[i] = nullptr;
                        return values[j];
                    } else {
                        return values[i];
                    }
                }
            } else {
                return nullptr;
            }
        }
    }

    V remove(const K& key) {
        if (key == nullptr)
            throw std::invalid_argument("Null key");

        setupProbing(key);
        int offset = normalizeIndex(key.hashCode());

        for (int i = offset, x = 1; ; i = normalizeIndex(offset + probe(x++))) {
            if (keys[i] == TOMBSTONE) continue;
            if (keys[i] == nullptr) return nullptr;
            if (keys[i] == key) {
                keyCount--;
                modificationCount++;
                V oldValue = values[i];
                keys[i] = TOMBSTONE;
                values[i] = nullptr;
                return oldValue;
            }
        }
    }
};
