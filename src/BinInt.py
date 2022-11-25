import random
from typing import Dict, Union


class BinInt(int):
    LENGTHS: Dict[int, int] = {}

    def __new__(cls, x):
        value = int.__new__(cls, x, base=2)
        cls.LENGTHS[id(value)] = len(x)
        return value

    def __del__(self):
        self.LENGTHS.pop(id(self))

    def __str__(self) -> str:
        return self.__to_bin_str(self, self.get_length())

    def __repr__(self):
        return f"BinInt({self.__str__()})"

    def __add__(self, other) -> "BinInt":
        new = super(BinInt, self).__add__(other)
        return self.copied(self, new)

    def __sub__(self, other) -> "BinInt":
        new = super(BinInt, self).__sub__(other)
        return self.copied(self, new)

    def __mul__(self, other) -> "BinInt":
        new = super(BinInt, self).__mul__(other)
        return self.copied(self, new)

    def __xor__(self, other) -> "BinInt":
        new = super(BinInt, self).__xor__(other)
        return self.copied(self, new)

    def __rshift__(self, other) -> "BinInt":
        new = super(BinInt, self).__rshift__(other)
        return self.copied(self, new)

    def __lshift__(self, other) -> "BinInt":
        new = super(BinInt, self).__lshift__(other)
        return self.copied(self, new)

    def get_length(self) -> int:
        return self.LENGTHS[id(self)]

    @classmethod
    def __to_bin_str(cls, binary: Union["BinInt", int], length: int) -> str:
        binary = bin(binary)[2:]
        if len(binary) != length:
            delta = abs(length - len(binary))
            binary = ('0' * delta) + binary
        return binary

    @classmethod
    def copied(cls, old: "BinInt", new: Union["BinInt", int]) -> "BinInt":
        if type(new) != BinInt:
            s = cls.__to_bin_str(new, old.get_length())
            new = BinInt(s)

        cls.LENGTHS[id(new)] = cls.LENGTHS[id(old)]
        return new

    @classmethod
    def create_random(cls, length: int) -> "BinInt":
        s = cls.random_bit_str(length)
        return cls(s)

    @classmethod
    def random_bit_str(cls, length: int) -> str:
        return "".join([random.choice(seq=('0', '1')) for _ in range(length)])

    @classmethod
    def bit_str_pattern(cls, pattern: str, length: int) -> str:
        result = ""
        while len(result) < length:
            result = result + pattern
        return result if (len(result) <= length) else result[:length]
