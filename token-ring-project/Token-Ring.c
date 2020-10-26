/*
A program that communicates multiple processes 
to emulate a form of network communication.

name: Monica Klosin
date: October 18, 2020

in Makefile:
run:
    ./a.out 

to run:
make
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/wait.h>

#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>
#include <stdio.h>
#include <unistd.h>

#define MAX 1024
#define READ 0
#define WRITE 1

void endSig(int);    //ctrl c handler
typedef int Pipe[2]; //Pipe array

int main(int argc, char *argv[])
{
    int parent_pid = getpid(); //parent ID
    char userWord[MAX];          //user word input
    char ProcessLen[MAX];        //how long the ring process is
    char ProcessWordGoesTo[MAX]; //which process is to recieve word
    char readMessage[MAX];  //reading input from write
    int processNum = 1; //keep track of the process

    /**************************************
    * Get user input
    ***************************************/
    //get message from user
    printf("What is message? ");
    fgets(userWord, MAX, stdin);
    //get how long the token ring circle should be
    printf("How many Processes? ");
    fgets(ProcessLen, MAX, stdin);
    int numProcess = atoi(ProcessLen) + 1;
    //get which process the message needs to go to
    printf("Where does message go? ");
    fgets(ProcessWordGoesTo, MAX, stdin);
    int ProcessDelivery = atoi(ProcessWordGoesTo);

    //Test user input
    if (ProcessDelivery == 0 || numProcess == 0)
    {
        printf("Please make sure all numerical values are numbers! \n");
        exit(1);
    }
    if (ProcessDelivery > (numProcess - 1))
    {
        printf("Please make the location word goes to less than how long the ring is!\n");
        exit(1);
    }
   
    //indicate the parent ID
    printf("Parent = %d\n", parent_pid);

    // Create pipes array. 
    Pipe pipes[numProcess + 1];

    // child id
    int pid;

    /**************************************
    * Create children and pipes
    ***************************************/
    for (int n = 0; n < numProcess + 1; n++)
    {
        /** make pipe **/
        if (pipe(pipes[n]) < 0)
        {
            perror("Error creating pipe\n");
            exit(1);
        }

        /** make child **/
        if ((pid = fork()) == 0){
            /*
            have to create mutiple pipes and link them to create token ring!
            so pipe 0 exists to all children
            */

            //opening and closing and duplicating files? Magic?
            for (int x = 0; x < numProcess + 1; x++)
            {
                // Close write of pipe.
                close(pipes[x][WRITE]);
                // Close read of pipe.
                close(pipes[x][READ]);
            }
            // Close the write pipe the last process.
            close(pipes[n - 1][WRITE]);
            // Close the read pipe of the current process.
            close(pipes[n][READ]);

            //once child is created, break out of for loop to go to while loop to read/write
            break;
        }
        else
        {
            /**  parent process  **/

            //opening and closing and duplicating files? Magic?
            for (int i = 1; i < numProcess; i++)
            {
                // Close write of pipe.
                close(pipes[i][WRITE]);
                // Close read of pipe.
                close(pipes[i][READ]);
            }

            // Close read of the first pipe.
            close(pipes[0][READ]);
            // Close write of the last pipe.
            close(pipes[numProcess][WRITE]);

            /*indexing for child value, called it processNum but  
             it is the childProcess value*/
            processNum = n + 1;
        }
    }

    //loop through pipes with message
    while (1)
    {
        //initial child
        if (processNum == 1)
        {
            printf("---------------------------------------\n");
            //printf("INITIAL Process %i (%d)-(PPID: %d) \n", processNum, getpid(), getppid());
            write(pipes[processNum - 1][WRITE], userWord, sizeof(userWord));
            printf("INITIAL Process %i (%d)-(PPID: %d) write message: %s\n", processNum, getpid(), getppid(), userWord);
        }
        /*find child that the message word is supposed to be delievered to
        once found, write "done!" in token vs the user input, and have "done!" read
        for the rest of the program. */
        else if (processNum == ProcessDelivery)
        {
            read(pipes[processNum - 1][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) DELIEVERY! read message: %s \n", processNum, getpid(), getppid(), readMessage);
            write(pipes[processNum - 1][WRITE], "done!", sizeof("done!"));
            printf("Process %i (%d)-(PPID:%d) write message: %s\n", processNum, getpid(), getppid(), "done!");
   
        }
        //other child processes
        else if (processNum < (numProcess ))
        {
            read(pipes[processNum - 1][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) read message: %s \n", processNum, getpid(), getppid(), readMessage);
            write(pipes[processNum - 1][WRITE], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) write message: %s\n", processNum, getpid(), getppid(), readMessage);
            // close(p1[1]);
        }
        //format output to have space between processes
        printf(" \n");

        //to not get infinite loop
        break;
    }

    /*
    End of program! 
    The program did not end well, it does not work as Monica hoped it would. 
    (Not for grade, but i'd like to ask you how to make this work, because its a head-scratcher.)
    */
    exit(0);
}