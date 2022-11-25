import src.drawing as draw
import random
from typing import List
from enum import Enum
from src.BinInt import BinInt
from math import exp
import bisect


def fitness(num: BinInt) -> int:
    result = 0
    for i in range(num.get_length()):
        result += (num >> i) & 1
    return result


def mutate(num: BinInt, rate: float) -> BinInt:
    length = num.get_length()
    for i in range(length):
        r = random.random()
        if r < rate:
            bit = (num >> i) & 1
            num ^= bit << i
    return num


def probability_distribution(nums_fitness: List[int]) -> List[float]:
    exps = [exp(x) for x in nums_fitness]
    summed = sum(exps)
    return [e / summed for e in exps]


class Criteria(Enum):
    KEEP_FITTEST_AND_MUTATE_SELECTED = 0,
    SELECT_TWO_AND_MUTATE = 1,
    KEEP_FITTEST_AND_MUTATE_TWO_SELECTED = 2


def select(nums: List[BinInt], nums_fitness: List[int],
           fittesIdx: int, criteria: Criteria) -> List[BinInt]:

    selected = []
    dist = probability_distribution(nums_fitness)

    total = 0
    cumulative = []
    for weight in dist:
        total += weight
        cumulative.append(total)

    if criteria == Criteria.KEEP_FITTEST_AND_MUTATE_SELECTED:
        selected.append(nums[fittesIdx])

        x = random.random() * total
        i = bisect.bisect(cumulative, x)
        selected.append(nums[i])

    return selected


def main(bits=100,
         population=16,
         mutationRate= 0.6,
         generations=9,
         criteria: Criteria = Criteria.KEEP_FITTEST_AND_MUTATE_SELECTED):

    gens = {}
    fittest = [0 for _ in range(population)]
    nums = [BinInt.create_random(bits) for _ in range(population)]
    nums_fitness = [0 for _ in range(population)]

    for gen in range(generations):
        for i in range(len(nums)):
            nums[i] = mutate(nums[i], mutationRate)
            nums_fitness[i] = fitness(nums[i])

        fittest[gen] = max(range(population), key=nums_fitness.__getitem__)

        gens[gen] = {
            "nums": nums,
            "numsFitness": nums_fitness,
            "fittestIdx": fittest[gen]
        }

        nums = select(nums, nums_fitness, fittest[gen], criteria)

        if len(nums) < population:
            start = len(nums)
            delta = population - start
            selected = nums[1]

            if criteria == criteria.KEEP_FITTEST_AND_MUTATE_SELECTED:
                for _ in range(delta):
                    nums.append()





if __name__ == "__main__":
    main()
