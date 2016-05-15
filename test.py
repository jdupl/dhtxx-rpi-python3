import unittest
from dht11 import DHT11


class DHT11Test(unittest.TestCase):
    def setUp(self):
        from fixtures import test_data
        self.raw_bits = test_data.raw_bits
        self.dht11 = DHT11()

    def test_get_length(self):
        length = self.dht11._get_length_of_sequential_bits(self.raw_bits, 0)
        self.assertEquals(length, 6)

    def test_get_data_impulses(self):
        lengths = [3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8,
                   9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3]
        self.assertEquals(self.dht11._get_data_impulses(self.raw_bits), lengths)

    def test_get_bits_from_impulses(self):
        lengths = [3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8,
                   9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3]

        actual_bits = self.dht11._get_bits_from_impulses(lengths)
        expected_bits = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0]
        self.assertEquals(expected_bits, actual_bits)

    def test_get_bytes_from_bits(self):
        bits = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
        0, 0, 0, 0, 0, 0]

        expected = [40, 0, 24, 0, 64]

        actual = self.dht11._get_bytes_from_bits(bits)
        self.assertEquals(expected, actual)
