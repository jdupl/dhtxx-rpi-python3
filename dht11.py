from statistics import mean


class DHT11:
    'DHT11 sensor reader class for Rpi.GPIO library (works with Pine64 port)'

    def _get_bytes_from_bits(self, bits):
        byte_array = []

        for i in range(0, len(bits), 8):
            byte = 0
            for j in range(0, 8):
                byte = byte << 1 | bits[i + j]
            byte_array.append(byte)

        return byte_array

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
