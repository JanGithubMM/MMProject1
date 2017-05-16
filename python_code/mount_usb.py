import os

if os.path.exists("/dev/sda1"):
    os.system("sudo mount /dev/sda1 /home/pi/usbdrv")
else:
    a = 0










#def disk_exists(path):
#	try:
#		return os.stat.S_ISBLK(os.stat(path).st_mode)
#	except:
#		return False

#if disk_exists("/dev/sda1"):
#	print("writing to usbdrv")

