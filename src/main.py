import src.util.drawing as draw
from typing import List, Tuple, Union, Dict
from src.BinInt import BinInt
from src.Selector import Selector, argmax
import math
import random


def mean_gens(acc: List[Dict[int, dict]]) -> Dict[int, dict]:
    generations = len(acc[0].keys())
    gens = {gen: dict(best=None, bestFitness=0, meanFitness=0, std=0) for gen in range(generations)}

    currBestFitness = {gen: 0 for gen in range(generations)}

    for it in acc:
        for gen, data in it.items():
            gens[gen]["meanFitness"] += data["meanFitness"]
            gens[gen]["std"] += data["std"]

            bestFitness = data["bestFitness"]

            if bestFitness > currBestFitness[gen]:
                gens[gen]["best"] = data["best"]
                currBestFitness[gen] = bestFitness

            gens[gen]["bestFitness"] += bestFitness

    it = float(len(acc))

    for gen, data in gens.items():
        data["meanFitness"] /= it
        data["bestFitness"] /= it
        data["std"] /= it

    return gens


def stats(fitnessNums: list) -> Tuple[float, tuple, float]:
    n = len(fitnessNums)
    mean = sum(fitnessNums) / n
    errors = tuple(abs(x - mean) ** 2 for x in fitnessNums)
    variance = float(sum(errors) / n)
    return mean, errors, math.sqrt(variance)


def record(generation: int, gens: dict, fitnessNums: List[int], fittest: BinInt):
    mean, errors, std = stats(fitnessNums)
    gens[generation] = {"best": fittest.copy(), "bestFitness": max(fitnessNums), "meanFitness": mean, "std": std}


def selectCriteria(generation: int, gens: dict, nums: List[BinInt], criteria: Dict[str, Union[bool, int]]) -> Tuple[
    int, List[BinInt]]:
    population = len(nums)
    fitnessNums = [num.count() for num in nums]
    fittest = nums[argmax(fitnessNums)]
    selector = Selector(nums, fitnessNums, isSorted=False)

    startIdx = 0
    delta = population
    unique = criteria["ENSURE_UNIQUE"]
    newNums = []

    if criteria["KEEP_FITTEST"]:
        if criteria["MUTATE_FITTEST"]:
            startIdx = 1

        newNums.append(fittest)

        if criteria["MAKE_FITTEST_A_FRACTION_OF_POPULATION"]:
            children = round(population * criteria["FITTEST_FRACTION"])
            delta -= children
            for i in range(children):
                newNums.append(fittest)

    selected = selector.select(criteria["k"], unique=unique)

    if type(selected) == BinInt:
        delta -= 1
        newNums.append(selected)

        for i in range(delta):
            newNums.append(selected)
    else:
        delta -= len(selected)
        newNums.extend(selected)
        for i in range(delta):
            newNums.append(random.choice(selected))

    record(generation, gens, fitnessNums, fittest)
    return startIdx, newNums


def main(bits=100, population=60, mutationRate=0.016, generations=60, iterations=1):
    criteria = {
        "KEEP_FITTEST": True,
        "MUTATE_FITTEST": True,
        "MAKE_FITTEST_A_FRACTION_OF_POPULATION": True,
        "ENSURE_UNIQUE": False,
        "FITTEST_FRACTION": 0.1,
        "k": 6
    }

    acc = []

    for _ in range(iterations):

        gens = {}
        nums = [BinInt.create_random(bits) for _ in range(population)]
        startIdx, nums = selectCriteria(0, gens, nums, criteria)

        for gen in range(1, generations + 1):
            for i in range(startIdx, len(nums)):
                nums[i] = BinInt.mutate(nums[i], mutationRate)

            startIdx, nums = selectCriteria(gen, gens, nums, criteria)

        acc.append(gens)

    gens = mean_gens(acc) if (iterations > 1) else acc[0]

    draw.print_bin_strs(gens, bits)
    draw.fitness_plot(gens, bits, makeXStep1=False, show=True)


if __name__ == "__main__":
    # random.seed(9)
    main()
