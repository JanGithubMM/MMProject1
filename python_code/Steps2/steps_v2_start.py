import pygame
import time
#import RPi.GPIO as GPIO
import os
from gpiozero import MCP3008

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

sensorLinks = MCP3008(1)
sensorRechts = MCP3008(3)
sensorTrigger = 0.1

pygame.init()
windowInfo = pygame.display.Info()
screen_size = (windowInfo.current_w,windowInfo.current_h)
screen = pygame.display.set_mode((windowInfo.current_w, windowInfo.current_h))
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 50)

uitleg = pygame.image.load("/home/pi/Documents/Photos/uitleg_start_scherm.png")

uitleg = pygame.transform.scale(uitleg, (windowInfo.current_w, windowInfo.current_h),)
screen.blit(uitleg, (-20,0))
pygame.display.flip()

while True:
        #sensor_value = (GPIO.input(24),GPIO.input(23))
        #if sensor_value == (1,0):
	if (sensorLinks.value > sensorTrigger and sensorRechts.value < sensorTrigger): #links
                time.sleep(1)
                #if sensor_value == (1,0):
		if (sensorLinks.value > sensorTrigger and sensorRechts.value < sensorTrigger):
                        screen.fill((255,255,255))
                        text = font.render("Je hebt gekozen voor leunen.", 1, (0,0,0))
                        textpos = text.get_rect()
                        textpos.centerx = screen.get_rect().centerx
                        textpos.centery = screen.get_rect().centery
                        screen.blit(text, textpos)
                        pygame.display.update()
                        time.sleep(2)
                        pygame.quit()
                        os.system('python /home/pi/python_code/Steps2/steps_v2_leunen.py')
                        break
        #elif sensor_value == (1,1):
	elif (sensorLinks.value > sensorTrigger and sensorRechts.value > sensorTrigger): #allebei
                screen.fill((255,255,255))
                text = font.render("Je hebt gekozen voor zitten staan.", 1, (0,0,0))
                textpos = text.get_rect()
                textpos.centerx = screen.get_rect().centerx
                textpos.centery = screen.get_rect().centery
                screen.blit(text, textpos)
                pygame.display.update()
                time.sleep(2)
                pygame.quit()
                os.system('python /home/pi/python_code/Steps2/steps_v2_staan_zitten.py')
                break
        #elif sensor_value == (0,1):
	elif (sensorLinks.value < sensorTrigger and sensorRechts.value > sensorTrigger): #rechts
                time.sleep(1)
                #if sensor_value == (0,1):
		if (sensorLinks.value < sensorTrigger and sensorRechts.value > sensorTrigger):
                        screen.fill((255,255,255))
                        text = font.render("Je hebt gekozen voor been optillen.", 1, (0,0,0))
                        textpos = text.get_rect()
                        textpos.centerx = screen.get_rect().centerx
                        textpos.centery = screen.get_rect().centery
                        screen.blit(text, textpos)
                        pygame.display.update()
                        time.sleep(2)
                        pygame.quit()
                        os.system('python /home/pi/python_code/Steps2/steps_v2_been_optillen.py')
                        break
