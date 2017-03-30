from __future__ import division
import pygame
import time
import os
import sys
from gpiozero import MCP3008
import RPi.GPIO as GPIO
import math

#typed on the pi

kleine_kaartjes = [None,None,None,None,None,None,None]
grote_kaartjes = [[],[],[],[],[],[],[]]
minimum_links = 1.0
minimum_rechts = 1.0

def init_sensors():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    s_l = MCP3008(1)     #druksensor links
    s_r = MCP3008(3)     #druksensor rechts
    return(s_l, s_r)

def init_pygame_and_screen():  #pygame en screen init
    pygame.init()
    windowInfo = pygame.display.Info()
    screen_w = windowInfo.current_w
    screen_h = windowInfo.current_h
    #screen_w = 800                     #voor testen met andere schermresolutie
    #screen_h = 600                     #voor testen met andere schermresolutie
    screen = pygame.display.set_mode((screen_w,screen_h))
    pygame.mouse.set_visible(False)
    return (screen, screen_w, screen_h)

def init_variables(screen_h):
    my_font = pygame.font.SysFont("Arial", int(screen_h/25))
    return my_font

def init_steps():
    sensors = init_sensors()
    screen, screen_w, screen_h = init_pygame_and_screen()
    my_font = init_variables(screen_h)
    return (sensors, screen, screen_w, screen_h, my_font)

def fotos_laden(screen_w, screen_h):           #fotos inladen en schalen
    screen_ratio = ((screen_w*(4/5)) / screen_h)
    print(screen_ratio)
    print((screen_w*(4/5)),screen_h)
    usbStickHasNoPhotos = True
    for file in os.listdir("/home/pi/usbdrv"):
        if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
            usbStickHasNoPhotos = False
            image = pygame.image.load("/home/pi/usbdrv/"+file)
            image_ratio = image.get_width()/image.get_height()
            if image_ratio < screen_ratio:          #zwarte balk aan de zijkant
                    image = pygame.transform.scale(image, (int(screen_h*image_ratio), screen_h))
            else:                                   #zwarte balk aan de onder en bovenkant
                    image = pygame.transform.scale(image, ((screen_w*(4/5)), ((screen_w*(4/5))*image_ratio)))
            yield image
    if (usbStickHasNoPhotos):
            for file in os.listdir("/home/pi/Pictures/Voorbeeldfotos"):
                    if file.endswith(".png")|file.endswith(".PNG")|file.endswith(".jpg")|file.endswith(".JPG")|file.endswith(".jpeg")|file.endswith(".JPEG"):
                            image = pygame.image.load("/home/pi/Pictures/Voorbeeldfotos/"+file)
                            image = scale_binnen_grenzen(image, screen_w*(4/5), screen_h)
                            yield image

def kaartjes_scalen(screen_w, screen_h):
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

