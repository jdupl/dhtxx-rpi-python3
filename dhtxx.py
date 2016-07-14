from time import sleep
from statistics import mean

GPIO = None


class DHT:
    """Reader class for DHTxx for GPIO library (works with Pine64 port)"""
    def __init__(self, pin, gpio_lib=None):
        """
        pin: BCM pin number
        gpio_lib: optional library injection (for tests, Pine64 or platforms)
        """
        self.pin = pin

        if not gpio_lib:
            # Loads only on a Raspberry Pi
            import RPi.GPIO as GPIO
        else:
            GPIO = gpio_lib
        self.gpio_lib = GPIO

        # GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

    def get_result(self, max_tries=5):
        """Try to get a valid result from the sensor within supplied limit.
        Returns the tuple (temperature, humidity) or None if 'max_tries'
        has been reached.
        """
        for try_num in range(0, max_tries):
            try:
                return self.get_result_once()
            except Exception:
                sleep(0.1)

    def get_result_once(self):
        """Only query DHT11 once.
        Returns the tuple (temperature, humidity) or throws exception.
        """
        byte_array = self._get_bytes_from_dht()
        self._checksum(byte_array)

        return self._get_temp_humidity_tuple(byte_array)

    def _get_temp_humidity_tuple(self, byte_array):
        """Abstract method implemented by DHT11/DHT22"""
        raise Exception('Unimplemented')

    def _checksum(self, byte_array):
        """Raises Exception if checksum is invalid."""
        checksum = byte_array[0] + byte_array[1] + \
            byte_array[2] + byte_array[3] & 255

        if checksum != byte_array[4]:
            raise Exception('Checksum error')

    def _get_bytes_from_dht(self):
        """Contact DHT11 and return bytes"""
        GPIO = self.gpio_lib
        raw_bits = []

        try:
            GPIO.setup(self.pin, GPIO.OUT)

            GPIO.output(self.pin, GPIO.LOW)
            sleep(30 / 1000.0)  # Send signal for 30ms
            GPIO.output(self.pin, GPIO.HIGH)

            GPIO.setup(self.pin, GPIO.IN, GPIO.PUD_UP)
            raw_bits = self._collect_raw_bits()
        except Exception:
            GPIO.cleanup()

        impulses = self._get_data_impulses(raw_bits)
        if len(impulses) != 40:
            raise Exception('Missing data. Only got %d bits.' % len(impulses))

        bits = self._get_bits_from_impulses(impulses)
        return self._get_bytes_from_bits(bits)

    def _collect_raw_bits(self):
        GPIO = self.gpio_lib
        seq_count = 0  # Sequential bits count
        last_bit = -1
        bits = []

        while seq_count < 64:
            bit = GPIO.input(self.pin)
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


class DHT11(DHT):
    """DHT11 sensor reader class """

    def __init__(self, *args, **kwargs):
        super(DHT11, self).__init__(*args, **kwargs)

    def _get_temp_humidity_tuple(self, byte_array):
        rel_humidity = byte_array[0]
        temp = byte_array[2]
        return temp, rel_humidity
