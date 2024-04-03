

#include <iostream>
#include <stack>
#include <stdexcept>

template <typename T>
class AVLTreeRecursive {
private:
    struct Node {
        int bf;
        T value;
        int height;
        Node* left;
        Node* right;

        Node(const T& val) : value(val), bf(0), height(0), left(nullptr), right(nullptr) {}
    };

    Node* root;
    int nodeCount;

    Node* insert(Node* node, const T& value) {
        if (node == nullptr) {
            nodeCount++;
            return new Node(value);
        }

        int cmp = value - node->value;

        if (cmp < 0) {
            node->left = insert(node->left, value);
        } else if (cmp > 0) {
            node->right = insert(node->right, value);
        } else {
            return node; // Duplicate value
        }

        update(node);
        return balance(node);
    }

    void update(Node* node) {
        int leftNodeHeight = (node->left == nullptr) ? -1 : node->left->height;
        int rightNodeHeight = (node->right == nullptr) ? -1 : node->right->height;

        node->height = 1 + std::max(leftNodeHeight, rightNodeHeight);
        node->bf = rightNodeHeight - leftNodeHeight;
    }

    Node* balance(Node* node) {
        if (node->bf == -2) {
            if (node->left->bf <= 0) {
                return rightRotation(node);
            } else {
                return leftRightCase(node);
            }
        } else if (node->bf == 2) {
            if (node->right->bf >= 0) {
                return leftRotation(node);
            } else {
                return rightLeftCase(node);
            }
        }
        return node;
    }

    Node* rightRotation(Node* node) {
        Node* newParent = node->left;
        node->left = newParent->right;
        newParent->right = node;
        update(node);
        update(newParent);
        return newParent;
    }

    Node* leftRotation(Node* node) {
        Node* newParent = node->right;
        node->right = newParent->left;
        newParent->left = node;
        update(node);
        update(newParent);
        return newParent;
    }

    Node* leftLeftCase(Node* node) {
        return rightRotation(node);
    }

    Node* leftRightCase(Node* node) {
        node->left = leftRotation(node->left);
        return leftLeftCase(node);
    }

    Node* rightRightCase(Node* node) {
        return leftRotation(node);
    }

    Node* rightLeftCase(Node* node) {
        node->right = rightRotation(node->right);
        return rightRightCase(node);
    }

    Node* remove(Node* node, const T& elem) {
        if (node == nullptr) return nullptr;

        int cmp = elem - node->value;

        if (cmp < 0) {
            node->left = remove(node->left, elem);
        } else if (cmp > 0) {
            node->right = remove(node->right, elem);
        } else {
            if (node->left == nullptr || node->right == nullptr) {
                Node* temp = (node->left == nullptr) ? node->right : node->left;
                if (temp == nullptr) {
                    temp = node;
                    node = nullptr;
                } else {
                    *node = *temp;
                }
                delete temp;
            } else {
                Node* successor = node->right;
                while (successor->left != nullptr) successor = successor->left;
                node->value = successor->value;
                node->right = remove(node->right, successor->value);
            }
        }

        if (node != nullptr) {
            update(node);
            return balance(node);
        }
        return node;
    }

    void destroy(Node* node) {
        if (node != nullptr) {
            destroy(node->left);
            destroy(node->right);
            delete node;
        }
    }

public:
    AVLTreeRecursive() : root(nullptr), nodeCount(0) {}

    ~AVLTreeRecursive() {
        destroy(root);
    }

    int height() const {
        return (root == nullptr) ? 0 : root->height;
    }

    int size() const {
        return nodeCount;
    }

    bool isEmpty() const {
        return size() == 0;
    }

    bool contains(const T& value) const {
        Node* node = root;
        while (node != nullptr) {
            int cmp = value - node->value;
            if (cmp < 0) {
                node = node->left;
            } else if (cmp > 0) {
                node = node->right;
            } else {
                return true;
            }
        }
        return false;
    }

    bool insert(const T& value) {
        if (contains(value)) return false;
        root = insert(root, value);
        return true;
    }

    bool remove(const T& value) {
        if (!contains(value)) return false;
        root = remove(root, value);
        nodeCount--;
        return true;
    }

    class Iterator {
    private:
        std::stack<Node*> stack;
        Node* trav;
        int expectedNodeCount;

    public:
        Iterator(Node* root, int count) : trav(root), expectedNodeCount(count) {
            while (trav != nullptr) {
                stack.push(trav);
                trav = trav->left;
            }
        }

        bool hasNext() const {
            return trav != nullptr || !stack.empty();
        }

        T next() {
            if (expectedNodeCount != nodeCount) {
                throw std::runtime_error("Concurrent Modification Exception");
            }
            if (!hasNext()) {
                throw std::runtime_error("No such element");
            }
            Node* node = stack.top();
            stack.pop();
            trav = node->right;
            while (trav != nullptr) {
                stack.push(trav);
                trav = trav->left;
            }
            return node->value;
        }
    };

    Iterator begin() const {
        return Iterator(root, nodeCount);
    }

    Iterator end() const {
        return Iterator(nullptr, nodeCount);
    }

    bool validateBSTInvariant(Node* node) const {
        if (node == nullptr) return true;
        bool isValid = true;
        if (node->left != nullptr) isValid = isValid && node->left->value < node->value;
        if (node->right != nullptr) isValid = isValid && node->right->value > node->value;
        return isValid && validateBSTInvariant(node->left) && validateBSTInvariant(node->right);
    }
};