def menu_steps(init_info, oefening_selected, welcome):
    sensors, screen, screen_w, screen_h, my_font = init_info
    s_l, s_r = sensors
    sensor_trigger = 0.1
    x = oefening_selected
    oefeningNumber = 0
    
    #Audio Init
    welkom_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/welkom_bij_steps.wav")
    goed_gedaan1 = pygame.mixer.Sound("/home/pi/Documents/Audio/goed_gedaan.wav")
    goed_gedaan2 = pygame.mixer.Sound("/home/pi/Documents/Audio/10_keer_gedaan_goed_werk.wav")
    goed_gedaan3 = pygame.mixer.Sound("/home/pi/Documents/Audio/goed_bezig.wav")
    goed_gedaan_special = pygame.mixer.Sound("/home/pi/Documents/Audio/goed_gedaan_barbershop.wav")

    achtergrond = pygame.image.load("/home/pi/Documents/Photos/Steps_achtergrond_def.png")
    oefening_klaar = pygame.image.load("/home/pi/Documents/Instructie/Oefening_Klaar.png")
    achtergrond = pygame.transform.scale(achtergrond, (screen_w, screen_h),)
    oefening_klaar = pygame.transform.scale(oefening_klaar, (screen_w, screen_h),)

    if (welcome):
        pygame.mixer.Sound.play(welkom_audio)

    ##!let op vanaf nu staat oefeningen 1 dus op positie grote_kaartjes[0]. Hierdoor kan oefening 0 dus niet worden toegevoegd. Oefeningen moeten altijd een nummer groter dan 0 hebben.

    kaartjes_scalen(screen_w, screen_h)
    screen.blit(achtergrond, (0,0))

    huidige_kaartje_x = ((screen_w/2)- pygame.Surface.get_width(grote_kaartjes[0][0])/2)
    huidige_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(grote_kaartjes[0][0])/1.75)
    vorige_kaartje_x = ((huidige_kaartje_x/2)-pygame.Surface.get_width(kleine_kaartjes[1])/2)
    klein_kaartje_y = ((screen_h/2)- pygame.Surface.get_height(kleine_kaartjes[0])/1.75)
    volgende_kaartje_x = (((screen_w-(pygame.Surface.get_width(grote_kaartjes[0][0])+huidige_kaartje_x))/2+(pygame.Surface.get_width(grote_kaartjes[0][0])+huidige_kaartje_x))-pygame.Surface.get_width(kleine_kaartjes[0])/2)

    #dit moet 0 zijn omdat oefeningen bij 0 begint
    animatie = 0 #deze variabele reguleert de animatie
    animatie_counter = 0
    sensor_counter = 0
    links = 0
    rechts = 0
    lock_rechts = 0
    lock_links = 0
    keuze_lock = 0
    klaar_counter = 0
    while True:
        klaar_counter = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()
        if (s_r_read(s_r.value) < sensor_trigger and s_l_read(s_l.value) > sensor_trigger):
                lock_links = 1
                keuze_lock = 0
        elif (s_r_read(s_r.value) > sensor_trigger and s_l_read(s_l.value) <sensor_trigger):
                lock_rechts = 1
                keuze_lock = 0
        elif (s_r_read(s_r.value) < sensor_trigger and s_l_read(s_l.value) < sensor_trigger):
                keuze_lock = 0

        if(s_l_read(s_l.value) < sensor_trigger and lock_links == 1):
                lock_links = 0
                if x > 0:
                        x = x - 1
                        animatie = 0
        if(s_r_read(s_r.value) < sensor_trigger and lock_rechts == 1):
                lock_rechts = 0
                if x < len(kleine_kaartjes)-1:
                        x = x + 1
                        animatie = 0
        
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
        animatie_counter += 1
        if(animatie_counter > 12):
                animatie_counter = 0
                if (animatie == len(grote_kaartjes[x])-1):
                        animatie = 0
                else:
                        animatie += 1
            
        pygame.display.update()
        
        #keuze
        if(s_l_read(s_l.value) > sensor_trigger and s_r_read(s_r.value) > sensor_trigger and keuze_lock == 0):
            keuze_lock = 1
            pygame.mixer.stop()
            return x

