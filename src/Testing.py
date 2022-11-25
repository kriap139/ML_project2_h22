import unittest
from src.BinInt import BinInt
from src.main import fitness, mutate


class MyTestCase(unittest.TestCase):

    def test_BinInt_Str(self):
        for length in (4, 9, 50, 100):
            bInt = BinInt.create_random(length)
            bitStr = str(bInt)

            self.assertEqual(len(bitStr), length)

            bInt = BinInt((length - 1) * '0' + "1")
            bitStr = str(bInt)
            self.assertEqual(len(bitStr), length)

            bInt = BinInt((length - 1) * '1' + "0")
            bitStr = str(bInt)
            self.assertEqual(len(bitStr), length)

    def test_bit_flip(self):
        n = BinInt("010110")
        bit = (n >> 2) & 1
        res = n ^ (bit << 2)
        self.assertEqual(str(res), "010010")

    def test_mutation(self):
        bs = BinInt("1111")
        mutated = mutate(bs, rate=1.0)
        self.assertEqual(str(mutated), "0000")

    def test_BitInt_Ops(self):
        b = BinInt("0110")
        shifted = b >> 1

    def test_BinInt_Bit_Value(self):
        num = BinInt("01101")
        bits = list(str(num))
        bits.reverse()

        for i, s in enumerate(bits):
            bit = (num >> i) & 1
            self.assertEqual(bit, int(s))

    def test_BinInt_Bit_Value_long(self):
        num = BinInt.create_random(100)
        bits = list(str(num))
        bits.reverse()

        for i, s in enumerate(bits):
            bit = (num >> i) & 1
            self.assertEqual(bit, int(s))

    def test_Fitness(self):
        nums = [BinInt("1011"), BinInt('1' * 100), BinInt('0' * 100)]

        for i, Fitness in enumerate([3, 100, 0]):
            self.assertEqual(fitness(nums[i]), Fitness)


if __name__ == '__main__':
    unittest.main()
