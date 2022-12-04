import random


def argmax(elements: list) -> int:
    """Returns index of largets element"""
    indexes = range(len(elements))
    i = max(indexes, key=elements.__getitem__)
    return int(i)


class Selector:
    def __init__(self, population: list,  weights: list, unique=False):

        if len(population) != len(weights):
            raise ValueError(f"Population ({len(population)}) and weights ({len(weights)}) are not of same length!")

        self.population = population
        self.weights = weights
        self.unique = unique
        self.total = 0
        self.cumulative = []

        if unique:
            self._population = population[:]
            self._weights = weights[:]
        else:
            self._population = population
            self._weights = weights

        self.__calc_cumulative_weights()

    def __calc_cumulative_weights(self):
        self.total = float(0)
        self.cumulative.clear()
        for weight in self._weights:
            self.total += weight
            self.cumulative.append(self.total)

    def select(self, k: int = 1):
        """Randomly select k element in the population, with a weighted probability using binary search.
            If the unique flag is set, then the selected elements needs to have unique indexes.
            :returns element ot [elements, ...k]
        """
        if self.unique:
            if k > len(self.population):
                raise ValueError("k bigger than population size")
            elif k > len(self._population):
                self._population = self.population[:]
                self._weights = self.weights[:]

            selected, weights = [], []

            for _ in range(k):
                i = self.__select()
                selected.append(self._population.pop(i))
                weights.append(self._weights.pop(i))
                self.__calc_cumulative_weights()

            return selected, weights
        else:
            selected, weights = [], []
            for _ in range(k):
                i = self.__select()
                selected.append(self._population[i])
                weights.append(self._weights[i])
            return selected, weights

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

    @classmethod
    def sort(cls, population: list, weights: list):
        joined = list(zip(population, weights))
        joined.sort(key=lambda tup: tup[1])
        population, weights = zip(*joined)
        return list(population), list(weights)
