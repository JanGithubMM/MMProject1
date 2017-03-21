from gpiozero import MCP3008
import time
import pygame
import sys

pygame.init()
pygame.font.init()
#screen = pygame.display.set_mode()
#windowInfo = pygame.display.Info()

sensorLinks = MCP3008(1)
sensorRechts = MCP3008(3)
sensorTrigger = 0.1

myfont = pygame.font.SysFont("Comic Sans MS", 30)
text01 = myfont.render("0,1", 1, (255,255,0))
text02 = myfont.render("0,2", 1, (255,255,0))
text03 = myfont.render("0,3", 1, (255,255,0))
text04 = myfont.render("0,4", 1, (255,255,0))
text05 = myfont.render("0,5", 1, (255,255,0))
text06 = myfont.render("0,6", 1, (255,255,0))
text07 = myfont.render("0,7", 1, (255,255,0))

while True: 
	print sensorLinks.value, sensorRechts.value
	time.sleep(0.1)

while True:
	print sensorLinks.value, sensorRechts.value
	pygame.draw.rect(screen,(0,0,0),(0,0,windowInfo.current_w,windowInfo.current_h))
	screen.blit(text01,(710,windowInfo.current_h-100))
	screen.blit(text02,(710,windowInfo.current_h-200))
	screen.blit(text03,(710,windowInfo.current_h-300))
	screen.blit(text04,(710,windowInfo.current_h-400))
	screen.blit(text05,(710,windowInfo.current_h-500))
	screen.blit(text06,(710,windowInfo.current_h-600))
	screen.blit(text07,(710,windowInfo.current_h-700))
	pygame.draw.rect(screen,(255,255,0),(400,windowInfo.current_h-sensorLinks.value*10000,300,sensorLinks.value*10000))
	pygame.draw.rect(screen,(255,255,0),(750,windowInfo.current_h-sensorRechts.value*1000,300,sensorRechts.value*1000))
	pygame.display.flip()
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.KEYDOWN:
			sys.exit(0)
	time.sleep(0.1)
