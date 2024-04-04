

#include "MinIndexDHeap.cpp"

template <typename T>
class MinIndexedBinaryHeap : public MinIndexedDHeap<T> {
public:
    MinIndexedBinaryHeap(int maxSize) : MinIndexedDHeap<T>(2, maxSize) {}
};