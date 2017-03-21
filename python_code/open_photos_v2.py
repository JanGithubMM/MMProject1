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
image=[]
x = 0
all_files = 0
##Init eerste foto##

for file in os.listdir("/home/pi/usbdrv"):
	if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG"):
		if (x == 0):
			image.append(file)
			image[x] = pygame.image.load("/home/pi/usbdrv/"+file)
			image[x] = pygame.transform.scale(image[x], (windowInfo.current_w,windowInfo.current_h))
			x += 1
		all_files += 1
screen = pygame.display.set_mode((windowInfo.current_w,(windowInfo.current_h)))

x = 0
photo = image[x]
screen.blit(photo, (0,0))
pygame.display.flip()

stap_lock = 0
#############################
foto_laden = True

while True:
	#photo = pygame.image.load("/home/pi/usbdrv/"+image[x])
	#photo = pygame.transform.scale(photo, (windowInfo.current_w/3,windowInfo.current_h/3))
	
	photo = image[x]
	screen.blit(photo, (0,0))
	pygame.display.flip()
	
	#hier wordt steeds 1 foto geladen (de eerst volgende) 		
	while foto_laden:
		current_foto = x
		x = 0
		for file in os.listdir("/home/pi/usbdrv"):
			if (file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")):
				if x == current_foto+1:
					image.append(file)
					image[x] = pygame.image.load("/home/pi/usbdrv/"+file)
					image[x] = pygame.transform.scale(image[x], (windowInfo.current_w,windowInfo.current_h))
					key_Check = True
				x = x + 1
		foto_laden = False
		x = current_foto

	if key_Check:		
		sensor_value = (GPIO.input(23),GPIO.input(24))
		events = pygame.event.get()
		if (sensor_value == (0,1) and stap_lock==0) and x < all_files:
			x = x + 1
			stap_lock = 1
			key_Check = False
			foto_laden = True
		if (sensor_value == (1,0) and stap_lock==1):
			stap_lock = 0
		for event in events:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					if x>0:
						x = x - 1
						key_Check = False
				if event.key == pygame.K_RIGHT:
					if x<all_files:	
						x= x + 1
						key_Check = False
						foto_laden = True
						break
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
