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
grote_kaartjes = [[],[],[],[],[],[],[]]
kleine_kaartjes = [None,None,None,None,None,None,None]
pygame.init()
windowInfo = pygame.display.Info()
screen_w = 2000 #windowInfo.current_w
screen_h = 1200 #windowInfo.current_h
screen_size = (screen_w,screen_h)
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.mouse.set_visible(False)
welkom_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/welkom_bij_steps.wav")
time.sleep(1)
pygame.mixer.Sound.play(welkom_audio)

achtergrond = pygame.image.load("/home/pi/Documents/Photos/Steps_achtergrond_def.png")

achtergrond = pygame.transform.scale(achtergrond, (screen_w, screen_h),)

def kaartjes_scalen():
        aantalOefeningen = 8
        for file in os.listdir("/home/pi/Documents/Kaartjes"):
                if file.endswith(".png")|file.endswith(".PNG"):
                        raw_kaartje = pygame.image.load("/home/pi/Documents/Kaartjes/"+file)
                        for oefeningNummer in range(0, aantalOefeningen):
                                if file.startswith("%d" % oefeningNummer):
                                        groot_plaatje = pygame.transform.smoothscale(raw_kaartje,(int (screen_w/2.33),int(pygame.Surface.get_height(raw_kaartje)/pygame.Surface.get_width(raw_kaartje)*(screen_w/2.33))))
                                        grote_kaartjes[oefeningNummer-1].append(groot_plaatje)
                                        if (len(grote_kaartjes[oefeningNummer-1]) == 1):
                                                klein_plaatje = pygame.transform.smoothscale(raw_kaartje,(int (screen_w/4.64),int(pygame.Surface.get_height(raw_kaartje)/pygame.Surface.get_width(raw_kaartje)*(screen_w/4.64))))
                                                kleine_kaartjes[oefeningNummer-1]=klein_plaatje

##!let op vanaf nu staat oefeningen 1 dus op positie grote_kaartjes[0]. Hierdoor kan oefening 0 dus niet worden toegevoegd. Oefeningen moeten altijd een nummer groter dan 0 hebben.

kaartjes_scalen()
print(grote_kaartjes)
screen.blit(achtergrond, (0,0))

huidige_kaartje_x = ((screen_w/2)- pygame.Surface.get_width(grote_kaartjes[0][0])/2)
huidige_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(grote_kaartjes[0][0])/1.75)
vorige_kaartje_x = ((huidige_kaartje_x/2)-pygame.Surface.get_width(kleine_kaartjes[1])/2)
klein_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(kleine_kaartjes[0])/1.75)
volgende_kaartje_x = (((screen_w-(pygame.Surface.get_width(grote_kaartjes[0][0])+huidige_kaartje_x))/2+(pygame.Surface.get_width(grote_kaartjes[0][0])+huidige_kaartje_x))-pygame.Surface.get_width(kleine_kaartjes[0])/2)

x = 0  #dit moet 0 zijn omdat oefeningen bij 0 begint
animatie = 0 #deze variabele reguleert de animatie

while True:
        rechts = 0
        links = 0
        if sensorLinks.value > 0.1 and sensorRechts.value < 0.1:
                rechts = 1
        elif sensorRechts.value > 0.1 and sensorLinks.value <0.1:
                links = 1

        if (x-1 >= 0 ):
                screen.blit(kleine_kaartjes[x-1], (vorige_kaartje_x,klein_kaartje_y))
        else:
                screen.blit(achtergrond,(vorige_kaartje_x,klein_kaartje_y),(vorige_kaartje_x,klein_kaartje_y,pygame.Surface.get_width(kleine_kaartjes[0]),pygame.Surface.get_height(kleine_kaartjes[0])))
        if (x+1 < len(kleine_kaartjes)):
                screen.blit(kleine_kaartjes[x+1], (volgende_kaartje_x,klein_kaartje_y))
        else:
                screen.blit(achtergrond, (volgende_kaartje_x,klein_kaartje_y),(volgende_kaartje_x,klein_kaartje_y,pygame.Surface.get_width(kleine_kaartjes[0]),pygame.Surface.get_height(kleine_kaartjes[0])))

        screen.blit(grote_kaartjes[x][animatie], (huidige_kaartje_x,huidige_kaartje_y))
        #animatie
        if(animatie == len(grote_kaartjes[x])-1):
                animatie = 0
        else:
                animatie += 1
                
        time.sleep(0.5)
        
        #keuze
        if(sensorLinks.value > 0.1 and sensorRechts.value > 0.1):
                        if(x == 0):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_ExtensieKnie.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_ExtensieKnie.py")
                                
                        if(x == 1):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_StaanZitten.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_StaanZitten.py")
                                
                        if(x == 2):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_AchterenLopen.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_AchterenLopen.py")
                                
                        if(x == 3):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_BeenHeffen.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_Beenheffen.py")
                                
                        if(x == 4):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_HakNaarBil.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_HakNaarBil.py")
                                
                        if(x == 5):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_StaanOpEenBeen.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_OpEenBeenStaanMs.py")
                                
                        if(x == 6):
                                os.system("python /home/pi/python_code/Steps2/steps_v2_intro_StaanOpEenBeen.py")
                                os.system("python /home/pi/python_code/Steps2/steps_v2_OpEenBeenStaanZs.py")
                                
        elif(rechts == 1):
                if x < len(kleine_kaartjes)-1:
                        x = x + 1
                        animatie = 0
        elif(links == 1):
                if x > 0:
                        x = x - 1
                        animatie = 0

        pygame.display.flip()
        
        