def oefening_steps(init_info, oefening_chosen):
    sensors, screen, screen_w, screen_h, my_font = init_info
    s_l, s_r = sensors
    houding1_audio, houding2_audio = init_audio(oefening_chosen)
    achtergrond = set_achtergrond(screen, screen_w, screen_h)
    
    foto_generator = fotos_laden(screen_w, screen_h)
    photo, photo_pos = select_volgende_foto(foto_generator, screen_w)   #selecteerde de eerste foto, omdat deze functie nog niet eerder aangeroepen is.

    oefening = Oefening(oefening_chosen, screen_w, screen_h)
    uitvoeringen_totaal = oefening.aantal_uitvoeringen
    uitvoeringen_gedaan = 0         #De oefening start altijd met 0 uitvoeringen.
    uitvoeringen_gedaan = verhoog_aantal_uitvoeringen(screen, achtergrond, screen_h, uitvoeringen_gedaan, uitvoeringen_totaal, my_font, verhoging = 0)

    fase = 1        #De oefeningen starten allemaal in fase 1
    houding = 1     #De oefeningen starten allemaal in houding 1
    pygame.mixer.Sound.play(houding1_audio)
    teller = 0      
    
    while (GPIO.input(4)!=1 and uitvoeringen_gedaan < uitvoeringen_totaal):

        check_keys()
        set_sensor_info(screen, achtergrond, oefening, oefening_chosen, houding, s_l, s_r, screen_h, screen_w)   #niet afhankelijk van de fase

        time.sleep(0.02)
        if(fase == 1):      #houding 1 aanhouden
            set_houding(screen, achtergrond, 1, oefening)  #afgebeelde houding aanpassen als nodig

            if(oefening.check_houding(oefening_chosen, houding, s_l, s_r)):      #hieruit komt een True of False
                teller += 1
                set_photo(screen, photo, photo_pos, screen_w, screen_h, teller, oefening.teller_totaal)
            if(teller > oefening.teller_totaal):         #houding 1 afgerond
                uitvoeringen_gedaan = verhoog_aantal_uitvoeringen(screen, achtergrond, screen_h, uitvoeringen_gedaan, uitvoeringen_totaal, my_font)
                photo, photo_pos = select_volgende_foto(foto_generator, screen_w)    #alvast de volgende foto inladen
                set_houding(screen, achtergrond, 2, oefening)  #afgebeelde houding aanpassen als nodig
                houding = 2         #wisselen naar houding 2
                teller = 0
                fase = 2
                play_sound(houding2_audio)
        elif(fase == 2):    #wisselen naar houding 2
            #iets dat de gebruiker attendeert om te wisselen van houding
            if(oefening.check_houding(oefening_chosen, houding, s_l, s_r)):      #hieruit komt een True of False
                pygame.mixer.stop()
                screen.blit(achtergrond, (screen_w/5,0), area=[screen_w/5,0,screen_w*(4/5),screen_h])   #achtergrond foto maken
                fase = 3
        elif(fase == 3):    #houding 2 aanhouden
            set_houding(screen, achtergrond, 2, oefening)  #afgebeelde houding aanpassen als nodig
            if(oefening.check_houding(oefening_chosen, houding, s_l, s_r)):      #hieruit komt een True of False
                teller += 1
                set_photo(screen, photo, photo_pos, screen_w, screen_h, teller, oefening.teller_totaal)
            if(teller > oefening.teller_totaal):         #houding 2 afgerond
                uitvoeringen_gedaan = verhoog_aantal_uitvoeringen(screen, achtergrond, screen_h, uitvoeringen_gedaan, uitvoeringen_totaal, my_font)
                photo, photo_pos = select_volgende_foto(foto_generator, screen_w)    #alvast de volgende foto inladen
                set_houding(screen, achtergrond, 1, oefening)  #afgebeelde houding aanpassen als nodig
                houding = 1         #wisselen naar houding 1
                teller = 0
                fase = 4
                play_sound(houding1_audio)
        elif(fase == 4):    #wisselen naar houding 1
            #iets dat de gebruiker attendeert om te wisselen van houding
            if(oefening.check_houding(oefening_chosen, houding, s_l, s_r)):      #hieruit komt een True of False
                pygame.mixer.stop()
                screen.blit(achtergrond, (screen_w/5,0), area=[screen_w/5,0,screen_w*(4/5),screen_h])   #achtergrond foto maken
                fase = 1
    oefening_result = (uitvoeringen_gedaan, uitvoeringen_gedaan >= uitvoeringen_totaal)
    pygame.mixer.stop()
    oefening_klaar = pygame.image.load("/home/pi/Documents/Instructie/Oefening_Klaar.png")
    screen.blit(oefening_klaar,(0,0))
    pygame.display.update()
    klaar_counter = 0
    while(klaar_counter < 30):
        time.sleep(0.1)
        if(s_l_read(s_l.value) < 0.1 and s_r_read(s_r.value) <  0.1):
            klaar_counter += 1
        else:
            klaar_counter = 0
    return oefening_result

def set_photo(screen, photo, photo_pos_x, screen_w, screen_h, teller, teller_totaal):
    photo_part_h = photo.get_height()
    photo_part_w = math.ceil(photo.get_width()/teller_totaal)
    photo_part_pos_x = photo_part_w * teller
    photo_part_pos_y = screen_h/2 - photo_part_h/2
    screen_part_w_pos = screen_w/teller_totaal * teller
    
    screen.blit(photo, (photo_pos_x+photo_part_pos_x,photo_part_pos_y), area=[photo_part_pos_x,0,photo_part_w,photo_part_h]) # van links naar rechts
    pygame.display.update()

def select_foto(volgende_foto):
    image = volgende_foto
    photo = image
    return photo

def set_achtergrond(screen, screen_w, screen_h):
    achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Steps_achtergrond.png")
    achtergrond = pygame.transform.scale(achtergrond, (screen_w, screen_h))
    screen.blit(achtergrond, (0,0))
    pygame.display.update()
    return achtergrond


