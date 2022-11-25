import random
from typing import Dict


class BinInt(int):
    LENGTHS: Dict[int, int] = {}

    def __new__(cls, x):
        value = int.__new__(cls, x, 2)
        if type(x) == str:
            cls.LENGTHS[id(value)] = len(x)
        return value

    def __del__(self):
        self.LENGTHS.pop(id(self))

    def __str__(self) -> str:
        value = bin(self)[2:]
        length = self.LENGTHS[id(self)]

        if len(value) != length:
            delta = abs(length - len(value))
            value = ('0' * delta) + value
        return value

    def __add__(self, other) -> "BinInt":
        new = super(BinInt, self).__add__(other)
        new = BinInt(new)
        self.copied(self, new)
        return new

    def __sub__(self, other) -> "BinInt":
        val = super(BinInt, self).__sub__(other)
        return

    def __mul__(self, other) -> "BinInt":
        val = super(BinInt, self).__mul__(other)
        return

    def __divmod__(self, other) -> "BinInt":
        val = super(BinInt, self).__divmod__(other)
        return

    def __xor__(self, other) -> "BinInt":
        val = super(BinInt, self).__xor__(other)
        return

    def __rshift__(self, other) -> "BinInt":
        val = super(BinInt, self).__rshift__(other)
        return

    def __lshift__(self, other) -> "BinInt":
        return super(BinInt, self).__lshift__(other)

    def get_length(self) -> int:
        return self.LENGTHS[id(self)]

    @classmethod
    def copied(cls, old: "BinInt", new: "BinInt"):
        cls.LENGTHS[id(new)] = cls.LENGTHS[id(old)]

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
