from __future__ import division
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
groteKaartjes = [[],[],[],[],[],[],[],[]]
pygame.init()
windowInfo = pygame.display.Info()
screen_w = 1000 #windowInfo.current_w
screen_h = 500 #windowInfo.current_h
screen_size = (screen_w,screen_h)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.mouse.set_visible(False)

achtergrond = pygame.image.load("/home/pi/Documents/Photos/Steps_achtergrond_def.png")

achtergrond = pygame.transform.scale(achtergrond, (screen_w, screen_h),)
#screen.blit(achtergrond, (0,0))
#pygame.display.flip()

def kaartjes_scalen():
        aantalOefeningen = 8
        for file in os.listdir("/home/pi/Documents/Kaartjes"):
                if file.endswith(".png")|file.endswith(".PNG"):
                        plaatje = pygame.image.load("/home/pi/Documents/Kaartjes/"+file)

                        #if file[0] > aantalOefeningen:
                        #        aantalOefeningen = file[0]
                        #        while len(groteKaartjes) < aantalOefeningen:
                        #                print(aantalOefeningen)
                        #                print(len(groteKaartjes))
                        #                print(groteKaartjes)
                        #                groteKaartjes.append([])
                        
                        for oefeningNummer in range(0, aantalOefeningen):   #omdat er maar 7 oefeningen zijn.
                                if file[0] == ("%d" % oefeningNummer):  #dit werkt nu.                                        
                                        try:
                                                groteKaartjes[oefeningNummer].append(plaatje)
                                                print("bestaande oefening")
                                                print(oefeningNummer)
                                        except IndexError:
                                                oefening = [] #new oefening
                                                print("new oefening")
                                                print(oefeningNummer)
                                                oefening.append(plaatje)
                                                print groteKaartjes
                                                groteKaartjes.insert(oefeningNummer, oefening)
                                                print groteKaartjes
                                        break
                                
                                
        print(groteKaartjes)

kaartjes_scalen()

#groteKaartjes
#        oefening 1
#                plaatje 1
#                plaatje 2
#        oefening 2
#                plaatje 1
#                plaatje 2
#                plaatje 3 

screen.blit(achtergrond, (0,0))

huidige_kaartje_x = ((screen_w/2)- pygame.Surface.get_width(groteKaartjes[1][0])/2)       
huidige_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(groteKaartjes[1][0])/1.75)
#vorige_kaartje_x = ((huidige_kaartje_x/2)-pygame.Surface.get_width(kleine_kaartjes[0])/2)
#klein_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(kleine_kaartjes[0])/1.75)
#volgende_kaartje_x = (((screen_w-(pygame.Surface.get_width(kaartjes[0])+huidige_kaartje_x))/2+(pygame.Surface.get_width(kaartjes[0])+huidige_kaartje_x))-pygame.Surface.get_width(kleine_kaartjes[0])/2)

x = 2
animatie = 0
while True:
        if sensorLinks.value > 0.1:
                if x < len(groteKaartjes)-1:
                        x = x + 1
        #if (sensorLinks.value > sensorTrigger and sensorRechts.value < sensorTrigger): #links
                #time.sleep(1)
                #if sensor_value == (1,0):
                       # pygame.quit()
                       # os.system('python /home/pi/python_code/Steps2/steps_v2_leunen.py')
        #               x = x + 10
        #elif sensor_value == (1,1):
        #elif (sensorLinks.value > sensorTrigger and sensorRechts.value > sensorTrigger): #allebei
                #os.system('python /home/pi/python_code/Steps2/steps_v2_staan_zitten.py')
        #       break
        elif sensorRechts.value > 0.1:
                if x > 0:
                        x = x - 1
        #elif (sensorLinks.value < sensorTrigger and sensorRechts.value > sensorTrigger): #rechts
                #time.sleep(1)
                #if sensor_value == (0,1):
        #       if (sensorLinks.value < sensorTrigger and sensorRechts.value > sensorTrigger):
                        #screen.fill((255,255,255))
                        #pygame.quit()
                        #os.system('python /home/pi/python_code/Steps2/steps_v2_been_optillen.py')
        #                x = x - 10
        screen.blit(groteKaartjes[x][animatie], (huidige_kaartje_x,huidige_kaartje_y))

        #print(x)
        #print(animatie)
        #print(groteKaartjes[x])
        #print(len(groteKaartjes[x]))
        
        if animatie == len(groteKaartjes[x])-1:
                animatie = 0
        else:
                animatie = animatie + 1
                
        #if (x-1 >= 0 ):
        #        screen.blit(kleine_kaartjes[x-1], (vorige_kaartje_x,klein_kaartje_y))
        #else:
        #        screen.blit(achtergrond,(vorige_kaartje_x,klein_kaartje_y),(vorige_kaartje_x,klein_kaartje_y,pygame.Surface.get_width(kleine_kaartjes[0]),pygame.Surface.get_height(kleine_kaartjes[0])))
        #if (x+1 < len(kleine_kaartjes)):
        #        screen.blit(kleine_kaartjes[x+1], (volgende_kaartje_x,klein_kaartje_y))
        #else:
        #        screen.blit(achtergrond, (volgende_kaartje_x,klein_kaartje_y),(vorige_kaartje_x,klein_kaartje_y,pygame.Surface.get_width(kleine_kaartjes[0]),pygame.Surface.get_height(kleine_kaartjes[0])))
        pygame.display.flip()
        time.sleep(1)