def select_volgende_foto(foto_generator, screen_w):
    try:
            volgende_foto = foto_generator.next()
    except StopIteration:
            foto_generator = fotos_laden()
            volgende_foto = foto_generator.next()

    photo_pos_x = math.ceil((screen_w*(3/5))-(volgende_foto.get_width()/2))
    return volgende_foto, photo_pos_x

def verhoog_aantal_uitvoeringen(screen, achtergrond, screen_h, aantal_uitvoeringen, uitvoeringen_totaal, my_font, verhoging = 1):
    aantal_uitvoeringen += verhoging
    uitvoering_text = my_font.render("%s van de %s" % (aantal_uitvoeringen, uitvoeringen_totaal), 1, (0,0,0))
    screen.blit(achtergrond, (50,screen_h-(screen_h/22)-uitvoering_text.get_height()), area=[50,screen_h-(screen_h/22)-uitvoering_text.get_height(),uitvoering_text.get_width(),uitvoering_text.get_height()])
    screen.blit(uitvoering_text, (50, screen_h-(screen_h/22)-uitvoering_text.get_height())) #de uitvoeringstekst
    pygame.display.update()
    return aantal_uitvoeringen

class Oefening:
    def __init__(self, oefening_chosen, screen_w, screen_h):
        if(oefening_chosen == 0):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 5
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/15c_Extensie_knie_in_zit.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/15b_Extensie_knie_in_zit.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 1):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/14a_Zit_naar_stand_twee_handen.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/14b_Zit_naar_stand_twee_handen.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 2):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/8a_achteruit_lopen_zonder.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/8b_achteruit_lopen_zonder.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 3):
            self.teller_totaal = 50
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/2a_Been_zijwaarts_heffen.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/2c_Been_zijwaarts_heffen.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 4):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/1a_Hiel_naar_de_bil.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/1e_Hiel_naar_de_bil.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 5):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/12c_Tien_seconden_op_1_been_staan_met_steun.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/12a_Tien_seconden_op_1_been_staan_met_steun.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
        elif(oefening_chosen == 6):
            self.teller_totaal = 150
            self.aantal_uitvoeringen = 10
            self.image_houding1 = pygame.image.load("/home/pi/Documents/Oefeningen/13c_Tien_seconden_op_1_been_staan_zonder_steun.png")        #aanpasbare afbeelding
            #self.image_houding1 = scale_binnen_grenzen(self.image_houding1, screen_w/5, screen_h*(2/5), smooth=True)
            self.image_houding1 = pygame.transform.smoothscale(self.image_houding1, (int(screen_w/100)*14, int(screen_w/100)*20))
            self.image_houding2 = pygame.image.load("/home/pi/Documents/Oefeningen/13a_Tien_seconden_op_1_been_staan_zonder_steun.png")        #aanpasbare afbeelding
            #self.image_houding2 = scale_binnen_grenzen(self.image_houding2, screen_w/5, screen_h*(2/5),smooth=True)
            self.image_houding2 = pygame.transform.smoothscale(self.image_houding2, (int(screen_w/100)*14, int(screen_w/100)*20))
    def check_houding(self, oefening_chosen, houding, s_l, s_r):
        if(houding == 1):
            s_trigger_links = 0.1
            s_trigger_rechts = 0.1
            if(oefening_chosen == 0):       #knie extensie
                s_trigger_links = 0.1
                s_trigger_rechts = 0.1
                return(s_l_read(s_l.value) < s_trigger_links and s_r_read(s_r.value) > s_trigger_rechts)
            elif(oefening_chosen == 1):     #staanzitten
                s_trigger_total = 0.8
                return(s_l_read(s_l.value) + s_r_read(s_r.value) < s_trigger_total)
            elif(oefening_chosen == 2):     #achterenlopen
                s_trigger_total = s_l_read(s_l.value) + s_r_read(s_r.value)
                return(s_l_read(s_l.value) > (s_trigger_total*0.7) and s_trigger_total > 0.1)
            elif(oefening_chosen == 3):     #beenheffen
                return(s_l_read(s_l.value) > s_trigger_links and s_r_read(s_r.value) < s_trigger_rechts)
            elif(oefening_chosen == 4):     #hak naar bil
                return(s_l_read(s_l.value) > s_trigger_links and s_r_read(s_r.value) < s_trigger_rechts)
            elif(oefening_chosen == 5 or oefening_chosen == 6):
                return(s_l_read(s_l.value) < s_trigger_links and s_r_read(s_r.value) > s_trigger_rechts)
        elif(houding == 2):
            s_trigger_links = 0.1
            s_trigger_rechts = 0.1
            if(oefening_chosen == 0):       #knie extensie
                s_trigger_links = 0.1
                s_trigger_rechts = 0.1
                return(s_l_read(s_l.value) > s_trigger_links and s_r_read(s_r.value) < s_trigger_rechts)
            elif(oefening_chosen == 1):     #staanzitten
                s_trigger_total = 0.8
                return(s_l_read(s_l.value) + s_r_read(s_r.value) > s_trigger_total)
            elif(oefening_chosen == 2):     #achterenlopen
                s_trigger_total = s_l_read(s_l.value) + s_r_read(s_r.value)
                return(s_r_read(s_r.value) > (s_trigger_total*0.7) and s_trigger_total > 0.1)
            elif(oefening_chosen == 3):     #beenheffen
                return(s_l_read(s_l.value) < s_trigger_links and s_r_read(s_r.value) > s_trigger_rechts)
            elif(oefening_chosen == 4):     #hak naar bil
                return(s_l_read(s_l.value) < s_trigger_links and s_r_read(s_r.value) > s_trigger_rechts)
            elif(oefening_chosen == 5 or oefening_chosen == 6):
                return(s_l_read(s_l.value) > s_trigger_links and s_r_read(s_r.value) < s_trigger_rechts)

