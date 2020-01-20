#include <gtk/gtk.h>
#include <wiringPi.h>
#include <stdio.h>
#include "gps.h"

int serialPort;
dataGps data;

GtkWidget *lbTime ;
GtkWidget *lbDate ;
GtkWidget *lbLatitud ;
GtkWidget *lbLongitud ;

#define LED 7

int main(int argc, char *argv[])
{
    GtkBuilder      *builder; 
    GtkWidget       *window;
    wiringPiSetup();
  	
	if(initSerial())
  	{
  		printf("Error Setup Serial\n");
  	}


    pinMode(LED,OUTPUT);

	
    gtk_init(&argc, &argv);

    builder = gtk_builder_new();
    gtk_builder_add_from_file (builder, "datagps.glade", NULL);

    window = GTK_WIDGET(gtk_builder_get_object(builder, "window"));
    gtk_builder_connect_signals(builder, NULL);
	lbTime = GTK_WIDGET(gtk_builder_get_object(builder, "lbTime"));
	lbDate = GTK_WIDGET(gtk_builder_get_object(builder, "lbDate"));
	lbLatitud = GTK_WIDGET(gtk_builder_get_object(builder, "lbLatitud"));
	lbLongitud = GTK_WIDGET(gtk_builder_get_object(builder, "lbLongitud"));

    g_object_unref(builder);

    gtk_widget_show(window);                

    gtk_main();
    return 0;
}

// called when window is closed
void on_window_destroy()
{
    gtk_main_quit();
}

void on_led(GtkWidget *wid, gpointer ptr)
{
	digitalWrite(LED,HIGH);
	}

void off_led(GtkWidget *wid, gpointer ptr)
{
	digitalWrite(LED,LOW);
}
void getGps(){
	char buffer[10];

	data = getDataGps();

 	sprintf(buffer, "%d:%d:%d", data.hour, data.minute, data.second);
	gtk_label_set_text(GTK_LABEL(lbTime), buffer);

	sprintf(buffer, "%d/%d/%d", data.month, data.day, data.year);
	gtk_label_set_text(GTK_LABEL(lbDate), buffer);
	
	sprintf(buffer, "%d%s%d%c%d%c %c", data.gradosLatitud, "°", data.minutosLatitud, 39, 
 	data.segundosLatitud, 34, data.latitud);
	gtk_label_set_text(GTK_LABEL(lbLatitud), buffer);

 	sprintf(buffer, "%d%s%d%c%d%c %c", data.gradosLongitud, "°", data.minutosLongitud, 39, 
	data.segundosLongitud, 34, data.longitud);
	gtk_label_set_text(GTK_LABEL(lbLongitud), buffer);
 

}

//Fin File
