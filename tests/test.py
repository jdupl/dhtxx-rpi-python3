import unittest
from unittest.mock import MagicMock

from dhtxx import DHT11, DHT22


class DHTXXTest(unittest.TestCase):
    def setUp(self):
        from fixtures import test_data
        self.raw_bits = test_data.raw_bits_dht11
        self.dhtxx = DHT11(12, MagicMock())

    def test_get_length(self):
        length = self.dhtxx._get_length_of_sequential_bits(self.raw_bits, 0)
        self.assertEqual(length, 6)

    def test_get_data_impulses(self):
        lengths = [3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8,
                   9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3]
        self.assertEqual(self.dhtxx._get_data_impulses(self.raw_bits), lengths)

    def test_get_bits_from_impulses(self):
        lengths = [3, 3, 8, 3, 8, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8,
                   9, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 8, 3, 3, 3, 3, 3, 3]

        actual_bits = self.dhtxx._get_bits_from_impulses(lengths)
        expected_bits = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                         0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                         0, 0, 0, 0, 0, 0]
        self.assertEqual(expected_bits, actual_bits)

    def test_get_bytes_from_bits(self):
        bits = [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1,
                0, 0, 0, 0, 0, 0]

        expected = [40, 0, 24, 0, 64]

        actual = self.dhtxx._get_bytes_from_bits(bits)
        self.assertEqual(expected, actual)


class DHT11Test(unittest.TestCase):
    def setUp(self):
        from fixtures import test_data
        self.raw_bits = test_data.raw_bits_dht11
        self.dht11 = DHT11(12, MagicMock())

    def test__get_temp_humidity_tuple(self):
        actual = self.dht11._get_temp_humidity_tuple([40, 0, 24, 0, 64])
        self.assertEqual(actual, (24, 40))


class DHT22Test(unittest.TestCase):
    def setUp(self):
        from fixtures import test_data
        self.raw_bits = test_data.raw_bits_dht22
        self.dht22 = DHT22(12, MagicMock())

    def test__get_temp_humidity_tuple(self):
        actual = self.dht22._get_temp_humidity_tuple([2, 123, 1, 32, 161])
        self.assertEqual(actual, (28.8, 63.5))
