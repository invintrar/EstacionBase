#!/usr/bin/python3
import spidev
#import Rpi.GPIO as GPIO
import time

spi = spidev.SpiDev()

spi.open(0,0)

to_send = [0x00, 0x01, 0x02]

def ByteToHex(Bytes):
	return ''.join(["0x%02X " % x for x in Bytes]).strip()
#end

def ReverseBits(byte):
	byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
	byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
	byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
	return byte
#end def


try:
	while True:
		resp = spi.xfer2(to_send)
		print(ByteToHex(resp))
		time.sleep(1)
	#end while
except KeyboardInterrupt:
	spi.close()
#end try

