import random


def argmax(elements: list) -> int:
    """Returns index of largets element"""
    indexes = range(len(elements))
    i = max(indexes, key=elements.__getitem__)
    return int(i)


class Selector:
    def __init__(self, population: list,  weights: list, isSorted: bool = True):

        if len(population) != len(weights):
            raise ValueError(f"Population ({len(population)}) and weights ({len(weights)}) are not of same length!")

        self.population = population
        self.weights = weights
        self.total = 0
        self.cumulative = []

        if not isSorted:
            self.__sort()
        self.__calc_cumulative_weights()

    def __calc_cumulative_weights(self):
        self.total = float(0)
        self.cumulative.clear()
        for weight in self.weights:
            self.total += weight
            self.cumulative.append(self.total)

    def __sort(self):
        joined = list(zip(self.population, self.weights))
        joined.sort(key=lambda tup: tup[1])
        self.population, self.weights = zip(*joined)

        self.population = list(self.population)
        self.weights = list(self.weights)

    def select(self, k: int = 1, unique=False):
        """Randomly select k element in the population, with a weighted probability using binary search.
            If the unique flag is set, then the selected elements needs to have unique indexes.
            :returns element ot [elements, ...k]
        """
        if k == 1:
            return self.population[self.__select()]
        elif k > len(self.population) and unique:
            raise ValueError("k bigger than population size")
        elif not unique:
            return [self.population[self.__select()] for _ in range(k)]
        else:
            selected = []

            for _ in range(k):
                i = self.__select()
                selected.append(self.population.pop(i))
                self.weights.pop(i)
                self.__calc_cumulative_weights()

        return selected

    def __select(self) -> int:
        x = random.uniform(0, self.total)
        left = 0
        right = len(self.cumulative)

        while left < right:
            mid = (left + right) // 2
            if self.cumulative[mid] < x:
                left = mid + 1
            else:
                right = mid

        return left
