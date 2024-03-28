

class UnionFind:

    # we have to know the number of elements that there
    # will be in our union find, it is necessary
    def __init__(self, size):
        if size <= 0:
            raise ValueError("Size <= 0 is not allowed")
        
        self.size = size
        self.numComponents = size
        self.sz = [1] * size

        # we will use the id array to point
        # to the parent node of i, and if the id
        # of the index i is equal to i, then
        # we know that i is a root node
        # and this is our way of accessing the
        # bijections that we have created
        self.id = [i for i in range(size)]

    def find(self, p):
        root = p
        # loop until we find a node pointing
        # at itself, so we know that it
        # is a root node
        while root != self.id[root]:
            root = self.id[root]
        
        # Path Compression
        while p != root:
            next_p = self.id[p]
            self.id[p] = root
            p = next_p
        
        return root

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def component_size(self, p):
        return self.sz[self.find(p)]

    def size(self):
        return self.size

    def components(self):
        return self.numComponents

    def unify(self, p, q):
        # we first define what is the root
        # node of each one of the groups
        root1 = self.find(p)
        root2 = self.find(q)

        # if the two root nodes are equal
        # then the two groups are the same
        # so we do not have to do anything
        if root1 == root2:
            return

        # Otherwise we merge the smaller group
        # into the larger group
        if self.sz[root1] < self.sz[root2]:
            self.sz[root2] += self.sz[root1]
            self.id[root1] = root2
            self.sz[root1] = 0
        else:
            self.sz[root1] += self.sz[root2]
            self.id[root2] = root1
            self.sz[root2] = 0

        # we have merged two groups, so the
        # number of components will be 
        # decreased by one
        self.numComponents -= 1
