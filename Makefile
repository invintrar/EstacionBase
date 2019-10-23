all:
	gcc `pkg-config --cflags --libs gtk+-2.0` guiMain.c -o guitt
	./guitt
	rm guitt
