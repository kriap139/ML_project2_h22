import src.util.drawing as draw
from typing import List, Tuple, Union, Dict
from src.BinInt import BinInt
from src.Selector import Selector, argmax
import src.util.io as uio
import math
import random
import os

PLOTS_DIR = "results/plots/"
DATA_FILE_PATH = "results/results.json"


def mean_gens(acc: List[Dict[int, dict]], decimals: int = 3) -> Dict[int, dict]:
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

# bits=100, population=30, mutationRate=0.01, generations=60, k=6

def main(bits=100, population=30, mutationRate=0.01, generations=60, iterations=30, save: bool = False):
    criteria = {
        "KEEP_FITTEST": False,
        "MUTATE_FITTEST": True,
        "MAKE_FITTEST_A_FRACTION_OF_POPULATION": False,
        "ENSURE_UNIQUE": True,
        "FITTEST_FRACTION": 0.5,
        "k": 13
    }

    uio.init(PLOTS_DIR, DATA_FILE_PATH)

    # Make sure parameters are set correctly
    if (not criteria["MUTATE_FITTEST"]) and criteria["MUTATE_FITTEST"]:
        print("FITTEST isn't keept, so 'MUTATE_FITTEST' flag will have no effect!")
    elif criteria["MAKE_FITTEST_A_FRACTION_OF_POPULATION"]:
        fraction = criteria["FITTEST_FRACTION"]
        if type(criteria["FITTEST_FRACTION"]) != float:
            raise ValueError(f"FITTEST_FRACTION needs to be of type float, not {type(criteria['FITTEST_FRACTION'])}")
        if (fraction > 1) or (fraction < 0):
            raise ValueError(f"'FITTEST_FRACTION' needs to be a value between 0 and 1, not {fraction}")
    elif (criteria["k"] > population) or (criteria["k"] < 0):
        raise ValueError("k is not: 0 < k <= population")

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

    if save:
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


if __name__ == "__main__":
    # random.seed(9)
    main()
