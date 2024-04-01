

#include <vector>
#include <stdexcept>

class FenwickTreeRangeUpdatePointQuery {
private:
    int N;
    std::vector<long long> originalTree;
    std::vector<long long> currentTree;

public:
    FenwickTreeRangeUpdatePointQuery(std::vector<long long>& values) {
        if (values.empty()) throw std::invalid_argument("Values array cannot be empty!");

        N = values.size();
        values.insert(values.begin(), 0);

        std::vector<long long> fenwickTree = values;
        
        for (int i = 1; i < N; i++) {
            int parent = i + lsb(i);
            if (parent < N) fenwickTree[parent] += fenwickTree[i];
        }

        originalTree = fenwickTree;
        currentTree = fenwickTree;
    }

    void updateRange(int left, int right, long long val) {
        add(left, val);
        add(right + 1, -val);
    }

    void add(int i, long long v) {
        while (i < N) {
            currentTree[i] += v;
            i += lsb(i);
        }
    }

    long long get(int i) {
        return prefixSum(i, currentTree) - prefixSum(i - 1, originalTree);
    }

private:
    long long prefixSum(int i, std::vector<long long>& tree) {
        long long sum = 0;
        while (i != 0) {
            sum += tree[i];
            i &= ~lsb(i);
        }
        return sum;
    }

    static int lsb(int i) {
        return i & -i;
    }
};
