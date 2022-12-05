import src.util.drawing as draw
from typing import List, Tuple, Union, Dict
from src.BinInt import BinInt
from src.Selector import Selector, argmax
import src.util.io as uio
import math
import random
import os
from dataclasses import dataclass
import dataclasses
import numpy as np

PLOTS_DIR = "results/plots/"
DATA_FILE_PATH = "results/results.json"


def mean_gens(acc: List[Dict[int, dict]]) -> Dict[int, dict]:
    generations = len(acc[0].keys())
    gens = {gen: dict(best=None, bestFitness=0, meanFitness=0, std=0) for gen in range(generations)}

    currBestFitness = {gen: 0 for gen in range(generations)}

    gen0Stats = []

    for it in acc:
        gen0Stats.append(
            dict(meanFitness=it[0]["meanFitness"], std=it[0]["std"], bestFitness=it[0]["bestFitness"], best=it[0]["best"])
        )

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

    gens[0]["gen0Stats"] = gen0Stats
    return gens


def stats(fitnessNums: list) -> Tuple[float, tuple, float]:
    n = len(fitnessNums)
    mean = sum(fitnessNums) / n
    errors = tuple(abs(x - mean) ** 2 for x in fitnessNums)
    variance = float(sum(errors) / n)
    return mean, errors, math.sqrt(variance)


def record(generation: int, gens: dict, nums: List[BinInt]) -> Tuple[List[int], BinInt]:
    fitnessNums = [num.bit_count() for num in nums]
    fittest = nums[argmax(fitnessNums)]
    mean, errors, std = stats(fitnessNums)

    gens[generation] = {"best": fittest, "bestFitness": max(fitnessNums), "meanFitness": mean, "std": std}
    return fitnessNums, fittest


@dataclass()
class SelectionData:
    k: int
    population: int
    unique: bool = False
    ff: float = 0.5


def selection1(nums: List[BinInt], fittest: BinInt, fitnessNums: List[int], data: SelectionData) -> List[BinInt]:
    delta = data.population - 1
    newNums = [fittest]

    children = round(data.population * data.ff)
    delta -= children

    for i in range(children):
        newNums.append(fittest)

    nums, fitnessNums = Selector.sort(nums, fitnessNums)
    selector = Selector(nums, fitnessNums, unique=data.unique)
    selected, weights = selector.select(delta)

    newNums.extend(selected)
    return newNums


def selection2(nums: List[BinInt], fittest: BinInt, fitnessNums: List[int], data: SelectionData) -> List[BinInt]:
    newNums = []
    joined = tuple(zip(nums, fitnessNums))

    for i in range(data.population):
        selected = tuple(random.choice(joined) for _ in range(data.k))
        selected = max(selected, key=lambda tup: tup[1])
        newNums.append(selected[0])

    return newNums


def selection3(nums: List[BinInt], fittest: BinInt, fitnessNums: List[int], data: SelectionData) -> List[BinInt]:
    nums, fitnessNums = Selector.sort(nums, fitnessNums)
    selector = Selector(nums, fitnessNums, unique=data.unique)

    newNums = [fittest]
    population = data.population - 1

    for _ in range(population):
        selected, weights = selector.select(data.k)
        newNums.append(selected[argmax(weights)])

    return newNums


def selection4(nums: List[BinInt], fittest: BinInt, fitnessNums: List[int], data: SelectionData) -> List[BinInt]:
    nums, fitnessNums = Selector.sort(nums, fitnessNums)
    selector = Selector(nums, fitnessNums, unique=data.unique)

    newNums = [fittest]
    population = data.population - 1

    it = population // data.k
    remainder = population % data.k

    for i in range(it):
        selected, weights = selector.select(data.k)
        newNums.extend(selected)

    if remainder > 0:
        selected, weights = selector.select(remainder)
        newNums.extend(selected)

    return newNums


# Defaults:
    # bits=100, population=25, mutationRate=0.009, generations=90, iterations=30
    # k=6, unique=False, ff=0.3


def main(bits=100, population=25, mutationRate=0.009, generations=90, iterations=5, save: bool = True):
    data = SelectionData(k=6, population=population, unique=False, ff=0.3)

    selectionFunc = selection3
    acc = []

    for _ in range(iterations):
        gens = {}
        nums = BinInt.create_random_arr(bits, population, 0.3)

        fitnessNums, fittest = record(0, gens, nums)
        nums = selectionFunc(nums, fittest, fitnessNums, data)

        for gen in range(1, generations + 1):
            for i in range(len(nums)):
                nums[i] = BinInt.mutate(nums[i], mutationRate)

            fitnessNums, fittest = record(gen, gens, nums)
            nums = selectionFunc(nums, fittest, fitnessNums, data)

        acc.append(gens)

    gens = mean_gens(acc) if (iterations > 1) else acc[0]
    draw.print_bin_strs(gens, iterations)

    if save:
        uio.init(PLOTS_DIR, DATA_FILE_PATH)
        configData = {
            "bits": bits,
            "population": population,
            "generations": generations,
            "mutationRate": mutationRate,
            "iterations": iterations,
            "method": selectionFunc.__name__,
            "data": dataclasses.asdict(data)
        }
        saveData = dict(config=configData, results=gens)
        saveID = uio.saveData(saveData, DATA_FILE_PATH, indent=3)
        savePath = os.path.join(PLOTS_DIR, str(saveID))
    else:
        savePath = None

    draw.fitness_plot(gens, bits, iterations, makeXStep1=False, show=True, savePath=savePath)


if __name__ == "__main__":
    # random.seed(9)
    main()


