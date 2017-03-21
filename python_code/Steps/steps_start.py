import pygame
import time
import RPi.GPIO as GPIO
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pygame.init()
windowInfo = pygame.display.Info()
screen_size = (windowInfo.current_w,windowInfo.current_h)
screen = pygame.display.set_mode((windowInfo.current_w, windowInfo.current_h))
pygame.mouse.set_visible(False)
font = pygame.font.Font(None, 50)

uitleg = pygame.image.load("/home/pi/Documents/Photos/uitleg_start_scherm.png")

uitleg = pygame.transform.scale(uitleg, (windowInfo.current_w, windowInfo.current_h),)
screen.blit(uitleg, (0,0))
pygame.display.flip()

while True:
        sensor_value = (GPIO.input(4),GPIO.input(15))
        print sensor_value
        if sensor_value == (1,0):
                time.sleep(1)
                sensor_value = (GPIO.input(4),GPIO.input(15))
                print sensor_value
                if sensor_value == (1,0):
                        screen.fill((255,255,255))
                        text = font.render("Je hebt gekozen voor leunen.", 1, (0,0,0))
                        textpos = text.get_rect()
                        textpos.centerx = screen.get_rect().centerx
                        textpos.centery = screen.get_rect().centery
                        screen.blit(text, textpos)
                        pygame.display.update()
                        time.sleep(2)
                        pygame.quit()
                        os.system('python /home/pi/python_code/Steps2/steps_v1_leunen.py')
                        break
        elif sensor_value == (1,1):
                screen.fill((255,255,255))
                text = font.render("Je hebt gekozen voor zitten staan.", 1, (0,0,0))
                textpos = text.get_rect()
                textpos.centerx = screen.get_rect().centerx
                textpos.centery = screen.get_rect().centery
                screen.blit(text, textpos)
                pygame.display.update()
                time.sleep(2)
                pygame.quit()
                os.system('python /home/pi/python_code/Steps2/steps_v1_zitten-staan.py')
                break
        elif sensor_value == (0,1):
                time.sleep(1)
                sensor_value = (GPIO.input(24),GPIO.input(23))
                print sensor_value
                if sensor_value == (0,1):
                        screen.fill((255,255,255))
                        text = font.render("Je hebt gekozen voor been optillen.", 1, (0,0,0))
                        textpos = text.get_rect()
                        textpos.centerx = screen.get_rect().centerx
                        textpos.centery = screen.get_rect().centery
                        screen.blit(text, textpos)
                        pygame.display.update()
                        time.sleep(2)
                        pygame.quit()
                        os.system('python /home/pi/python_code/Steps2/steps_v1_been-optillen.py')
                        break
