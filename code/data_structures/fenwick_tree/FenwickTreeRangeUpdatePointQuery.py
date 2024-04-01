

class FenwickTreeRangeUpdatePointQuery:
    def __init__(self, values):
        if values is None:
            raise ValueError("Values array cannot be None!")
        
        # From the wanted values, we will get the
        # number of values N. And we will insert a 
        # 0 value in order to construc the P array
        self.N = len(values)
        values.insert(0, 0)
        
        # Make a clone of the values array
        fenwick_tree = values[:]
        
        # Get the value at each position of the
        # Fenwick Tree looking at its parent's value
        for i in range(1, self.N):
            parent = i + self.lsb(i)
            if parent < self.N:
                fenwick_tree[parent] += fenwick_tree[i]
        
        self.original_tree = fenwick_tree
        self.current_tree = fenwick_tree[:]
    
    def update_range(self, left, right, val):
        self.add(left, val)
        self.add(right + 1, -val)
    
    def add(self, i, v):
        while i < self.N:
            self.current_tree[i] += v
            i += self.lsb(i)
    
    def get(self, i):
        return self.prefix_sum(i, self.current_tree) - self.prefix_sum(i - 1, self.original_tree)
    
    def prefix_sum(self, i, tree):
        sum_val = 0
        while i != 0:
            sum_val += tree[i]
            i &= ~self.lsb(i)
        return sum_val
    
    @staticmethod
    def lsb(i):
        return i & -i
