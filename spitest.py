#!/usr/bin/python3
import RPi.GPIO as GPIO
import spidev
import time

GPIO.setmode(GPIO.BCM)		# Pines se numeran por la Broadcom
#GPIO.setmode(GPIO.BOARD)	# Pines se numeran de forma fisica
GPIO.setwarnings(False)
GPIO.setup(8,GPIO.OUT)
# Create spi object
spi = spidev.SpiDev()

# Open spi port 0, device (CS) 0
spi.open(0, 0)

spi.bits_per_word = 8
spi.cshigh = False
spi.mode = 0
spi.loop = False
spi.lsbfirst = False
spi.threewire = False

time.sleep(1)

try:
	while True:
		GPIO.output(8,GPIO.LOW)
		resp = spi.xfer2([0x00,0x01,0x01])	# transfer one byte
		GPIO.output(8,GPIO.HIGH)

		print("%d\t%d\t%d\n" %(resp[0],resp[1],resp[2]))

		time.sleep(1)				# sleep for 0.1 seconds
	#end while
except KeyboardInterrupt:			# Ctrl+C pressed, so...
	print ("Rutina Terminada")
	spi.close()
#end try

