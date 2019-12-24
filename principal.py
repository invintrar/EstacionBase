#!/usr/bin/python3

import RPi.GPIO as gpio
import spidev
from time import sleep

# Create spi object
spi = spidev.SpiDev()
# Open spi port 0, device (CS) 0
spi.open(0,0)
spi.bits_per_word = 8
spi.max_speed_hz = 10000000
spi.mode = 0

gpio.setwarnings(False)
# Set mode: BOARD pines physical, BCM pines leveles
gpio.setmode(gpio.BOARD)

led = 7
ce = 15
irq = 16
bIntEx = 3
dataRec = [0,0,0,0,0,0,0,0]

gpio.setup(led, gpio.OUT, initial = gpio.LOW)
gpio.setup(ce,gpio.OUT, initial = gpio.LOW)
gpio.setup(irq, gpio.IN, pull_up_down = gpio.PUD_DOWN)

def configNrf():
	gpio.output(ce, gpio.LOW);

	#RX_ADDR_P0
	spi.xfer2([0x2A, 0x78, 0x78, 0x78, 0x78, 0x78])

	#TX_ADDR
	spi.xfer2([0x30,0x78, 0x78, 0x78, 0x78, 0x78])

	# EN_AA Habilite Auto Ack
	spi.xfer2([0x21, 0x01])

	#EN_RXADD active Pipe0
	spi.xfer2([0x22, 0x01])

	#SETUP_AW
	spi.xfer2([0x23, 0x03])

	#SETUP_RETR
	spi.xfer2([0x24, 0x1A])

	#RF_CH
	spi.xfer2([0x25, 0x0C])

	#RF_SETUP
	spi.xfer2([0x26,0x0E])

	#STATUS
	spi.xfer2([0x27, 0x70])

	#RX_PWP0
	spi.xfer2([0x31, 0x08])

	#CONFIG Colocamos en modo recepcion, y definimos CRC de 2 Bytes
	spi.xfer2([0x20, 0x0F])

	#tiempo para salir del modo stanby y entrar en modo recepcion
	sleep(2)
	gpio.output(ce, gpio.HIGH)
	sleep(0.15)

def sendData(data):
	ve = [0x00]
	gpio.output(ce, gpio.LOW)

	#STATUS
	spi.xfer2([0x27, 0x70])

	#W_TX_PAYLOAD
	ve[0] = 0xA0
	for x in data:
		ve.append(x)

	spi.xfer2(ve)

	#CONFIG Activo mode transmition
	spi.xfer2([0x20,0x0E])

	gpio.output(ce, gpio.HIGH)
	sleep(0.015)
	gpio.output(ce, gpio.LOW)


def getData():
	value = [0]

	value[0]=0x61

	for x in range(8):
		value.append(0)

	spi.xfer2(value)

	value = value[1:]
	return value


def intEx(channel):
	global dataRec
	global bIntEx

	status=spi.xfer2([0x07,00])

	if((status[1] & 0x20) == 0x20):
		bIntEx = 1

		print("Send Data")
		if((status[1] & 0x40)== 0x40):
			print("Ready Data")
			dataRec = getData()
			#TX_FLUS clearn of the buffer FIFO RX
			spi.xfer2([0xE2])
			for x in dataRec:
				print(x)

		#TX_FLUSH clean of the buffer FIFO TX
		spi.xfer2([0xE1])
		#STATUS CLEAR REGISTER
		spi.xfer2([0x27, 0x70])
		#CONFIG configuration RX mode
		spi.xfer2([0x20,0x0F])
		gpio.output(ce, gpio.HIGH)
		sleep(0.15)
		return
	elif((status[1] & 0x40) == 0x40):
		bIntEX = 2
		print("Ready Data")
		dataRec = getData()
		#TX_FLUS clearn of the buffer FIFO RX
		spi.xfer2([0xE2])
		#STATUS CLEAR REGISTER
		spi.xfer2([0x27,0x70])
		for x in dataRec:
			print(x)
		return
	elif((status[1] & 0x10)== 0x10 ):
		bIntEx = 3
		#TX_FLUSH CLEAR OF THE BUFFER FIFO TX
		spi.xfer2([0xE1])
		#STATUS CLEAR REGISTER
		spi.xfer2([0x27,0x70])
		print("Maximun Retransmission")
		return


def ByteToHex(Bytes):
	return ''.join(["0x%02X " % x for x in Bytes]).strip()

gpio.add_event_detect(irq,gpio.FALLING, callback = intEx, bouncetime = 300)

tog = 1;

configNrf()

try:
	while True:
		if(tog):
			gpio.output(led,gpio.HIGH)
			sleep(0.25);
			tog = 0;
		else:
			gpio.output(led, gpio.LOW)
			sleep(0.25)
			tog = 1;

		#resp=spi.xfer2([0x07, 0x00])

		#config
		#resp1 = spi.xfer2([0x00,0x00])

		#EN_RXADDR
		#resp2 = spi.xfer2([0x02,0x00])

		#RX_PW0
		#resp3 = spi.xfer2([0x0A,0x00])

		#print("0x07:%4s 0x00:%4s 0x02:%4s 0x0A:%4s" %
		#(ByteToHex([resp[1]]),
		#ByteToHex([resp1[1]]),
		#ByteToHex([resp2[1]]),
		#ByteToHex([resp3[1]])))

		data = [10,30,16,3,24,19,6,7]

		if(bIntEx == 3):
			sendData(data)

except KeyboardInterrupt:
	#gpio.output(led,gpio.LOW)
	spi.close()
	gpio.cleanup()

gpio.cleanup()
spi.close()
