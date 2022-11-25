import src.drawing as draw
import random
from typing import List
from enum import Enum
from src.BinInt import BinInt


def fitness(num: BinInt) -> int:
    result = 0
    for i in range(num.get_length()):
        result += (num >> i) & 1
    return result


def mutate(num: BinInt, rate: float):
    length = num.get_length()
    for i in range(length):
        r = random.random()
        if r < rate:
            bit = (num >> i) & 1
            num ^= bit << i


class Criteria(Enum):
    pass



def selection(nums: List[BinInt], criteria: Criteria):
    pass


def main(bits=100, population=16, mutationRate= 0.6, generations=9, criteria: Criteria = None):
    pass


if __name__ == "__main__":
    main()