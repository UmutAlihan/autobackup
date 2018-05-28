#!/usr/bin/python3


import RPi.GPIO as GPIO ## Import GPIO library
import time

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setwarnings(False)
GPIO.setup(17, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(17,True) ## Turn on GPIO pin 7
time.sleep(3)
GPIO.output(17,False) ## Turn on GPIO pin 7