def set_houding(screen, achtergrond, houding, oefening):    
    houding_x = 20
    houding_y = 20
    if(houding == 1):   #de houding die afgebeeld wordt
        uitleg_plaatje = oefening.image_houding1
    elif(houding == 2):  #de houding die afgebeeld wordt
        uitleg_plaatje = oefening.image_houding2    
    screen.blit(achtergrond, (houding_x,houding_y), area=[houding_x,houding_y,uitleg_plaatje.get_width(),uitleg_plaatje.get_height()])
    screen.blit(uitleg_plaatje, (houding_x,houding_y))
    pygame.display.update()

def set_sensor_info(screen, achtergrond, oefening, oefening_chosen, houding, s_l, s_r, screen_h, screen_w):
        
    ### schalend maken op het scherm!!  ###
    #breedte = screen_w/5
    #hoogte = screen_h*(2/5)
    #x = 0
    #y = screen_h*(2/5)
    
    hoogte_sensor_links = math.floor(s_l_read(s_l.value) * 300)
    hoogte_sensor_rechts = math.floor(s_r_read(s_r.value) * 300)

    if(oefening.check_houding(oefening_chosen, houding, s_l, s_r)):
        kleur_sensor = (50,255,50)
    else:
        kleur_sensor = (255,50,50)
    
    screen.blit(achtergrond, (50,screen_h-550), area=[50,screen_h-550,200,305])
    if(hoogte_sensor_links > 0):
        pygame.draw.rect(screen,(kleur_sensor),(50,screen_h-250-hoogte_sensor_links,80,hoogte_sensor_links))
    if(hoogte_sensor_rechts > 0):
        pygame.draw.rect(screen,(kleur_sensor),(170,screen_h-250-hoogte_sensor_rechts,80,hoogte_sensor_rechts))
    pygame.display.update((50,screen_h-550,200,305))

    ######
    #pygame.display.update((0,screen_h*(2/5),screen_w/5,screen_h*(2/5)))
    ######
    

def init_audio(oefening_chosen):
    if(oefening_chosen == 0):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/strek_linkerbeen.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/strek_rechterbeen.wav")
    elif(oefening_chosen == 1):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/ga_zitten.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/ga_staan.wav")
    elif(oefening_chosen == 2):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/leun_naar_voren.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/leun_naar_achter.wav")
    elif(oefening_chosen == 3):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/til_rechterbeen_op.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/til_linkerbeen_op.wav")
    elif(oefening_chosen == 4):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/buig_rechterknie.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/buig_linkerknie.wav")
    elif(oefening_chosen == 5 or oefening_chosen == 6):
        houding1_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/sta_op_rechterbeen.wav")
        houding2_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/sta_op_linkerbeen.wav")
    return houding1_audio, houding2_audio

