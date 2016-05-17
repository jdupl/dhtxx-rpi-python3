#!/usr/bin/env python3
from time import sleep
from dht11 import DHT11

# Adjust pin (BCM) for your needs !
dht11 = DHT11(14)

while True:
    r = dht11.get_result()

    if r:
        print(r)
    else:
        print('failed to get result !')
    sleep(1)
