#!/usr/bin/env python3
import RPi.GPIO as GPIO

from time import sleep
from dht11 import DHT11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Adjust pin for your needs !
dht11 = DHT11(14)

while True:
    r = dht11.get_result()

    if r:
        print(r)
    else:
        print('failed to get result !')
    sleep(1)
