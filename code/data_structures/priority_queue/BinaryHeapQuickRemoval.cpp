

#include <vector>
#include <unordered_map>
#include <set>
#include <stdexcept>

template<typename T>
class BinaryHeapQuickRemovals {
private:
    std::vector<T> heap;
    std::unordered_map<T, std::set<int>> map;

public:
    BinaryHeapQuickRemovals() {}

    BinaryHeapQuickRemovals(int sz) : heap(sz) {}

    BinaryHeapQuickRemovals(const std::vector<T>& elems) : heap(elems.begin(), elems.end()) {
        for (int i = std::max(0, static_cast<int>(heap.size()) / 2 - 1); i >= 0; --i)
            sink(i);
    }

    bool isEmpty() {
        return size() == 0;
    }

    void clear() {
        heap.clear();
        map.clear();
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
        return map.find(elem) != map.end();
    }

    void add(const T& elem) {
        if (elem == nullptr) throw std::invalid_argument("Null element");
        heap.push_back(elem);
        int indexOfLastElem = size() - 1;
        mapAdd(elem, indexOfLastElem);
        swim(indexOfLastElem);
    }

    bool remove(const T& element) {
        auto it = map.find(element);
        if (it == map.end()) return false;
        int index = *it->second.rbegin();
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
        mapSwap(heap[i], heap[j], i, j);
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
        mapRemove(removed_data, indexOfLastElem);
        if (i == indexOfLastElem) return removed_data;
        T elem = heap[i];
        sink(i);
        if (heap[i] == elem) swim(i);
        return removed_data;
    }

    void mapAdd(const T& value, int index) {
        map[value].insert(index);
    }

    void mapRemove(const T& value, int index) {
        auto it = map.find(value);
        if (it != map.end()) {
            it->second.erase(index);
            if (it->second.empty()) map.erase(it);
        }
    }

    void mapSwap(const T& val1, const T& val2, int val1Index, int val2Index) {
        map[val1].erase(val1Index);
        map[val2].erase(val2Index);
        map[val1].insert(val2Index);
        map[val2].insert(val1Index);
    }
};
