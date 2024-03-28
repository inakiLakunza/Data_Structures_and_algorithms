

#include <vector>
#include <stdexcept>

class UnionFind {
private:
    int size;
    std::vector<int> sz;
    std::vector<int> id;
    int numComponents;

public:
    UnionFind(int size) {
        if (size <= 0)
            throw std::invalid_argument("Size <= 0 is not allowed");

        this->size = this->numComponents = size;
        sz.resize(size, 1);
        id.resize(size);

        for (int i = 0; i < size; i++) {
            id[i] = i; // Link to itself (self root)
        }
    }

    int find(int p) {
        int root = p;
        while (root != id[root])
            root = id[root];

        // Path Compression
        while (p != root) {
            int next = id[p];
            id[p] = root;
            p = next;
        }

        return root;
    }

    bool connected(int p, int q) {
        return find(p) == find(q);
    }

    int componentSize(int p) {
        return sz[find(p)];
    }

    int getSize() {
        return size;
    }

    int components() {
        return numComponents;
    }

    void unify(int p, int q) {
        if (connected(p, q))
            return;

        int root1 = find(p);
        int root2 = find(q);

        // Merge smaller component/set into the larger one.
        if (sz[root1] < sz[root2]) {
            sz[root2] += sz[root1];
            id[root1] = root2;
            sz[root1] = 0;
        } else {
            sz[root1] += sz[root2];
            id[root2] = root1;
            sz[root2] = 0;
        }

        numComponents--;
    }
};
