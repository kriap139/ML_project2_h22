from typing import Dict
import matplotlib.pyplot as plt
from matplotlib import markers


def fitness_plot(data: Dict[int, dict], bits: int, makeXStep1=False, show=False, savePath=None):

    gens = tuple(data.values())
    generations = len(tuple(data.keys()))
    generations = tuple(range(generations))

    bestFitness = tuple(gen['bestFitness'] for gen in gens)
    meanFitness = tuple(gen["meanFitness"] for gen in gens)
    sds = tuple(gen["std"] for gen in gens)

    plt.figure(figsize=(20, 5))
    plt.subplot()
    plt.title("Fitness plot")
    plt.xlabel("Generations")
    plt.ylabel("Fitness")

    plt.plot(bestFitness, marker="o", markersize=7, markerfacecolor="mediumseagreen", color="mediumseagreen", label="Best")

    plt.errorbar(generations, meanFitness, yerr=sds, marker=markers.CARETUPBASE, markersize=7,
                 markerfacecolor="dodgerblue", linestyle="dashed",  color="dodgerblue", label="Average",
                 ecolor="firebrick", elinewidth=1.3, barsabove=True,  capsize=3)

    if makeXStep1:
        plt.xticks(generations)
    else:
        plt.xlim(1, len(generations))

    plt.ylim(0, bits)
    plt.legend()

    if savePath is not None:
        plt.savefig(f'{savePath}.png', bbox_inches='tight')

    if show:
        plt.show()


def print_bin_strs(data: Dict[int, dict], bits: int):
    gens = tuple(data.values())
    fitness = [gen['best'].bit_count() for gen in gens]

    digits = len(str(len(gens))) + 1
    df = len(str(max(fitness)))

    bestStrings = [
        f"Best gen {i}(fitness={fitness[i]}):{(digits - len(str(i))) * ' ' + df * ' '}{str(gen['best'])}" for i, gen in enumerate(gens)
    ]

    text = "\n".join(bestStrings)
    print(text)
