from __future__ import division
import pygame
import time
import os
import sys
from gpiozero import MCP3008
import RPi.GPIO as GPIO

#GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#sensoren
sL = MCP3008(1)
sR = MCP3008(3)

#pygame en screen init
pygame.init()
windowInfo = pygame.display.Info()
screen_size = (windowInfo.current_w,windowInfo.current_h)
screen_w = windowInfo.current_w
screen_h = windowInfo.current_h
screen_ratio = int(screen_w / screen_h)
#screen_size = (1920,800)            #voor testen met andere schermresolutie
#screen_w = 1920                     #voor testen met andere schermresolutie
#screen_h = 800                      #voor testen met andere schermresolutie
myfont = pygame.font.SysFont("monospace", int(screen_h/25))

#vaste variable
stap_lock = "Rechts"
key_Check= True
black = (0,0,0)

#aanpasbare variable
xStep = screen_w/200        #bij 100 -> 1.4 sec      bij 150 -> 2.2 sec       bij 200 -> 3 sec
sT = 0.1
aantal_uitvoeringen = 10

#groene balk onderaan
x = xStep

#uitvoering van de oefening
uitvoering = 0         #de oefening is nog geen 1 keer uitgevoerd
uitvoeringText = myfont.render("%s van de %s" % (uitvoering ,aantal_uitvoeringen), 1, (255,255,255))

#fotos inladen en schalen
def fotosladen():
        usbStickHasNoPhotos = True
        for file in os.listdir("/home/pi/usbdrv"):
                if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
                        usbStickHasNoPhotos = False
                        image = pygame.image.load("/home/pi/usbdrv/"+file)
                        image_ratio = image.get_width()/image.get_height()
                        if image_ratio > screen_ratio:          #zwarte balk aan de zijkant
                                image = pygame.transform.scale(image, (int(screen_h*image_ratio), screen_h))
                        else:                                   #zwarte balk aan de onder en bovenkant
                                image = pygame.transform.scale(image, (screen_w, int(screen_w*image_ratio)))
                        yield image
        if (usbStickHasNoPhotos):
                for file in os.listdir("/home/pi/Pictures/Voorbeeldfotos"):
                        if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
                                image = pygame.image.load("/home/pi/Pictures/Voorbeeldfotos/"+file)
                                image = pygame.transform.scale(image, (screen_size))
                                yield image
                                
screen = pygame.display.set_mode((screen_w,(screen_h)))
pygame.mouse.set_visible(False)
foto_generator = fotosladen()
image = foto_generator.next()
photo = image
volgende_foto = foto_generator.next()
next_foto = False
screen.fill(black)
screen.blit(photo, (screen_w/2 - photo.get_width()/2, screen_h/2 - photo.get_height()/2))

#voorbeeld man of vrouw die de oefening voor doet.
voorbeeld1 = pygame.image.load("/home/pi/Documents/Oefeningen/13a_Tien_seconden_op_1_been_staan_zonder_steun.png")        #aanpasbare afbeelding
voorbeeld1 = pygame.transform.smoothscale(voorbeeld1, (int(screen_w/100)*14, int(screen_w/100)*20))
voorbeeld2 = pygame.image.load("/home/pi/Documents/Oefeningen/13c_Tien_seconden_op_1_been_staan_zonder_steun.png")        #aanpasbare afbeelding
voorbeeld2 = pygame.transform.smoothscale(voorbeeld2, (int(screen_w/100)*14, int(screen_w/100)*20))
voorbeeld = voorbeeld2
voorbeeldPosRechts = (screen_w - voorbeeld1.get_width(),0)
voorbeeldPosLinks = (0,0)
voorbeeldPos = voorbeeldPosRechts
screen.blit(voorbeeld, voorbeeldPos)

#audio
audio1 = pygame.mixer.Sound("/home/pi/Documents/Audio/sta_op_rechterbeen.wav")               #aanpasbare audio
audio2 = pygame.mixer.Sound("/home/pi/Documents/Audio/sta_op_linkerbeen.wav")                #aanpasbare audio
pygame.mixer.Sound.play(audio1)                                                #audio

