#!/usr/bin/python3

'''
@author: DarwinZh
'''

import spidev
import time


def ByteToHex(Bytes):
	return ''.join(["0x%02X " %  x for x in Bytes]).strip()
#end def

# Create spi object
spi  = spidev.SpiDev()
# open spi port 0, device (CS) 0
spi.open(0,0)
# numero de byte  para transmitir y recibir
spi.bits_per_word = 8
# Velocidad maxima para el spi 10 MHz
spi.max_speed_hz = 10000000
# Modo de transmision spi para el rf mode 0
spi.mode = 0
# variable para la direccion que se va leer en el nrf
address = 0x00

try:
	print("Address"," ","Contenido")

	while True:
		# transfer one byte y uno para recibir
		resp = spi.xfer2([address, 0x00])
		# Convertimos el valor recibido a hexadecimal
		resp1 = ByteToHex([resp[1]])
		#Mostramos lo que recibe y la direccion que enviamos
		print("%2d" % address, "      ", resp1)
		# sleep for 0.1 seconds
		time.sleep(0.1)
		# leemos el mapa de registro del nrf que tiene hasta la dirc 1x1D
		if (address > 0x1C):
			spi.close()
			break
		#end if
		# incrementamos  la direccion a leer
		address += 1
	# end while
except KeyboardInterrupt:
	spi.close()
# end try
