/*
A program that communicates multiple processes 
to emulate a form of network communication.

name: Monica Klosin
date: October 18, 2020

compile: gcc -Wall Token-Ring.c -o a.out
run: ./a.out 1 [num value of how big you want ring communicaiton]

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>

int line[100]; //array for input
char **comms;   //storage of the arguments

int main(int argc, char *argv[])
{

    int processStartVal = atoi(argv[1]); //start value for token ring, always 1
    int processEndVal = atoi(argv[2]); //end value of token ring
    char wordOfDay = *argv[3]; //word that is being passed around
    int processWordGoesTo = atoi(argv[4]); //process value that word goes to

    //making sure values are set correctly
    if (processStartVal != 1)
    {
        printf("Please make your start process value 1! \n");
        exit(1);
    }
    if (processEndVal == 0 || processWordGoesTo == 0){
        printf("Please make sure all numerical values are numbers! \n");
        exit(1);
    }

        printf(" Token range %i - %i, Word  %c, Word goes to token %i: \n ", processStartVal, processEndVal, wordOfDay, processWordGoesTo);
        printf("________________________________________________________\n "); //aesthetics~
}