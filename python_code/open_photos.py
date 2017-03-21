#!/usr/bin/python

import pygame
import time
import os
import sys
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pygame.init()
windowInfo = pygame.display.Info()
x=0
image=[]



x = 0
for file in os.listdir("/home/pi/usbdrv"):
	if file.endswith(".png")|file.endswith(".JPG")|file.endswith(".jpg"):
		image.append(file)
		image[x] = pygame.image.load("/home/pi/usbdrv/"+file)
		image[x] = pygame.transform.scale(image[x], (windowInfo.current_w,windowInfo.current_h))
		x = x + 1	

screen = pygame.display.set_mode((windowInfo.current_w,(windowInfo.current_h)))

stap_lock = 0
x = 0
while True:
	#photo = pygame.image.load("/home/pi/usbdrv/"+image[x])
	#photo = pygame.transform.scale(photo, (windowInfo.current_w/3,windowInfo.current_h/3))
	sensor_value = (GPIO.input(23),GPIO.input(24))
	photo = image[x]
	screen.blit(photo, (0,0))
	pygame.display.flip()
	key_Check = True
	while key_Check:		
		sensor_value = (GPIO.input(23),GPIO.input(24))
		#pygame.display.update()
		#screen.blit(photo, (0,0))
		events = pygame.event.get()
		if (sensor_value == (0,1) and x < len(image)-1 and stap_lock==0):
			x = x + 1
			stap_lock = 1
			key_Check = False
		if (sensor_value == (1,0) and stap_lock==1):
			stap_lock = 0
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if x>0:
						x = x - 1
						key_Check = False
				if event.key == pygame.K_RIGHT:
					if x<len(image)-1:	
						x= x + 1
						key_Check = False
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
