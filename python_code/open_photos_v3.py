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
screen_size = (windowInfo.current_w,windowInfo.current_h)
stap_lock = False
key_Check= True
x = 0

def fotosladen():
	for file in os.listdir("/home/pi/usbdrv"):
		if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG"):
			#image.append(file)
			image = pygame.image.load("/home/pi/usbdrv/"+file)
			image = pygame.transform.scale(image, (screen_size))
			yield image

screen = pygame.display.set_mode((windowInfo.current_w,(windowInfo.current_h)))
foto_generator = fotosladen()
image = foto_generator.next()
photo = image
volgende_foto = foto_generator.next()
	

while True:
	if key_Check:
		sensor_value = (GPIO.input(23),GPIO.input(24))
		events = pygame.event.get()
		if (sensor_value == (0,1) and stap_lock==False):
			if x < windowInfo.current_w:
				x += 100
			else:
				x = 0	
				image = volgende_foto
				photo = image
				screen.blit(photo, (0,0))
				pygame.display.flip()
				try:
					volgende_foto = foto_generator.next()
				except StopIteration:
					foto_generator = fotosladen()
					image = foto_generator.next()
					photo = image
					volgende_foto = foto_generator.next()
				stap_lock = True
				key_Check = False
		if (sensor_value == (1,0) and stap_lock==True):
			if x < windowInfo.current_w:
				x += 100
			else:
				x = 0
				image = volgende_foto
				photo = image
				screen.blit(photo, (0,0))
				pygame.display.flip
				try:
					volgende_foto = foto_generator.next()
				except StopIteration:
					foto_generator = fotosladen()
					image = foto_generator.next()
					photo = image
					volgende_foto = foto_generator.next()
				key_Check = False
				stap_lock = False
		for event in events:
			if event.key == pygame.K_ESCAPE:
				sys.exit(0)
	screen.blit(photo, (0,0))
	pygame.draw.rect(screen,(132,240,95),(0,windowInfo.current_h-80,x,windowInfo.current_h),0)
	pygame.display.flip()  	
	key_Check = True