#het hoofdprogramma
while True:
        if (GPIO.input(4)==1):
                pygame.quit()
                sys.exit(1)
        if key_Check:                                                   #Checkt hoe je staat en vult het balkje (als nodig)
                if (sL.value < sT and sR.value > sT and stap_lock=="Rechts"):        #aanpasbare if statement
                        if x < screen_w:
                                x += xStep
                        else:
                                if uitvoering == aantal_uitvoeringen:           #check of dit al de laatste uivoering was.
                                        pygame.quit()
                                        sys.exit(0)
                                uitvoering += 1
                                
                                voorbeeld = voorbeeld1
                                screen.fill(black)
                                screen.blit(photo, (screen_w/2 - photo.get_width()/2, screen_h/2 - photo.get_height()/2))
                                voorbeeldPos = voorbeeldPosLinks
                                screen.blit(voorbeeld, voorbeeldPos)
                                screen.blit(uitvoeringText, (screen_w-uitvoeringText.get_width() ,screen_h-(screen_h/22)-uitvoeringText.get_height()))
                                pygame.display.update()                                
                                pygame.mixer.Sound.play(audio2)                #audio
                                while (sL.value < sT or sR.value > sT):              #aanpasbare if statement
                                        time.sleep(0.1)
                                        if (GPIO.input(4)==1):
                                                pygame.quit()
                                                sys.exit(1)
                                stap_lock = "Links" #volgende foto
                                next_foto = True
                                key_Check = False
                elif (sL.value > sT and sR.value < sT and stap_lock=="Links"):       #aanpasbare if statement
                        if x < screen_w:
                                x += xStep
                        else: 
                                if uitvoering == aantal_uitvoeringen:           #check of dit al de laatste uivoering was.
                                        pygame.quit()
                                        sys.exit(0)
                                uitvoering += 1
                                
                                voorbeeld = voorbeeld2
                                screen.fill(black)
                                screen.blit(photo, (screen_w/2 - photo.get_width()/2, screen_h/2 - photo.get_height()/2))
                                voorbeeldPos = voorbeeldPosRechts
                                screen.blit(voorbeeld, voorbeeldPos)
                                screen.blit(uitvoeringText, (screen_w-uitvoeringText.get_width() ,screen_h-(screen_h/22)-uitvoeringText.get_height()))
                                pygame.display.update()
                                pygame.mixer.Sound.play(audio1)                #audio
                                while (sL.value > sT or sR.value < sT):              #aanpasbare if statement
                                        time.sleep(0.1)
                                        if (GPIO.input(4)==1):
                                                pygame.quit()
                                                sys.exit(1)
                                stap_lock = "Rechts" #volgende foto
                                next_foto = True
                                key_Check = False
                events = pygame.event.get()
                for event in events:
                        if event.type == pygame.KEYDOWN:
                                pygame.quit()
                                sys.exit(0)
        
        if next_foto:                           # Als dit True is gaat het systeem naar de volgende foto
                x = xStep
                image = volgende_foto
                photo = image
                screen.fill(black)
                screen.blit(photo, (screen_w/2 - photo.get_width()/2, screen_h/2 - photo.get_height()/2))
                screen.blit(voorbeeld, voorbeeldPos)
                pygame.display.flip()
                try:
                        volgende_foto = foto_generator.next()
                except StopIteration:
                        foto_generator = fotosladen()
                        volgende_foto = foto_generator.next()
                next_foto = False
                key_Check = True

                uitvoeringText = myfont.render("%s van de %s" % (uitvoering ,aantal_uitvoeringen), 1, (255,255,255))
        
        pygame.draw.rect(screen,(132,240,95),(0,screen_h-(screen_h/22),x,screen_h),0) #groene balk
        screen.blit(uitvoeringText, (screen_w-uitvoeringText.get_width() ,screen_h-(screen_h/22)-uitvoeringText.get_height())) #de uitvoeringstekst
        pygame.display.flip()
        time.sleep(0.01)
