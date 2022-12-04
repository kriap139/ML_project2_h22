from typing import Dict
import matplotlib.pyplot as plt
from matplotlib import markers


def fitness_plot(data: Dict[int, dict], bits: int, iterations: int, makeXStep1=False, makeYStep1=True,  show=False, savePath=None,
                 printInfo=True):

    gens = tuple(data.values())
    generations = len(tuple(data.keys()))
    generations = tuple(range(generations))

    best = [gen['best'].bit_count() for gen in gens]
    bestFitness = tuple(gen['bestFitness'] for gen in gens)
    meanFitness = tuple(gen["meanFitness"] for gen in gens)
    sds = tuple(gen["std"] for gen in gens)

    if printInfo:
        print(f"Last gen Best: {best[-1]}\nLast gen bestFitness (Avg): {bestFitness[-1]}\nLast gen meanFitness (Avg): {meanFitness[-1]}\nLast gen SDS (Avg): {sds[-1]}")
        print(f"\nBest: {max(best)}\nbestFitness (Avg): {max(bestFitness)}\nmeanFitness (Avg): {max(meanFitness)}\nSDS (Avg): {max(sds)}")

    plt.figure(figsize=(20, 5))
    plt.subplot()
    plt.title(f"Fitness plot (Avg over {iterations} iterations)")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")

    if iterations > 1:
        plt.plot(best, marker="o", markersize=6, markerfacecolor="goldenrod", color="goldenrod", label="Best")

    plt.plot(bestFitness, marker="o", markersize=7, markerfacecolor="mediumseagreen", color="mediumseagreen", label="Avg Best")

    plt.errorbar(generations, meanFitness, yerr=sds, marker=markers.CARETUPBASE, markersize=7,
                 markerfacecolor="dodgerblue", linestyle="dashed",  color="dodgerblue", label="Avg fitness",
                 ecolor="firebrick", elinewidth=1.3, barsabove=True,  capsize=3)

    if makeXStep1:
        plt.xticks(generations)
    else:
        plt.xlim(1, len(generations))

    if makeYStep1:
        plt.yticks(range(0, bits + 1, 10))
    else:
        plt.ylim(0, bits)

    plt.legend()

    if savePath is not None:
        plt.savefig(f'{savePath}.png', bbox_inches='tight')

    if show:
        plt.show()


def print_bin_strs(data: Dict[int, dict], iterations: int):
    gens = tuple(data.values())
    fitness = [gen['best'].bit_count() for gen in gens]

    digits = len(str(len(gens))) + 1
    df = len(str(max(fitness)))

    bestStrings = [
        f"Best gen {i}(fitness={fitness[i]}):{(digits - len(str(i))) * ' ' + df * ' '}{str(gen['best'])}" for i, gen in enumerate(gens)
    ]

    text = "\n".join(bestStrings)
    print(text, end='\n\n')

    if iterations > 1:
        print("Gen0Stats: ")
        for i, d in enumerate(gens[0]["gen0Stats"]):
            print(f"\tIteration {i}: {d}")
        print()
