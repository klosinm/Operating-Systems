/*
A program that communicates multiple processes 
to emulate a form of network communication.

name: Monica Klosin
date: October 18, 2020

in makeBFile:
gcc -Wall token-ring-complete.c -o b.out
./b.out 

to run:
./makeBFile
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
#include <sys/types.h>
#include <signal.h>


#define MAX 1024

#define READ 0
#define WRITE 1

void endSig(int);    //ctrl c handler
typedef int Pipe[2]; //Pipe array
void endSig(int);
//to ^C out of program.

int main(int argc, char *argv[])
{

    signal(SIGINT, endSig); //signal handler
    int parent_pid = getpid(); //parent ID
    //int p1[2]; //pipe process 2

    char userWord[MAX];          //user word input
    char ProcessLen[MAX];        //how long the ring process is
    char ProcessWordGoesTo[MAX]; //which process is to recieve word
    char readMessage[MAX];       //reading input from write
    int processNum = 1;          //keep track of the process

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
    if (ProcessDelivery > (numProcess-1))
    {
        printf("Please make the location word goes to less than how long the ring is!\n");
        exit(1);
    }

    //copying user message to message going through pipes
    strcpy(readMessage, userWord);

    //indicate the parent ID
    printf("Parent = %d\n", parent_pid);

    // Create pipes array.
    Pipe pipes[numProcess + 1];

    // child id
    int pid;

    /**************************************
    * Create pipes
    ***************************************/

    for (int n = 0; n <= numProcess - 2; n++)
    {
        /** make pipe **/
        if (pipe(pipes[n]) < 0)
        {
            perror("Error creating pipe\n");
            exit(1);
        }
    }

    /**************************************
    * Create children 
    ***************************************/

    for (int n = 0; n < numProcess - 2; n++)
    {
        /** make child **/
        if ((pid = fork()) == 0)
        {        
            //once child is created, break out of for loop to go to while loop to read/write
            break;
        }
        else
        {
            /**  parent process  **/
            /*indexing for child value, called it processNum but in 
            actualitiy it is the childProcess value*/
            processNum = n + 2;
        }
    }

    while (1)
    {
        //initial child
        if (processNum == 1)
        {
            printf("---------------------------------------\n");
            write(pipes[1][WRITE], readMessage, sizeof(readMessage));
            printf("INITIAL Process %i (%d)-(PPID: %d) write message: %s\n", processNum, getpid(), getppid(), readMessage);
            read(pipes[0][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) read message: %s \n", processNum, getpid(), getppid(), readMessage);
        }
        /*find child that the message word is supposed to be delievered to
        once found, write "done!" in token vs the user input, and have "done!" read
        for the rest of the program. */
        else if (processNum == ProcessDelivery)
        {
            read(pipes[processNum - 1][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) DELIEVERY! read message: %s \n", processNum, getpid(), getppid(), readMessage);
            write(pipes[processNum][WRITE], "done!", sizeof("done!"));
            printf("Process %i (%d)-(PPID:%d) write message: %s\n", processNum, getpid(), getppid(), "done!");
        }
        //other child processes
        else if (processNum < (numProcess - 1))
        {
            read(pipes[processNum - 1][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) read message: %s \n", processNum, getpid(), getppid(), readMessage);
            write(pipes[processNum][WRITE], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) write message: %s\n", processNum, getpid(), getppid(), readMessage);
        }
        //last process
        else if (processNum == (numProcess - 1))
        {
            read(pipes[processNum - 1][READ], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) read message: %s \n", processNum, getpid(), getppid(), readMessage);
            write(pipes[0][WRITE], readMessage, sizeof(readMessage));
            printf("Process %i (%d)-(PPID:%d) write message: %s\n", processNum, getpid(), getppid(), readMessage);           
        }

        //format output to have space between processes
        printf(" \n");
        // for dramatic effect
        sleep(1);
    }

}

//ends on ^C
void endSig(int sigNum)
{
    sleep(1);
    //destroy child process
    kill(getpid(), SIGINT);
    printf("\r ^C recieved. Process %d shutting down.\n", getpid());
    exit(0);   
}

/*
    End of program! 
*/
