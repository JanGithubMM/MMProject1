#!/usr/bin/python
from __future__ import division
import pygame
import time
import os
import sys
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
pygame.init()
windowInfo = pygame.display.Info()
screen_w = windowInfo.current_w
screen_h = windowInfo.current_h
screen_size = (screen_w, screen_h)
screen_ratio = int(screen_w/screen_h)



#image
instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_BeenHeffen.png")
instructie = pygame.transform.scale(instructie, (screen_size))
plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_size))
screen = pygame.display.set_mode((screen_w,(screen_h)))
mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_staat2.png")
mannetje_ratio = mannetje.get_width()/mannetje.get_height()
mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/3), int(screen_w/5/mannetje_ratio)))
#audio
uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_been_heffen.wav")
plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_been_heffen.wav")

#video
pygame.mixer.Sound.play(uitleg_audio)

screen.blit(instructie, (0,0))
pygame.display.flip()    
for i in range (0, 100):
    time.sleep(uitleg_audio.get_length()/100)
    if (GPIO.input(4) == 1) :
        pygame.quit()
        sys.exit(1)


pygame.mixer.Sound.play(plaatsing_audio)

screen.blit(plaatsing_achtergrond, (0,0))
pygame.display.flip()
for i in range (0, 100):
    time.sleep(plaatsing_audio.get_length()/2 /100)
    if (GPIO.input(4) == 1) :
        pygame.quit()
        sys.exit(1)
screen.blit(mannetje, ((screen_w/2 - screen_w/5.5),(screen_h/2-screen_h/6)))
pygame.display.flip()
for i in range (0, 100):
    time.sleep(plaatsing_audio.get_length()/2 /100)
    if (GPIO.input(4) == 1) :
        pygame.quit()
        sys.exit(1)

pygame.quit()
sys.exit(1)


