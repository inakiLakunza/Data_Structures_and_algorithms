#include <iostream>
#include <stdexcept>

template <typename T>
class Array {
private:
    T* arr;
    int len = 0;         // length user thinks array is
    int capacity = 0;    // actual array size

public:
    Array() : Array(16) {} // If no array capacity is inserted, use 16

    Array(int capacity) {
        if (capacity < 0) throw std::invalid_argument("Illegal Capacity: " + std::to_string(capacity));
        this->capacity = capacity;
        arr = new T[capacity];
    }

    ~Array() {
        delete[] arr;
    }

    int size() const { return len; }
    bool isEmpty() const { return size() == 0; }

    T get(int index) const { return arr[index]; }
    void set(int index, T elem) { arr[index] = elem; }

    void clear() {
        for (int i = 0; i < capacity; i++)
            arr[i] = T();
        len = 0;
    }

    void add(T elem) {
        // Resizing
        if (len + 1 >= capacity) {
            if (capacity == 0) capacity = 1;
            else capacity *= 2; // double the size
            T* new_arr = new T[capacity];
            for (int i = 0; i < len; i++)
                new_arr[i] = arr[i];
            delete[] arr;
            arr = new_arr; // arr has extra nulls padded
        }
        arr[len++] = elem;
    }

    T removeAt(int rm_index) {
        if (rm_index >= len || rm_index < 0) throw std::out_of_range("Index out of bounds");
        T data = arr[rm_index];
        T* new_arr = new T[len - 1];
        for (int i = 0, j = 0; i < len; i++, j++)
            if (i == rm_index) j--; // Skip over rm_index by fixing j temporarily
            else new_arr[j] = arr[i];
        delete[] arr;
        arr = new_arr;
        capacity = --len;
        return data;
    }

    bool remove(const T& obj) {
        for (int i = 0; i < len; i++) {
            if (arr[i] == obj) {
                removeAt(i);
                return true;
            }
        }
        return false;
    }

    int indexOf(const T& obj) const {
        for (int i = 0; i < len; i++)
            if (arr[i] == obj)
                return i;
        return -1;
    }

    bool contains(const T& obj) const {
        return indexOf(obj) != -1;
    }

    // Iterator is still fast but not as fast as iterative for loop
    class Iterator {
    private:
        int index = 0;
        const Array<T>* array;

    public:
        Iterator(const Array<T>& arr) : array(&arr) {}

        bool hasNext() const { return index < array->len; }
        T next() { return array->arr[index++]; }
    };

    Iterator iterator() const {
        return Iterator(*this);
    }

    std::string toString() const {
        if (len == 0) return "[]";
        else {
            std::string result = "[";
            for (int i = 0; i < len - 1; i++)
                result += std::to_string(arr[i]) + ", ";
            return result + std::to_string(arr[len - 1]) + "]";
        }
    }
};
