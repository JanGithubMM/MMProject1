#!/usr/bin/python
import os

#def disk_exists(path):
#	try:
#		return os.stat.S_ISBLK(os.stat(path).st_mode)
#	except:
#		return False

#if disk_exists("/dev/sda1"):
#	print("writing to usbdrv")
os.system("sudo mount /dev/sda1 /home/pi/usbdrv")
#else:
#	print("no usb connected")
