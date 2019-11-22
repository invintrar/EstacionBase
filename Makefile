all:
	gcc `pkg-config --cflags --libs gtk+-3.0` -lwiringPi guiMain.c -o guitt
	./guitt
	rm guitt
