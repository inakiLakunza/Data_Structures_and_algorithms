

class AVLTreeRecursive:

    # Node class, apart from the value it contains
    # in each node we have to save its balance factor (bf),
    # its height value, and the pointers which reference its
    # left and right children 
    class Node:
        def __init__(self, value):
            self.bf = 0  # Balance Factor
            self.value = value
            self.height = 0
            self.left = None
            self.right = None

    # When we initialize the BBST we initialize
    # it with a null (None) node. And we will
    # count the number of nodes it contains
    def __init__(self):
        self.root = None
        self.nodeCount = 0

    # In order to get the height of the tree
    # we will use the root node and get its height
    # we can do this easily since each node has the
    # information of its height, and we always have a
    # pointer to the root node of the tree
    def height(self):
        if self.root is None:
            return 0
        return self.root.height

    # The size of the tree will be given by
    # the number of nodes it contains, we can
    # easily get it since it is an attribute of the tree
    def size(self):
        return self.nodeCount

    def is_empty(self):
        return self.size() == 0

    
    # Using a leading underscore (lowbar) in Python typically
    # indicates that a method or attribute is intended for
    # internal use within a class and is not part of the public interface.
    # This convention is known as "name mangling" and helps to differentiate
    # between methods or attributes meant for internal use and those
    # meant to be accessed from outside the class.

    # Here, contains is the public method that is meant to be accessed by
    # users of the class, while _contains is intended for internal use
    # within the class. The leading underscore signals to other developers
    # that _contains is not part of the public API and should not
    # be relied upon externally.

    # The importance of using leading underscores in this context lies in
    # maintaining encapsulation and abstraction. By hiding implementation
    # details within the class and exposing only the necessary methods and
    # attributes, you can ensure that users interact with the class in a way
    # that is less prone to errors and unintended side effects. It also allows
    # for easier maintenance and refactoring of the codebase since internal
    # changes won't affect external code that relies on the public interface.
    def contains(self, value):
        return self._contains(self.root, value)


    # We will transverse the tree looking for the node we want.
    # THE DATA WE USE MUST BE COMPARABLE, so we will start from
    # the root node and traverse the tree finding the node we want
    # we will compare the current node and the one we are looking
    # for and depending on the comparison's outcome we will
    # traverse the tree accordingly
    def _contains(self, node, value):
        if node is None:
            return False
        cmp = value - node.value
        if cmp < 0:
            return self._contains(node.left, value)
        elif cmp > 0:
            return self._contains(node.right, value)
        else:
            return True

    # We do not allow repeated values, so we first have to check
    # if the tree already contains that value. Then we will
    # use our internal insert method to add it to the tree
    # and we will add 1 to the node counter of the tree.
    # We will use a boolean to indicate if the node
    # has been inserted in the tree or not
    def insert(self, value):
        if value is None:
            return False
        if not self.contains(value):
            self.root = self._insert(self.root, value)
            self.nodeCount += 1
            return True
        return False


    # We make the insertion as seen in the notes,
    # using rotations and updating the tree so
    # to maintain the tree invariant and to
    # maintain its balance
    def _insert(self, node, value):
        if node is None:
            return self.Node(value)
        cmp = value - node.value
        if cmp < 0:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)
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
                return self._right_rotation(node)
            else:
                return self._left_right_case(node)
        elif node.bf == 2:
            if node.right.bf >= 0:
                return self._left_rotation(node)
            else:
                return self._right_left_case(node)
        return node

    def _left_rotation(self, node):
        new_parent = node.right
        node.right = new_parent.left
        new_parent.left = node
        self._update(node)
        self._update(new_parent)
        return new_parent

    def _right_rotation(self, node):
        new_parent = node.left
        node.left = new_parent.right
        new_parent.right = node
        self._update(node)
        self._update(new_parent)
        return new_parent

    def _left_right_case(self, node):
        node.left = self._left_rotation(node.left)
        return self._right_rotation(node)

    def _right_left_case(self, node):
        node.right = self._right_rotation(node.right)
        return self._left_rotation(node)

    def remove(self, elem):
        if elem is None:
            return False
        if self.contains(elem):
            self.root = self._remove(self.root, elem)
            self.nodeCount -= 1
            return True
        return False

    # The removal is almost similar to the removal
    # process of Binary Search Trees, but adding
    # the update and balance methods
    def _remove(self, node, elem):
        if node is None:
            return None
        cmp = elem - node.value
        if cmp < 0:
            node.left = self._remove(node.left, elem)
        elif cmp > 0:
            node.right = self._remove(node.right, elem)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.height > node.right.height:
                    successor_value = self._find_max(node.left)
                    node.value = successor_value
                    node.left = self._remove(node.left, successor_value)
                else:
                    successor_value = self._find_min(node.right)
                    node.value = successor_value
                    node.right = self._remove(node.right, successor_value)
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

    def __str__(self):
        return self._get_tree_display(self.root)

    def _get_tree_display(self, root):
        if root is None:
            return ''
        stack = [root]
        lines = []
        while stack:
            new_stack = []
            line = []
            for node in stack:
                if node is not None:
                    line.append(str(node.value))
                    new_stack.append(node.left)
                    new_stack.append(node.right)
                else:
                    line.append(' ')
            if any(new_stack):
                lines.append(line)
            stack = new_stack
        return '\n'.join([' '.join(line) for line in lines if line])


# Example usage:
if __name__ == "__main__":
    tree = AVLTreeRecursive()
    values = [10, 5, 3, 6, 15, 12, 18]
    for value in values:
        tree.insert(value)
    print("AVL Tree:")
    print(tree)
