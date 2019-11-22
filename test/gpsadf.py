#!/usr/bin/python3

import time
import adafruit_gps
import serial

# open serial port
uart = serial.Serial("/dev/ttyS0", baudrate=9600,timeout=30)

gps = adafruit_gps.GPS(uart, debug=False)

gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command(b'PMTK220,1000')

timestamp = time.monotonic()


try:
	while True:
		data = uart.read(32)
		#print(data)

		if data is not None:
			data_string = ''.join([chr(b) for b in data])
			print(data_string, end="")

		if time.monotonic() - timestamp > 5:
			# every 5 seconds..
			gps.send_command(b'PMTK605')
			timestamp = time.monotonic()

except KeyboardInterrupt:
	uart.close()

