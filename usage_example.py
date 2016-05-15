#!/usr/bin/env python3
import RPi.GPIO as GPIO
from dht11 import DHT11

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# Adjust pin for your needs !
dht11 = DHT11(pin=14)
dht11.get_bytes_from_dht11()
