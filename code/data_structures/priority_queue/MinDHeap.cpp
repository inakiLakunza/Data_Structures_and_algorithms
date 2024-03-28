

#include <vector>
#include <stdexcept>

template<typename T>
class MinDHeap {
private:
    std::vector<T> heap;
    std::vector<int> child, parent;
    int d, n, sz;

public:
    MinDHeap(int degree, int maxNodes) : d(std::max(2, degree)), n(std::max(d, maxNodes)), heap(n), child(n), parent(n), sz(0) {
        for (int i = 0; i < n; ++i) {
            parent[i] = (i - 1) / d;
            child[i] = i * d + 1;
        }
    }

    int size() {
        return sz;
    }

    bool isEmpty() {
        return sz == 0;
    }

    void clear() {
        heap.clear();
        child.clear();
        parent.clear();
        sz = 0;
    }

    T peek() {
        if (isEmpty()) return T();
        return heap[0];
    }

    T poll() {
        if (isEmpty()) return T();
        T root = heap[0];
        heap[0] = heap[--sz];
        heap[sz] = T();
        sink(0);
        return root;
    }

    void add(const T& elem) {
        if (elem == nullptr) throw std::invalid_argument("No null elements please :)");
        heap[sz] = elem;
        swim(sz);
        ++sz;
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
        int index = -1;
        int from = child[i];
        int to = std::min(sz, from + d);
        for (int j = from; j < to; ++j)
            if (less(j, i)) {
                index = i = j;
            }
        return index;
    }

    bool less(int i, int j) {
        return heap[i] < heap[j];
    }

    void swap(int i, int j) {
        T tmp = heap[i];
        heap[i] = heap[j];
        heap[j] = tmp;
    }
};
