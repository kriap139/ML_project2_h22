import src.util.drawing as draw
from typing import List, Tuple, Union, Dict
from src.BinInt import BinInt
from src.Selector import Selector, argmax
import src.util.io as uio
import math
import random
import os


def stats(fitnessNums: list) -> Tuple[float, tuple, float]:
    n = len(fitnessNums)
    mean = sum(fitnessNums) / n
    errors = tuple(abs(x - mean) ** 2 for x in fitnessNums)
    variance = float(sum(errors) / n)
    return mean, errors, math.sqrt(variance)


def selectCriteria(generation: int, gens: dict, nums: List[BinInt], criteria: Dict[str, Union[bool, int]]) -> Tuple[
    int, List[BinInt]]:
    population = len(nums)
    fitnessNums = [num.bit_count() for num in nums]
    fittest = nums[argmax(fitnessNums)]
    selector = Selector(nums, fitnessNums, isSorted=False)

    startIdx = 0
    delta = population
    unique = criteria["ENSURE_UNIQUE"]
    newNums = []
    k = criteria["k"]

    if generation == 0:
        mean, errors, std = stats(fitnessNums)
        print(f"Mean={mean}, std={std}")

    if criteria["KEEP_FITTEST"]:
        if criteria["MUTATE_FITTEST"]:
            startIdx = 1

        newNums.append(fittest)
        delta -= 1

        if criteria["MAKE_FITTEST_A_FRACTION_OF_POPULATION"]:
            children = round(population * criteria["FITTEST_FRACTION"])
            delta -= children
            for i in range(children):
                newNums.append(fittest)

            if k > delta:
                k = delta

    selected = selector.select(k, unique=unique)

    if type(selected) == BinInt:
        delta -= 1
        newNums.append(selected)
        for i in range(delta):
            newNums.append(selected)
    else:
        delta -= len(selected)
        newNums.extend(selected)

        if criteria["MUTATE_FITTEST"] and not criteria["KEEP_FITTEST"]:
            ft = [num.bit_count() for num in selected]
            selectedFittest = selected[argmax(ft)]
            for i in range(delta):
                newNums.append(selectedFittest)
        else:
            for i in range(delta):
                newNums.append(random.choice(selected))

    mean, errors, std = stats(fitnessNums)
    gens[generation] = {"best": fittest, "bestFitness": max(fitnessNums), "meanFitness": mean, "std": std}

    return startIdx, newNums