import time
import RPi

from time import sleep
from statistics import mean


class DHT11:
    'DHT11 sensor reader class for Rpi.GPIO library (works with Pine64 port)'

    def __init__(self, pin):
        self.pin = pin

    def get_result(self, max_tries=50):
        """Try to get a valid result from the sensor within supplied limit.
        Returns None if limit has been reached.
        """
        start_time = time.time()

        for try_num in range(0, max_tries):
            r = self.get_result_once()

            if r:
                print(try_num)
                return r

    def get_result_once(self):
        try:
            byte_array = self._get_bytes_from_dht11()
            self._checksum(byte_array)
        except Exception as e:
            return

        rel_humidity = byte_array[0]
        temp = byte_array[2]
        return temp, rel_humidity

    def _checksum(self, byte_array):
        checksum = byte_array[0] + byte_array[1] + \
            byte_array[2] + byte_array[3] & 255
        if checksum != byte_array[4]:
            raise Exception('Checksum error')

    def _get_bytes_from_dht11(self):
        """Contact DHT11 and return bytes bytes"""
        RPi.GPIO.setup(self.pin, RPi.GPIO.OUT)

        RPi.GPIO.output(self.pin, RPi.GPIO.LOW)
        sleep(30 / 1000.0)  # Send signal for 30ms
        RPi.GPIO.output(self.pin, RPi.GPIO.HIGH)

        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, RPi.GPIO.PUD_UP)
        raw_bits = self._collect_raw_bits()
        impulses = self._get_data_impulses(raw_bits)

        if len(impulses) != 40:
            raise Exception('Missing data. Only got %d bits.' % len(impulses))

        bits = self._get_bits_from_impulses(impulses)

        return self._get_bytes_from_bits(bits)

    def _collect_raw_bits(self):
        seq_count = 0  # Sequential bits count
        last_bit = -1
        bits = []

        while seq_count < 64:
            bit = RPi.GPIO.input(self.pin)
            bits.append(bit)

            if last_bit != bit:
                seq_count = 0
                last_bit = bit
            else:
                seq_count += 1

        return bits

    def _get_bits_from_impulses(self, impulses):
        avg = mean(impulses)
        bits = []

        for impulse_length in impulses:
            bits.append(1 if impulse_length > avg else 0)

        return bits

    def _get_data_impulses(self, data_bits):
        impulses = []  # Defines length of each data impulse

        while len(data_bits) > 1:
            # Ignore pull down
            length = self._get_length_of_sequential_bits(data_bits, 0)
            data_bits = data_bits[length:]

            length = self._get_length_of_sequential_bits(data_bits, 1)
            data_bits = data_bits[length:]
            # Save length of pull up
            impulses.append(length)

        # Ignore init and final pull ups
        return impulses[1:-1]

    def _get_length_of_sequential_bits(self, bits, bit_type):
        for i, bit in enumerate(bits):
            if bit != bit_type:
                break
        return i

    def _get_bytes_from_bits(self, bits):
        byte_array = []

        for byte_index in range(0, len(bits), 8):
            byte = 0
            for bit_index in range(0, 8):
                byte = byte << 1 | bits[byte_index + bit_index]
            byte_array.append(byte)

        return byte_array
