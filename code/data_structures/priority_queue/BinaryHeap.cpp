

#include <vector>
#include <algorithm>
#include <stdexcept>

template<typename T>
class BinaryHeap {
private:
    std::vector<T> heap;

public:
    BinaryHeap() {}

    BinaryHeap(int sz) : heap(sz) {}

    BinaryHeap(const std::vector<T>& elems) : heap(elems) {
        int heapSize = heap.size();
        for (int i = std::max(0, heapSize / 2 - 1); i >= 0; --i)
            sink(i);
    }

    bool isEmpty() {
        return size() == 0;
    }

    void clear() {
        heap.clear();
    }

    int size() {
        return heap.size();
    }

    T peek() {
        if (isEmpty()) return T();
        return heap[0];
    }

    T poll() {
        return removeAt(0);
    }

    bool contains(const T& elem) {
        return std::find(heap.begin(), heap.end(), elem) != heap.end();
    }

    void add(const T& elem) {
        heap.push_back(elem);
        swim(size() - 1);
    }

    bool remove(const T& elem) {
        auto it = std::find(heap.begin(), heap.end(), elem);
        if (it == heap.end()) return false;
        int index = std::distance(heap.begin(), it);
        removeAt(index);
        return true;
    }

    bool isMinHeap(int k) {
        int heapSize = size();
        if (k >= heapSize) return true;
        int left = 2 * k + 1;
        int right = 2 * k + 2;
        if (left < heapSize && !less(k, left)) return false;
        if (right < heapSize && !less(k, right)) return false;
        return isMinHeap(left) && isMinHeap(right);
    }

    std::string toString() {
        std::string result;
        for (const auto& elem : heap) {
            result += std::to_string(elem) + " ";
        }
        return result;
    }

private:
    void swim(int k) {
        int parent = (k - 1) / 2;
        while (k > 0 && less(k, parent)) {
            swap(parent, k);
            k = parent;
            parent = (k - 1) / 2;
        }
    }

    void sink(int k) {
        int heapSize = size();
        while (true) {
            int left = 2 * k + 1;
            int right = 2 * k + 2;
            int smallest = left;
            if (right < heapSize && less(right, left)) smallest = right;
            if (left >= heapSize || less(k, smallest)) break;
            swap(smallest, k);
            k = smallest;
        }
    }

    void swap(int i, int j) {
        std::swap(heap[i], heap[j]);
    }

    bool less(int i, int j) {
        return heap[i] < heap[j];
    }

    T removeAt(int i) {
        if (isEmpty()) return T();
        T removed_data = heap[i];
        int indexOfLastElem = size() - 1;
        swap(i, indexOfLastElem);
        heap.pop_back();
        if (i == indexOfLastElem) return removed_data;
        T elem = heap[i];
        sink(i);
        if (heap[i] == elem) swim(i);
        return removed_data;
    }
};
