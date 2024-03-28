

#include <vector>
#include <stdexcept>
#include <algorithm> // for std::min and std::max

template<typename T>
class MinIndexedDHeap {
private:
    std::vector<T> values;
    std::vector<int> pm, im, child, parent;
    int sz, N, D;

public:
    MinIndexedDHeap(int degree, int maxSize) : D(std::max(2, degree)), N(std::max(D + 1, maxSize)), values(N), pm(N), im(N), child(N), parent(N), sz(0) {
        for (int i = 0; i < N; ++i) {
            parent[i] = (i - 1) / D;
            child[i] = i * D + 1;
            pm[i] = im[i] = -1;
        }
    }

    int size() {
        return sz;
    }

    bool isEmpty() {
        return sz == 0;
    }

    bool contains(int ki) {
        keyInBoundsOrThrow(ki);
        return pm[ki] != -1;
    }

    int peekMinKeyIndex() {
        isNotEmptyOrThrow();
        return im[0];
    }

    int pollMinKeyIndex() {
        int minki = peekMinKeyIndex();
        deleteKey(minki);
        return minki;
    }

    T peekMinValue() {
        isNotEmptyOrThrow();
        return values[im[0]];
    }

    T pollMinValue() {
        T minValue = peekMinValue();
        deleteKey(peekMinKeyIndex());
        return minValue;
    }

    void insert(int ki, T value) {
        if (contains(ki)) throw std::invalid_argument("index already exists; received: " + ki);
        valueNotNullOrThrow(value);
        pm[ki] = sz;
        im[sz] = ki;
        values[ki] = value;
        swim(sz++);
    }

    T valueOf(int ki) {
        keyExistsOrThrow(ki);
        return values[ki];
    }

    T deleteKey(int ki) {
        keyExistsOrThrow(ki);
        int i = pm[ki];
        swap(i, --sz);
        sink(i);
        swim(i);
        T value = values[ki];
        values[ki] = T();
        pm[ki] = -1;
        im[sz] = -1;
        return value;
    }

    T update(int ki, T value) {
        keyExistsAndValueNotNullOrThrow(ki, value);
        int i = pm[ki];
        T oldValue = values[ki];
        values[ki] = value;
        sink(i);
        swim(i);
        return oldValue;
    }

    void decrease(int ki, T value) {
        keyExistsAndValueNotNullOrThrow(ki, value);
        if (less(value, values[ki])) {
            values[ki] = value;
            swim(pm[ki]);
        }
    }

    void increase(int ki, T value) {
        keyExistsAndValueNotNullOrThrow(ki, value);
        if (less(values[ki], value)) {
            values[ki] = value;
            sink(pm[ki]);
        }
    }

    bool isMinHeap() {
        return isMinHeap(0);
    }

private:
    void sink(int i) {
        int j = minChild(i);
        while (j != -1) {
            swap(i, j);
            i = j;
            j = minChild(i);
        }
    }

    void swim(int i) {
        while (less(i, parent[i])) {
            swap(i, parent[i]);
            i = parent[i];
        }
    }

    int minChild(int i) {
        int index = -1, from = child[i], to = std::min(sz, from + D);
        for (int j = from; j < to; ++j) {
            if (less(j, i)) {
                index = i = j;
            }
        }
        return index;
    }

    void swap(int i, int j) {
        pm[im[j]] = i;
        pm[im[i]] = j;
        std::swap(im[i], im[j]);
    }

    bool less(int i, int j) {
        return values[im[i]] < values[im[j]];
    }

    bool less(T obj1, T obj2) {
        return obj1 < obj2;
    }

    void isNotEmptyOrThrow() {
        if (isEmpty()) throw std::out_of_range("Priority queue underflow");
    }

    void keyExistsAndValueNotNullOrThrow(int ki, T value) {
        keyExistsOrThrow(ki);
        valueNotNullOrThrow(value);
    }

    void keyExistsOrThrow(int ki) {
        if (!contains(ki)) throw std::out_of_range("Index does not exist; received: " + ki);
    }

    void valueNotNullOrThrow(T value) {
        if (value == NULL) throw std::invalid_argument("value cannot be null");
    }

    void keyInBoundsOrThrow(int ki) {
        if (ki < 0 || ki >= N)
            throw std::invalid_argument("Key index out of bounds; received: " + ki);
    }

    bool isMinHeap(int i) {
        int from = child[i], to = std::min(sz, from + D);
        for (int j = from; j < to; ++j) {
            if (!less(i, j)) return false;
            if (!isMinHeap(j)) return false;
        }
        return true;
    }
};
