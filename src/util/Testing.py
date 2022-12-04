import unittest
from src.BinInt import BinInt
from src.Selector import Selector
import random
import time


class MyTestCase(unittest.TestCase):

    def test_BinInt_Str(self):
        for length in (4, 9, 50, 100):
            bInt = BinInt.create_random(length)
            bitStr = str(bInt)

            self.assertEqual(len(bitStr), length)
            self.assertEqual(bInt.length(), length)

            bInt = BinInt((length - 1) * '0' + "1")
            bitStr = str(bInt)
            self.assertEqual(len(bitStr), length)

            bInt = BinInt((length - 1) * '1' + "0")
            bitStr = str(bInt)
            self.assertEqual(len(bitStr), length)

    def test_bit_flip(self):
        n = BinInt("010110")
        self.assertEqual(str(n.flip_bit(0)), "010111")
        self.assertEqual(str(n.flip_bit(1)), "010100")
        self.assertEqual(str(n.flip_bit(2)), "010010")
        self.assertEqual(str(n.flip_bit(3)), "011110")
        self.assertEqual(str(n.flip_bit(4)), "000110")
        self.assertEqual(str(n.flip_bit(5)), "110110")
        self.assertEqual(str(n.flip_bit(6)), "01010110")

        n = n.flip_bit(0)
        self.assertEqual(str(n), "010111")
        n = n.flip_bit(3)
        self.assertEqual(str(n), "011111")
        n = n.flip_bit(5)
        self.assertEqual(str(n), "111111")

    def test_mutation(self):
        bs = BinInt("1111")
        mutated = BinInt.mutate(bs, flipRate=1.0)
        self.assertEqual(str(mutated), "0000")

    def test_Random_probability(self):
        n = 1000000
        probability = 0.5
        positives = 0
        for i in range(n):
            if random.random() < probability:
                positives += 1

        p = positives / n
        self.assertAlmostEqual(p, probability, places=2)

    def test_BinInt_Bit_State(self):
        num = BinInt("01101")
        bits = list(str(num))
        bits.reverse()

        for i, s in enumerate(bits):
            self.assertEqual(num.bit_state(i), int(s))

        self.assertEqual(num.bit_state(num.length() + 10), 0)

    def test_BinInt_Bit_State_long(self):
        num = BinInt.create_random(100)
        bits = list(str(num))
        bits.reverse()

        for i, s in enumerate(bits):
            self.assertEqual(num.bit_state(i), int(s))

    def test_Fitness(self):
        nums = [BinInt("1011"), BinInt('1' * 100), BinInt('0' * 100)]

        for i, fitness in enumerate([3, 100, 0]):
            self.assertEqual(nums[i].count(), fitness)

    def test_Selector(self):
        if True:
            nums = [5, 1, 3, 9, 6, 8, 4, 7, 2, 10]
            weights = [10, 13, 40, 90, 60, 70, 4, 40, 20, 50]
            nums, weights = Selector.sort(nums, weights)

            selector = Selector(nums, weights)

            self.assertListEqual(selector.population, [4, 5, 1, 2, 3, 7, 10, 6, 8, 9])
            self.assertListEqual(selector.weights, [4, 10, 13, 20, 40, 40, 50, 60, 70, 90])

            total = sum(weights)
            probabilities = [weight / float(total) for weight in weights]
            self.assertEqual(sum(probabilities), 1.0)

            nums = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
            weights = [4, 10, 13, 20, 40, 40, 50, 60, 70, 90]

            n = 10000000
            selector = Selector(nums, weights, unique=True)
            result = [0 for _ in range(len(nums))]

            for _ in range(n):
                i = selector.select()
                result[i] += 1

            total = sum(weights)
            probabilities = [weight / float(total) for weight in weights]
            probs = [positives / float(n) for positives in result]

            for i in range(len(weights)):
                print(f"Probability: {round(probabilities[i], 4)} Calculated: {round(probs[i], 4)}")

    def tests_bit_count_vs_native(self):
        n = 100
        num = BinInt.create_random(n)

        start = time.time()
        c = num.count()
        end1 = time.time() - start

        start = time.time()
        bc = num.bit_count()
        end2 = time.time() - start

        self.assertEqual(c, bc)

        # print(f"count(): {end1} sec, bit_count(): {end2}")

        # 100: count(): 0.00016045570373535156 sec, bit_count(): 4.0531158447265625e-06
        # 10000: count(): 0.14647674560546875 sec, bit_count(): 3.5762786865234375e-06
        # 100000: count(): 13.200358390808105 sec, bit_count(): 1.049041748046875e-05


if __name__ == '__main__':
    unittest.main()
