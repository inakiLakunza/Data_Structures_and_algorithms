

class AVLTreeRecursiveOptimized:
    class Node:
        def __init__(self, value):
            self.bf = 0
            self.value = value
            self.height = 0
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None
        self.nodeCount = 0
        self.TOKEN = self.Node(None)

    def height(self):
        if self.root is None:
            return 0
        return self.root.height

    def size(self):
        return self.nodeCount

    def is_empty(self):
        return self.size() == 0

    def contains(self, value):
        node = self.root
        while node is not None:
            cmp = value - node.value
            if cmp < 0:
                node = node.left
            elif cmp > 0:
                node = node.right
            else:
                return True
        return False

    def insert(self, value):
        if value is None:
            return False
        new_root = self._insert(self.root, value)
        inserted_node = new_root is not self.TOKEN
        if inserted_node:
            self.nodeCount += 1
            self.root = new_root
        return inserted_node

    def _insert(self, node, value):
        if node is None:
            return self.Node(value)
        cmp = value - node.value
        if cmp < 0:
            new_left_node = self._insert(node.left, value)
            if new_left_node is self.TOKEN:
                return self.TOKEN
            node.left = new_left_node
        elif cmp > 0:
            new_right_node = self._insert(node.right, value)
            if new_right_node is self.TOKEN:
                return self.TOKEN
            node.right = new_right_node
        else:
            return self.TOKEN
        self._update(node)
        return self._balance(node)

    def _update(self, node):
        left_node_height = -1 if node.left is None else node.left.height
        right_node_height = -1 if node.right is None else node.right.height
        node.height = 1 + max(left_node_height, right_node_height)
        node.bf = right_node_height - left_node_height

    def _balance(self, node):
        if node.bf == -2:
            if node.left.bf <= 0:
                return self.right_rotation(node)
            else:
                return self.left_right_case(node)
        elif node.bf == 2:
            if node.right.bf >= 0:
                return self.left_rotation(node)
            else:
                return self.right_left_case(node)
        return node

    def left_left_case(self, node):
        return self.right_rotation(node)

    def left_right_case(self, node):
        node.left = self.left_rotation(node.left)
        return self.left_left_case(node)

    def right_right_case(self, node):
        return self.left_rotation(node)

    def right_left_case(self, node):
        node.right = self.right_rotation(node.right)
        return self.right_right_case(node)

    def left_rotation(self, node):
        new_parent = node.right
        node.right = new_parent.left
        new_parent.left = node
        self._update(node)
        self._update(new_parent)
        return new_parent

    def right_rotation(self, node):
        new_parent = node.left
        node.left = new_parent.right
        new_parent.right = node
        self._update(node)
        self._update(new_parent)
        return new_parent

    def remove(self, elem):
        new_root = self._remove(self.root, elem)
        removed_node = new_root is not self.TOKEN or new_root is None
        if removed_node:
            self.root = new_root
            self.nodeCount -= 1
            return True
        return False

    def _remove(self, node, elem):
        if node is None:
            return self.TOKEN
        cmp = elem - node.value
        if cmp < 0:
            new_left_node = self._remove(node.left, elem)
            if new_left_node is self.TOKEN:
                return self.TOKEN
            node.left = new_left_node
        elif cmp > 0:
            new_right_node = self._remove(node.right, elem)
            if new_right_node is self.TOKEN:
                return self.TOKEN
            node.right = new_right_node
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.height > node.right.height:
                    successor_value = self._find_max(node.left)
                    node.value = successor_value
                    replacement = self._remove(node.left, successor_value)
                    if replacement is self.TOKEN:
                        return self.TOKEN
                    node.left = replacement
                else:
                    successor_value = self._find_min(node.right)
                    node.value = successor_value
                    replacement = self._remove(node.right, successor_value)
                    if replacement is self.TOKEN:
                        return self.TOKEN
                    node.right = replacement
        self._update(node)
        return self._balance(node)

    def _find_min(self, node):
        while node.left is not None:
            node = node.left
        return node.value

    def _find_max(self, node):
        while node.right is not None:
            node = node.right
        return node.value

    def __iter__(self):
        expected_node_count = self.nodeCount
        stack = [self.root]

        def next_node():
            nonlocal stack
            nonlocal expected_node_count
            while stack:
                current_node = stack.pop()
                if current_node is None:
                    continue
                if current_node.right is not None:
                    stack.append(current_node.right)
                if current_node.left is not None:
                    stack.append(current_node.left)
                return current_node.value
            if expected_node_count != self.nodeCount:
                raise RuntimeError("Tree modified during iteration")
            raise StopIteration()

        return iter(next_node, None)

    def validate_BST_invariant(self, node):
        if node is None:
            return True
        val = node.value
        is_valid = True
        if node.left is not None:
            is_valid = is_valid and node.left.value < val
        if node.right is not None:
            is_valid = is_valid and node.right.value > val
        return is_valid and self.validate_BST_invariant(node.left) and self.validate_BST_invariant(node.right)
