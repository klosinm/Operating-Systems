
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <fcntl.h>

//ctrl c handler
void endSig(int);

//user handler function
void userSig1(int);
void userSig2(int);

pid_t pid; //global variable PID

int main()
{
    //ctrl c handler
    signal(SIGINT, endSig);

    //spawn child
    pid = fork();

    if (pid < 0)
    {
        perror("fork failure");
        exit(1);
    }

    else if (pid == 0)
    {

        while (1)
        {

            //sleep for a random time (1-5 secs)
            int sleepTime = rand() % 5 + 1;
            sleep(sleepTime);

            //random generate signal
            int signalNum = rand() % 2 + 1;
            if (signalNum == 1)
            {
                //send sig1 to parent
                kill(getppid(), SIGUSR1);
            }
            else
            {
                //send sig2 to parent
                kill(getppid(), SIGUSR2);
            }
        }
    }
    else
    {
        pid = fork();

        //add an error check

        if (pid == 0)
        {
            while (1)
            {
                int sleepTime = rand() % 5 + 1;
                sleep(sleepTime);
                int signalNum = rand() % 2 + 1;
                if (signalNum == 1)
                {
                    kill(getpid(), SIGUSR1);
                }
                else
                {
                    kill(getpid(), SIGUSR2);
                }
            }
        }
        else
        {
            printf("spawned child PID# %d\n", pid);

            //singal handlers
            signal(SIGUSR1, userSig1);
            signal(SIGUSR2, userSig2);

            //waiting and printing and all that
            while (1)
            {
                printf("waiting...\t");
                fflush(stdout);
                pause();
            }
        }
    }

    return 0;
}

void userSig1(int sigNum)
{
    signal(SIGUSR1, userSig1);
    printf("recieved a SIGUSR1 signal PID: %d\n", pid);
}

void userSig2(int sigNum)
{
    signal(SIGUSR2, userSig2);
    printf("recieved a SIGUSR2 signal PID: %d\n", pid);
}

void endSig(int sigNum)
{
    if (pid != 0)
    {
        printf(" received. I need more creative exit ideas.\n");
    }
    exit(0);
}