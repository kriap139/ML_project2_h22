import random
from typing import Union, Iterable, Tuple, List


class BinInt(int):
    def __new__(cls, x):
        instance = int.__new__(cls, x, base=2)
        instance.__length = len(x)
        return instance

    def __str__(self) -> str:
        return self.__to_bin_str(self, self.length())

    def __repr__(self):
        return f"BinInt({self.__str__()})"

    def __add__(self, other) -> "BinInt":
        new = super(BinInt, self).__add__(other)
        return self._mutated(self, new)

    def __sub__(self, other) -> "BinInt":
        new = super(BinInt, self).__sub__(other)
        return self._mutated(self, new)

    def __mul__(self, other) -> "BinInt":
        new = super(BinInt, self).__mul__(other)
        return self._mutated(self, new)

    def __xor__(self, other) -> "BinInt":
        new = super(BinInt, self).__xor__(other)
        return self._mutated(self, new)

    def __rshift__(self, other) -> "BinInt":
        new = super(BinInt, self).__rshift__(other)
        return self._mutated(self, new)

    def __lshift__(self, other) -> "BinInt":
        new = super(BinInt, self).__lshift__(other)
        return self._mutated(self, new)

    def bit_state(self, k: int) -> int:
        """Get the state (0 or 1) of the kth bit from the right (LSB)"""
        return (self >> k) & 1

    def flip_bit(self, k: int) -> "BinInt":
        """Flip the kth bit from the right (LSB)"""
        return self ^ (1 << k)

    def count(self) -> int:
        """Return number of ones in the bit string"""
        result = 0
        for i in range(self.length()):
            result += self.bit_state(i)
        return result

    def length(self) -> int:
        """Return the number of bits in the bit string"""
        return self.__length

    def copy(self) -> "BinInt":
        s = self.__to_bin_str(self, self.length())
        return BinInt(s)

    @staticmethod
    def mutate(num: "BinInt", flipRate: float) -> "BinInt":
        """Mutates a bit string by randomly flipping bits.
        The probability that a bit is flipped is given by flipRate"""
        length = num.length()
        for i in range(length):
            if random.random() < flipRate:
                num = num.flip_bit(i)
        return num

    @classmethod
    def __to_bin_str(cls, binary: Union["BinInt", int], length: int) -> str:
        binary = bin(binary)[2:]
        if len(binary) != length:
            delta = abs(length - len(binary))
            binary = ('0' * delta) + binary
        return binary

    @classmethod
    def _mutated(cls, old: "BinInt", new: Union["BinInt", int]) -> "BinInt":
        if type(new) != BinInt:
            s = cls.__to_bin_str(new, old.length())
            new = BinInt(s)
        return new

    @classmethod
    def create_random(cls, length: int) -> "BinInt":
        s = cls.random_bit_str(length)
        return cls(s)

    @classmethod
    def random_bit_str(cls, length: int) -> str:
        return "".join([random.choice(seq=('0', '1')) for _ in range(length)])