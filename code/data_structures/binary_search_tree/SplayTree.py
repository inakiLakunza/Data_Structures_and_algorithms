class SplayTree:
    class BinaryTree:
        def __init__(self, data):
            if data is None:
                raise ValueError("Null data not allowed into tree")
            self.data = data
            self.leftChild = None
            self.rightChild = None

        def getLeft(self):
            return self.leftChild

        def setLeft(self, leftChild):
            self.leftChild = leftChild

        def getRight(self):
            return self.rightChild

        def setRight(self, rightChild):
            self.rightChild = rightChild

        def getText(self):
            return str(self.data)

        def getData(self):
            return self.data

        def setData(self, data):
            if data is None:
                raise ValueError("Null data not allowed into tree")
            self.data = data

        def __str__(self):
            return self.getTreeDisplay()

        def getTreeDisplay(self):
            # You need to implement the tree display logic here
            pass

    def __init__(self, root=None):
        self.root = root

    def getRoot(self):
        return self.root

    def search(self, node):
        if self.root is None:
            return None
        self.root = self.splayUtil(self.root, node)
        return self.root.getData() if self.root.getData() == node else None

    def insert(self, node):
        if self.root is None:
            self.root = self.BinaryTree(node)
            return self.root
        self.splay(node)
        left, right = self.split(node)
        self.root = self.BinaryTree(node)
        self.root.setLeft(left)
        self.root.setRight(right)
        return self.root

    def delete(self, node):
        if self.root is None:
            return None
        search_result = self.splay(node)
        if search_result.getData() != node:
            return None
        left_subtree = self.root.getLeft()
        right_subtree = self.root.getRight()
        self.root.setLeft(None)
        self.root.setRight(None)
        self.root = self.join(left_subtree, right_subtree)
        return self.root

    def findMax(self, root=None):
        temp = root if root else self.root
        while temp.getRight() is not None:
            temp = temp.getRight()
        return temp.getData()

    def findMin(self, root=None):
        temp = root if root else self.root
        while temp.getLeft() is not None:
            temp = temp.getLeft()
        return temp.getData()

    def __str__(self):
        return "Elements:" + str(self.inorder(self.root, [])) if self.root else None

    def rightRotate(self, node):
        p = node.getLeft()
        node.setLeft(p.getRight())
        p.setRight(node)
        return p

    def leftRotate(self, node):
        p = node.getRight()
        node.setRight(p.getLeft())
        p.setLeft(node)
        return p

    def splayUtil(self, root, key):
        if root is None or root.getData() == key:
            return root
        if root.getData() > key:
            if root.getLeft() is None:
                return root
            if root.getLeft().getData() > key:
                root.getLeft().setLeft(self.splayUtil(root.getLeft().getLeft(), key))
                root = self.rightRotate(root)
            elif root.getLeft().getData() < key:
                root.getLeft().setRight(self.splayUtil(root.getLeft().getRight(), key))
                if root.getLeft().getRight() is not None:
                    root.setLeft(self.leftRotate(root.getLeft()))
            return root.getLeft() if root.getLeft() is None else self.rightRotate(root)
        else:
            if root.getRight() is None:
                return root
            if root.getRight().getData() > key:
                root.getRight().setLeft(self.splayUtil(root.getRight().getLeft(), key))
                if root.getRight().getLeft() is not None:
                    root.setRight(self.rightRotate(root.getRight()))
            elif root.getRight().getData() < key:
                root.getRight().setRight(self.splayUtil(root.getRight().getRight(), key))
                root = self.leftRotate(root)
            return root.getRight() if root.getRight() is None else self.leftRotate(root)

    def splay(self, node):
        if self.root is None:
            return None
        self.root = self.splayUtil(self.root, node)
        return self.root

    def split(self, node):
        right = None
        left = None
        if node > self.root.getData():
            right = self.root.getRight()
            left = self.root
            left.setRight(None)
        else:
            left = self.root.getLeft()
            right = self.root
            right.setLeft(None)
        return [left, right]

    def join(self, L, R):
        if L is None:
            self.root = R
            return R
        self.root = self.splayUtil(L, self.findMax(L))
        self.root.setRight(R)
        return self.root

    def inorder(self, root, sorted):
        if root is None:
            return sorted
        self.inorder(root.getLeft(), sorted)
        sorted.append(root.getData())
        self.inorder(root.getRight(), sorted)
        return sorted
