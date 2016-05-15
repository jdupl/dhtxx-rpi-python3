import Rpi

from statistics import mean
from time import sleep


class DHT11:
    'DHT11 sensor reader class for Rpi.GPIO library (works with Pine64 port)'

    def __init__(pin):
        self.pin = pin

    def get_bytes_from_dht11(self):
        """Contact DHT11 and return bytes bytes"""
        RPi.GPIO.setup(self.pin, RPi.GPIO.OUT)

        self._send(RPi.GPIO.HIGH, 0.05)
        self._send(RPi.GPIO.LOW, 0.02)

        RPi.GPIO.setup(self.pin, RPi.GPIO.IN, RPi.GPIO.PUD_UP)

        raw_bits = self._collect_raw_bits()
        bits = _get_bits_from_impulses(raw_bits)
        byte_array = _get_bytes_from_bits(bits)

        if len(bits) != 40:
            print('Missing data. Only got %d bits' % len(bits))
        print(byte_array)

    def _send(self, output, delay):
        RPi.GPIO.output(self.pin, output)
        sleep(delay)

    def _collect_raw_bits(self):
        seq_count = 0  # Sequential bits count
        last = -1
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
