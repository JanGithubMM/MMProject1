import sys
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

printlock=0
while True:
	print("%s \t %s") % (GPIO.input(23),GPIO.input(24)) 
	time.sleep(0.01)

 
