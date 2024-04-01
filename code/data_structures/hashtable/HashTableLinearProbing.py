
from HashTableOpenAddressingBase import HashTableOpenAddressingBase

class HashTableLinearProbing(HashTableOpenAddressingBase):
    LINEAR_CONSTANT = 17

    def __init__(self, capacity=7, load_factor=0.65):
        super().__init__(capacity, load_factor)

    def setup_probing(self, key):
        pass

    def probe(self, x):
        return self.LINEAR_CONSTANT * x

    def adjust_capacity(self):
        while self.gcd(self.LINEAR_CONSTANT, self.capacity) != 1:
            self.capacity += 1

    @staticmethod
    def gcd(a, b):
        while b != 0:
            a, b = b, a % b
        return a