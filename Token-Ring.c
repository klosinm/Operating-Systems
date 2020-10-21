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

#define MAX 1024

int main(int argc, char *argv[])
{
    char str[MAX]; //user input
    char *words[MAX]; //parsing user input
    int i = 0; //integer to help with parsing user input

    /**************************************
    * Get user input
    ***************************************/
    printf("Enter process ring lenth, process Word gets sent to, word: ");
    fgets(str, MAX, stdin);
   
    //parse user input
    char * ptr = strtok(str," ");
    while (ptr != NULL)
    {
        words[i] = ptr;
        //printf("input %i is: %s\n",i, words[i]);
        ptr = strtok(NULL, " ");
        i++;
    }
    int processEndVal = atoi(words[0]);  //end value of token ring
    int processWordGoesTo = atoi(words[1]); //token word is to go to
    char* wordOfDay = words[2];           //word that is being passed around
    
    //making sure values are set correctly
    if (processEndVal == 0 || processWordGoesTo == 0){
        printf("Please make sure all numerical values are numbers! \n");
        exit(1);
    }
    if(processWordGoesTo > processEndVal){
        printf("Please make the location word goes to less than how long the ring is!\n");
        exit(1);
    }
    
    //confirm choices (not like you can change them)
    printf("Token range 1 - %i, Word goes to token %i, Word is %s ", processEndVal, processWordGoesTo, wordOfDay);
    printf("________________________________________________________\n "); //aesthetics~

    /**************************************
    * Create x amount of pipes
    ***************************************/

    /*

    //create x amount of pipes
    int fd[2];
    pid_t childpid;

    pipe(fd);

    if ((childpid = fork()) == -1)
    {
        perror("fork");
        exit(1);
    }
    else{
        printf("Wooo pipe! %d\n", getpid());
    }

    */
}