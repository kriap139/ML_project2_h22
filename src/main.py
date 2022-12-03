import src.util.drawing as draw
from typing import List, Tuple, Union, Dict
from src.BinInt import BinInt
from src.Selector import Selector, argmax
import src.util.io as uio
import math
import random
import os
from dataclasses import dataclass

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


def selectCriteria(nums: List[BinInt], fittest: BinInt, fitnessNums: List[int], criteria: Dict[str, Union[bool, int]],
                   data: SelectionData) -> Tuple[int, List[BinInt]]:

    selector = Selector(nums, fitnessNums, isSorted=False)
    startIdx = 0

    delta = data.population
    unique = criteria["ENSURE_UNIQUE"]
    newNums = []
    k = data.k

    if criteria["KEEP_FITTEST"]:
        if criteria["MUTATE_FITTEST"]:
            startIdx = 1

        newNums.append(fittest)
        delta -= 1

        if criteria["MAKE_FITTEST_A_FRACTION_OF_POPULATION"]:
            children = round(data.population * criteria["FITTEST_FRACTION"])
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

    return startIdx, newNums


# bits=100, population=30, mutationRate=0.01, generations=60, k=6

def main(bits=100, population=10, mutationRate=0.01, generations=60, iterations=2, save: bool = False):
    data = SelectionData(8, population)
    criteria = {
        "KEEP_FITTEST": False,
        "MUTATE_FITTEST": True,
        "MAKE_FITTEST_A_FRACTION_OF_POPULATION": False,
        "ENSURE_UNIQUE": True,
        "FITTEST_FRACTION": 0.5,
        "k": 8
    }

    acc = []

    for _ in range(iterations):
        gens = {}
        nums = BinInt.create_random_arr(bits, population, 0.3)

        fitnessNums, fittest = record(0, gens, nums)
        startIdx, nums = selectCriteria(nums, fittest, fitnessNums, criteria, data)

        for gen in range(1, generations + 1):
            for i in range(startIdx, len(nums)):
                nums[i] = BinInt.mutate(nums[i], mutationRate)

            fitnessNums, fittest = record(gen, gens, nums)
            startIdx, nums = selectCriteria(nums, fittest, fitnessNums, criteria, data)
        acc.append(gens)

    gens = mean_gens(acc) if (iterations > 1) else acc[0]
    draw.print_bin_strs(gens, bits)

    if iterations > 1:
        print("Gen0Stats: ")
        for d in gens[0]["gen0Stats"]:
            print(f"\t{d}")
        print()

    if save:
        uio.init(PLOTS_DIR, DATA_FILE_PATH)
        configData = {
            "bits": bits,
            "population": population,
            "generations": generations,
            "mutationRate": mutationRate,
            "iterations": iterations,
            "criteria": criteria
        }
        saveData = dict(config=configData, results=gens)
        saveID = uio.saveData(saveData, DATA_FILE_PATH, indent=3)
        savePath = os.path.join(PLOTS_DIR, str(saveID))
    else:
        savePath = None

    draw.fitness_plot(gens, bits, iterations, makeXStep1=False, show=True, savePath=savePath)


def rand_test():
    nums = BinInt.create_random_arr(100, 30, 0.3)  # 0.3, 0.9
    mean, errors, std = stats([num.bit_count() for num in nums])
    for num in nums:
        print(num)
    print("Mean: ", mean, " std: ", std)


if __name__ == "__main__":
    # random.seed(9)
    main()
    #rand_test()


