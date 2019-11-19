import spidev
import time

def ReverseBits(byte):
	byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
	byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
	byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
	return byte
#end def

def ByteToHex(Bytes):
	return ''.join(["0x%02X " %  x for x in Bytes]).strip()
#end def

spi  = spidev.SpiDev()					# Create spi object
# open spi port 0, device (CS) 0
spi.open(0,0)
spi.bits_per_word = 8
spi.max_speed_hz = 10000000
spi.mode = 0
'''
print(spi.bits_per_word)
print(spi.cshigh)
print(spi.loop)
print(spi.lsbfirst)
print(spi.max_speed_hz)
print(spi.mode)
print(spi.threewire)
'''
a = 0x00

try:
	while True:
		resp = spi.xfer2([a, 0x00])			# transfer one byte
		resp1 = ByteToHex([resp[1]])
		print(a," ", resp1)
		time.sleep(0.1)					# sleep for 0.1 seconds
		if (a > 0x1C):
			spi.close()
			break
		#end if
		a = a + 1
	# end while
except KeyboardInterrupt:
	spi.close()
# end try
