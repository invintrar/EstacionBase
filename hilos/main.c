#include <stdio.h>
#include<stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <string.h>
#include <unistd.h>

typedef struct dato
{
	char *cadena;
	int x,y;
}parametro;

void gotoxy(int x, int y){
	printf("\033[%d;%df", y, x);
}

void *saludo(void *args){
	char *cadena =(char *) args ;
	for (i=0;i < strlen(cadena); i++){
		fflush(stdout);
		gotoxy(x,y);
		x++;
		printf("%c", cadena[i]);
		sleep(1);
	}


int main(int argc, char const *argv[])
{
	pthread_t hilo1, hilo2;
	parametro p1;
	p1.cadena = "hola";
	p1.x = 10;
	p1.y = 20;
	pthread_create(&hilo1,NULL,saludo ,(void *)&p1);
	pthread_join(hilo1,NULL);
	return 0;
}
