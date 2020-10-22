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
#include<stdio.h>
#include<unistd.h>


#define MAX 1024


void endSig(int); //ctrl c handler
typedef int Pipe[2]; //Pipe array

int main(int argc, char *argv[])
{
    int c1_wr;
    int parent_pid = getpid();
    int p1[2];
   // int p2[2];

    char userWord[MAX];    //user word input
    char ProcessLen[MAX];  //how long the ring process is
    char ProcessWordGoesTo[MAX];  //which process is to recieve word
    char readMessage[MAX];
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
    int numProcess = atoi(ProcessLen);
    //get which process the message needs to go to
    printf("Where does message go? ");
    fgets(ProcessWordGoesTo, MAX, stdin);
    int ProcessDelivery= atoi(ProcessWordGoesTo);

    //Test input
    if (ProcessDelivery == 0 || numProcess == 0)
    {
        printf("Please make sure all numerical values are numbers! \n");
        exit(1);
    }
    if (ProcessDelivery > numProcess)
    {
        printf("Please make the location word goes to less than how long the ring is!\n");
        exit(1);
    }

    
    c1_wr = dup(p1[1]);
    printf("%d children\n", numProcess);
    printf("Parent = %d\n", parent_pid);

    // Create pipes array.
    Pipe pipes[numProcess + 1];

    /**************************************
    * Create x amount of children
    ***************************************/
    int pid;
    for (int n = 0; n < numProcess ; n++)
    {
        //create a pipe
        if (pipe(pipes[n]) < 0)
        {
            perror("Error creating pipe\n");
            exit(1);
        }
        //if child
        if ((pid = fork()) == 0)
        {
         // printf("Process %2d (%d)-(PPID: %d) \n", n + 1, getpid(), getppid());
            /* Child process closes up input side of pipe */
         //first child has access to pipe 0
         //2nd child has access to pipe 1, pipe 0 doesnt exist to 2nd
         dup(p1[0]);

         close(pipes[n][0]);

         break;
        }
        else{
            processNum = n + 2;
           // printf("processNum %2d \n", processNum);
            /* Parent process closes up output side of pipe */
           // close(p1[1]);
        }

      /*  close(p1[0]);
        close(p1[1]);
        p1[0] = p2[0];
        p1[1] = p2[1];*/
    }
    while (1)
    {
        //initial child
        if (processNum == 1)
        {
            printf("---------------------------------------\n");
            printf("INITIAL Process %i (%d)-(PPID: %d) \n", processNum, getpid(), getppid());
            write(p1[1], userWord, sizeof(userWord));
            printf("initial write message: %s\n", userWord);
            close(p1[1]);
        }
        //check if its process message is to be delievered too
        else if (processNum == ProcessDelivery){
            printf("Process %i (%d)-(PPID: %d) GOT MESSAGE!\n", processNum, getpid(), getppid());
            read(p1[0], readMessage, sizeof(readMessage));
            printf("read message: %s\n", readMessage);
            write(p1[1], "done!", sizeof("done!"));
            printf("write message: %s\n", "done!");
        }
        else if (processNum < numProcess){
                printf("Process %i (%d)-(PPID: %d) \n", processNum, getpid(), getppid());

                read(p1[0], readMessage, sizeof(readMessage));
                printf("read message: %s\n", readMessage);
                write(p1[1], readMessage, sizeof(readMessage));
                printf("write message: %s\n", readMessage);
                // close(p1[1]);
            }

        
        break;
    }
           
        
    

/*
while(1){
    for (int processNum = 1; processNum < numProcess+1; processNum++)
    {
        //inital process
        if (processNum == 1)
        {

            printf("---------------------------------------\n");
            printf("INITIAL Process %i (%d)-(PPID: %d) \n", processNum, getpid(), getppid());
            write(p1[1], userWord, sizeof(userWord));
            printf("write message: %s\n", userWord);
        }
        else 
        {
            printf("Process %i (%d)-(PPID: %d) \n", processNum, getpid(), getppid());
            read(p1[0], readMessage, sizeof(readMessage));
            printf("read message: %s\n", readMessage);
            write(p1[1], userWord, sizeof(userWord));
            printf("write message: %s\n", userWord);
           
        }
       // break;
    }
}
*/
    exit(0);
    /*
       //check if first process, to just write
       if (processNum == 1)
       {
           write(p1[1], userWord, sizeof(userWord));
           printf("write message: %s\n", userWord);
        }
        //check if we are at process that needs word
        else if (processNum == ProcessDelivery){
            read(p1[0], readMessage, sizeof(readMessage));
            printf("read message: %s\n", readMessage);
            write(p1[1], "recieved!", sizeof("recieved!"));
            printf("write message: %s\n", "recieved!");
            break;
        }
        else{
            read(p1[0], readMessage, sizeof(readMessage));
            printf("read message: %s\n", readMessage);
            write(p1[1], userWord, sizeof(userWord));
            printf("write message: %s\n", userWord);
        }
        printf("---------------------------------------\n");
        //wait();
        break;
        */
    //look at X Process, which needs to read from pipe and write to output pipe

    /*if ((pid = fork()) == 0)
        {
            read(p1[0], readMessage, sizeof(readMessage));
          //  printf("Process %2d (%d)- Reading from pipe -(PPID: %d): %s \n", n+1, getppid(), getpid(), readMessage);
           }
        else
        { //Parent process

          //  printf("  Process %2d (%d)- writing from pipe -(PPID: %d): %s \n", n+1, getppid(), getpid(), userWord);
            write(p2[1], userWord, sizeof(userWord));
      
        }*/

    //printf("Child %2d = %d\n", n + 1, pid);
    // printf("p1[0] %d, p2[1] %d: ", p1[0], p2[1]);
    
}
/*
//ends on ctrl c
void endSig(int sigNum)
{
    if (pid != 0)
    {
        printf("^C received. Process %d shutting down.\n", getpid());
        //free(data);
    }
    exit(0);

}
*/