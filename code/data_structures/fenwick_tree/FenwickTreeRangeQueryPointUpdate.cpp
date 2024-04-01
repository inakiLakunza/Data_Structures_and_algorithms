

#include <vector>
#include <iostream>

class FenwickTreeRangeQueryPointUpdate {
private:
    int N;
    std::vector<long long> tree;

public:
    FenwickTreeRangeQueryPointUpdate(int sz) : N(sz + 1), tree(N, 0) {}

    FenwickTreeRangeQueryPointUpdate(std::vector<long long>& values) {
        N = values.size();
        values.insert(values.begin(), 0);
        tree = values;

        for (int i = 1; i < N; ++i) {
            int parent = i + lsb(i);
            if (parent < N) tree[parent] += tree[i];
        }
    }

    int lsb(int i) {
        return i & -i;
    }

    long long prefixSum(int i) {
        long long sum = 0LL;
        while (i != 0) {
            sum += tree[i];
            i &= ~lsb(i);
        }
        return sum;
    }

    long long sum(int left, int right) {
        if (right < left) throw std::invalid_argument("Make sure right >= left");
        return prefixSum(right) - prefixSum(left - 1);
    }

    long long get(int i) {
        return sum(i, i);
    }

    void add(int i, long long v) {
        while (i < N) {
            tree[i] += v;
            i += lsb(i);
        }
    }

    void set(int i, long long v) {
        add(i, v - sum(i, i));
    }

    void print() {
        for (int i = 1; i < N; ++i) {
            std::cout << tree[i] << " ";
        }
        std::cout << std::endl;
    }
};
