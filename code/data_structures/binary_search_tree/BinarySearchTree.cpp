#include <iostream>
#include <vector>
#include <stdexcept>

template<typename T>
class SplayTree {
private:
    template<typename U>
    class BinaryTree {
    private:
        U data;
        BinaryTree<U>* leftChild;
        BinaryTree<U>* rightChild;

    public:
        BinaryTree(U value) : data(value), leftChild(nullptr), rightChild(nullptr) {
            if (value == nullptr) {
                throw std::invalid_argument("Null data not allowed into tree");
            }
        }

        BinaryTree<U>* getLeft() {
            return leftChild;
        }

        void setLeft(BinaryTree<U>* left) {
            leftChild = left;
        }

        BinaryTree<U>* getRight() {
            return rightChild;
        }

        void setRight(BinaryTree<U>* right) {
            rightChild = right;
        }

        U getData() {
            return data;
        }

        void setData(U value) {
            if (value == nullptr) {
                throw std::invalid_argument("Null data not allowed into tree");
            }
            data = value;
        }

        std::string getText() {
            return std::to_string(data);
        }

        std::string getTreeDisplay() {
            // You need to implement the tree display logic here
            return "";
        }
    };

    BinaryTree<T>* root;

    BinaryTree<T>* rightRotate(BinaryTree<T>* node) {
        BinaryTree<T>* p = node->getLeft();
        node->setLeft(p->getRight());
        p->setRight(node);
        return p;
    }

    BinaryTree<T>* leftRotate(BinaryTree<T>* node) {
        BinaryTree<T>* p = node->getRight();
        node->setRight(p->getLeft());
        p->setLeft(node);
        return p;
    }

    BinaryTree<T>* splayUtil(BinaryTree<T>* root, T key) {
        if (root == nullptr || root->getData() == key) {
            return root;
        }

        if (root->getData() > key) {
            if (root->getLeft() == nullptr) {
                return root;
            }
            if (root->getLeft()->getData() > key) {
                root->getLeft()->setLeft(splayUtil(root->getLeft()->getLeft(), key));
                root = rightRotate(root);
            } else if (root->getLeft()->getData() < key) {
                root->getLeft()->setRight(splayUtil(root->getLeft()->getRight(), key));
                if (root->getLeft()->getRight() != nullptr) {
                    root->setLeft(leftRotate(root->getLeft()));
                }
            }
            return (root->getLeft() == nullptr) ? root : rightRotate(root);
        } else {
            if (root->getRight() == nullptr) {
                return root;
            }
            if (root->getRight()->getData() > key) {
                root->getRight()->setLeft(splayUtil(root->getRight()->getLeft(), key));
                if (root->getRight()->getLeft() != nullptr) {
                    root->setRight(rightRotate(root->getRight()));
                }
            } else if (root->getRight()->getData() < key) {
                root->getRight()->setRight(splayUtil(root->getRight()->getRight(), key));
                root = leftRotate(root);
            }
            return (root->getRight() == nullptr) ? root : leftRotate(root);
        }
    }

    BinaryTree<T>* splay(T node) {
        if (root == nullptr) {
            return nullptr;
        }
        root = splayUtil(root, node);
        return root;
    }

public:
    SplayTree() : root(nullptr) {}

    BinaryTree<T>* getRoot() {
        return root;
    }

    BinaryTree<T>* search(T node) {
        if (root == nullptr) {
            return nullptr;
        }
        root = splayUtil(root, node);
        return (root->getData() == node) ? root : nullptr;
    }

    BinaryTree<T>* insert(T node) {
        if (root == nullptr) {
            root = new BinaryTree<T>(node);
            return root;
        }
        splay(node);
        auto l_r = split(node);
        auto left = l_r[0];
        auto right = l_r[1];
        root = new BinaryTree<T>(node);
        root->setLeft(left);
        root->setRight(right);
        return root;
    }

    BinaryTree<T>* deleteNode(T node) {
        if (root == nullptr) {
            return nullptr;
        }
        BinaryTree<T>* searchResult = splay(node);
        if (searchResult->getData() != node) {
            return nullptr;
        }
        BinaryTree<T>* leftSubtree = root->getLeft();
        BinaryTree<T>* rightSubtree = root->getRight();
        root->setLeft(nullptr);
        root->setRight(nullptr);
        root = join(leftSubtree, rightSubtree);
        return root;
    }

    T findMax(BinaryTree<T>* root = nullptr) {
        BinaryTree<T>* temp = root ? root : this->root;
        while (temp->getRight() != nullptr) {
            temp = temp->getRight();
        }
        return temp->getData();
    }

    T findMin(BinaryTree<T>* root = nullptr) {
        BinaryTree<T>* temp = root ? root : this->root;
        while (temp->getLeft() != nullptr) {
            temp = temp->getLeft();
        }
        return temp->getData();
    }

    std::vector<T> inorder(BinaryTree<T>* root, std::vector<T> sorted) {
        if (root == nullptr) {
            return sorted;
        }
        inorder(root->getLeft(), sorted);
        sorted.push_back(root->getData());
        inorder(root->getRight(), sorted);
        return sorted;
    }

    std::vector<BinaryTree<T>*> split(T node) {
        BinaryTree<T>* right;
        BinaryTree<T>* left;
        if (node > root->getData()) {
            right = root->getRight();
            left = root;
            left->setRight(nullptr);
        } else {
            left = root->getLeft();
            right = root;
            right->setLeft(nullptr);
        }
        std::vector<BinaryTree<T>*> l_r;
        l_r.push_back(left);
        l_r.push_back(right);
        return l_r;
    }

    BinaryTree<T>* join(BinaryTree<T>* L, BinaryTree<T>* R) {
        if (L == nullptr) {
            root = R;
            return R;
        }
        root = splayUtil(L, findMax(L));
        root->setRight(R);
        return root;
    }
};
