#!/usr/bin/env python3
from time import sleep
from dht11 import DHT11


def read_results_without_exceptions():
    # Adjust pin (BCM) for your needs !
    dht11 = DHT11(14)

    while True:
        # Retries 'max_tries' from DHT11 to get a valid result
        r = dht11.get_result(max_tries=10)  # 'max_tries' defaults to 5
        if r:
            print(r)
        else:
            print('Failed to get result !')
        sleep(1)


def read_results_with_exceptions():
    # Adjust pin (BCM) for your needs !
    dht11 = DHT11(14)

    while True:
        try:
            print(dht11.get_result_once())
        except Exception as e:
            print(e)
        sleep(1)
