all:
	gcc -o output main.c gps.c -lm -lwiringPi -Wall  `pkg-config --cflags --libs gtk+-3.0` -export-dynamic 
	./output
	rm output
