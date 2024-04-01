

class FenwickTreeRangeQueryPointUpdate:
    def __init__(self, sz_or_values):
        if isinstance(sz_or_values, int):
            self.N = sz_or_values + 1
            self.tree = [0] * self.N
        elif isinstance(sz_or_values, list):
            if sz_or_values is None:
                raise ValueError("Values array cannot be None!")
            
            self.N = len(sz_or_values)
            sz_or_values[0] = 0
            
            self.tree = sz_or_values[:]
            
            for i in range(1, self.N):
                parent = i + self.lsb(i)
                if parent < self.N:
                    self.tree[parent] += self.tree[i]
        else:
            raise ValueError("Invalid argument type for constructor")
    
    def lsb(self, i):
        return i & -i
    
    def prefix_sum(self, i):
        sum_val = 0
        while i != 0:
            sum_val += self.tree[i]
            i &= ~self.lsb(i)
        return sum_val
    
    def sum(self, left, right):
        if right < left:
            raise ValueError("Make sure right >= left")
        return self.prefix_sum(right) - self.prefix_sum(left - 1)
    
    def get(self, i):
        return self.sum(i, i)
    
    def add(self, i, v):
        while i < self.N:
            self.tree[i] += v
            i += self.lsb(i)
    
    def set(self, i, v):
        self.add(i, v - self.sum(i, i))
    
    def __str__(self):
        return str(self.tree)
