
from HashTableOpenAddressingBase import HashTableOpenAddressingBase

from abc import ABC, abstractmethod

from typing import TypeVar

K = TypeVar('K', bound='SecondaryHash')
V = TypeVar('V')


class SecondaryHash(ABC):
    @abstractmethod
    def hash_code2(self) -> int:
        pass

class HashTableDoubleHashing(HashTableOpenAddressingBase[K, V]):

    def __init__(self, capacity=7, load_factor=0.65):
        super().__init__(capacity, load_factor)
        self.hash = 0

    def setup_probing(self, key):
        self.hash = self.normalize_index(key.hash_code2())

        if self.hash == 0:
            self.hash = 1

    def probe(self, x):
        return x * self.hash

    def adjust_capacity(self):
        while not self.is_probable_prime(self.capacity):
            self.capacity += 1

    @staticmethod
    def is_probable_prime(n, k=20):
        return pow(2, n - 1, n) == 1 if n >= 3 else n == 2
