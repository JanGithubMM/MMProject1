from gpiozero import MCP3008
import time
sensorLinks = MCP3008(1)
sensorRechts = MCP3008(3)
sensorTrigger = 0.1

while (sensorLinks.value < sensorTrigger):
	print sensorLinks.value, sensorRechts.value
	time.sleep(0.2)

print "links getriggerd"

while (sensorRechts.value < sensorTrigger):
	print sensorLinks.value, sensorRechts.value
	time.sleep(0.2)

print "rechts getriggerd"


while (sensorLinks.value < sensorTrigger or sensorRechts.value > sensorTrigger):
	print sensorLinks.value, sensorRechts.value
	time.sleep(0.2)

print "links wel, rechts niet"

while (sensorLinks.value > sensorTrigger or sensorRechts.value < sensorTrigger):
	print sensorLinks.value, sensorRechts.value
	time.sleep(0.2)

print "links niet, rechts wel"
