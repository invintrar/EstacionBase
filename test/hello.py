#!/usr/bin/python3

def hello():
	data = b'$GPRMC,N,13,53,23\r\n'
	data1 = data.decode()
	if (data1[:6] == "$GPRMC"):
		print("Comparado")
	else:
		print("NO se compara")

hello()
