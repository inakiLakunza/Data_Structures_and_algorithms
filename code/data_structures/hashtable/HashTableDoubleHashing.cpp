

#include <iostream>
#include <vector>
#include <stdexcept>
#include <cmath>
#include "HashTableOpenAddressingBase.cpp"

template<typename K, typename V>
class HashTableDoubleHashing : public HashTableOpenAddressingBase<K, V> {
private:
    int hash;

public:
    HashTableDoubleHashing(int capacity = 7, double loadFactor = 0.65) : HashTableOpenAddressingBase<K, V>(capacity, loadFactor), hash(0) {}

    void setupProbing(const K& key) override {
        hash = this->normalizeIndex(key.hash_code2());
        if (hash == 0)
            hash = 1;
    }

    int probe(int x) override {
        return x * hash;
    }

    void adjustCapacity() override {
        while (!isProbablePrime(this->capacity))
            this->capacity++;
    }

    static bool isProbablePrime(int n, int k = 20) {
        return (n >= 3) ? (std::pow(2, n - 1) % n == 1) : (n == 2);
    }
};