def play_sound(houding_audio):
    #time.sleep(1)
    pygame.mixer.Sound.play(houding_audio)

def check_keys():
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit(0)

def s_r_read(value):
    global minimum_rechts
    if value < minimum_rechts:
        minimum_rechts = value
    return (value - minimum_rechts)

def s_l_read(value):
    global minimum_links
    if value < minimum_links:
        minimum_links = value
    return (value - minimum_links)

def scale_binnen_grenzen(image, vak_w, vak_h, smooth=False):
    vak_ratio = vak_w/vak_h
    image_ratio = image.get_width()/image.get_height()
    
    if image_ratio < vak_ratio:          #balk aan de zijkant
        if(smooth):
            image = pygame.transform.smoothscale(image, (int(vak_h/image_ratio), int(vak_h)))
        else:
            image = pygame.transform.scale(image, (int(vak_h/image_ratio), int(vak_h)))
    else:                                   #balk aan de onder en bovenkant
        if(smooth):
            image = pygame.transform.smoothscale(image, (int(vak_w), int(vak_w/image_ratio)))
        else:
            image = pygame.transform.scale(image, (int(vak_w), int(vak_w/image_ratio)))
    return image


def oefening_uitleg(init_info, oefening_chosen):
    sensors, screen, screen_w, screen_h, my_font = init_info

    if(oefening_chosen == 0):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_ExtensieKnie.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_zit.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/5), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/9),(screen_h/2))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_benen_strekken.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_benen_strekken.wav")
    elif(oefening_chosen == 1):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StaanZitten.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_zit.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/5), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/9),(screen_h/2))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_staan_zitten.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_staan_zitten.wav")
    elif(oefening_chosen == 2):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_AchterenLopen.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsVerticaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_staat1.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/3), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/5.5),(screen_h/2-screen_h/6))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_achteren_lopen.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_achteren_lopen.wav")
    elif(oefening_chosen == 3):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_BeenHeffen.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_staat2.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/3), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/5.5),(screen_h/2-screen_h/6))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_been_heffen.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_been_heffen.wav")            
    elif(oefening_chosen == 4):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_HakNaarBil.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_staat2.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/3), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/5.5),(screen_h/2-screen_h/6))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_hak_naar_bil.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_hak_naar_bil.wav")
    elif(oefening_chosen == 5 or oefening_chosen == 6):
        #image
        instructie = pygame.image.load("/home/pi/Documents/Instructie/Instructie_OpEenBeenStaan.png")
        instructie = pygame.transform.scale(instructie, (screen_w, screen_h))
        plaatsing_achtergrond = pygame.image.load("/home/pi/Documents/Instructie/Instructie_StepsHorizontaal.png")
        plaatsing_achtergrond = pygame.transform.scale(plaatsing_achtergrond, (screen_w, screen_h))
        mannetje = pygame.image.load("/home/pi/Documents/Instructie/Oudere_staat2.png")
        mannetje_ratio = mannetje.get_width()/mannetje.get_height()
        mannetje = pygame.transform.smoothscale(mannetje,(int(screen_w/3), int(screen_w/5/mannetje_ratio)))
        pos_mannetje = ((screen_w/2 - screen_w/5.5),(screen_h/2-screen_h/6))
        #audio
        uitleg_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/uitleg_op_een_been_staan.wav")
        plaatsing_audio = pygame.mixer.Sound("/home/pi/Documents/Audio/plaatsing_op_een_been_staan.wav")

    #video
    pygame.mixer.Sound.play(uitleg_audio)

    screen.blit(instructie, (0,0))
    pygame.display.update()    
    for i in range (0, 100):
        time.sleep(uitleg_audio.get_length()/100)
        if (GPIO.input(4) == 1):
            pygame.mixer.stop()
            return

    pygame.mixer.Sound.play(plaatsing_audio)

    screen.blit(plaatsing_achtergrond, (0,0))
    pygame.display.update()
    for i in range (0, 100):
        time.sleep(plaatsing_audio.get_length()/2 /100)
        if (GPIO.input(4) == 1):
            pygame.mixer.stop()
            return
    screen.blit(mannetje, pos_mannetje)
    pygame.display.update()
    for i in range (0, 100):
        time.sleep(plaatsing_audio.get_length()/2 /100)
        if (GPIO.input(4) == 1):
            pygame.mixer.stop()
            
