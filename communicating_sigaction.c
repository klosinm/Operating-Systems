#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <signal.h>
#include <fcntl.h>
#include <sys/wait.h>

void sig_handler(int);

pid_t pid;  //global variable that stores the Process ID number

int main() {
    //install signal handler before fork so both parent and child will catch interrupts

    //struct to store sigaction arguments
    struct sigaction new_action;

    new_action.sa_handler = sig_handler; //set the new signal handler function to sig_handler(int sigNum)
    sigemptyset(&new_action.sa_mask); //default settings
    new_action.sa_flags = 0; //default settings
    sigaction(SIGINT, &new_action, NULL); //assign SIGINT to our new action handler for all processes

    //this code block spawns 2 child processes
    //parent spawns off child process
    if ((pid = fork()) < 0) {
        //error handling for fork failure
        perror("fork failure");
        exit(1);
    } else if (pid != 0) {
        //parent takes this branch
        printf("spawned child PID# %d\n", pid);

        //parent spawns off another child process
        if ((pid = fork()) < 0) {
            //error handling for fork failure
            perror("fork failure");
            exit(1);
        } else if (pid != 0) {
            //parent takes this branch
            printf("spawned child PID# %d\n", pid);
        }
    }

    //this code block implements signal handling for child and parent processes
    if (pid == 0) {
        //children take this branch
        while (1) {
            int random_time = rand() % 5 + 1; //get random time (1-5 seconds)
            sleep(random_time); //sleep for random time

            int random_signal = rand() % 2 + 1; //get random signal number(1 or 2)

            //send random signal to parent process
            if (random_signal == 1) {
                kill(getppid(), SIGUSR1);
            } else {
                kill(getppid(), SIGUSR2);
            }
        }
    } else {
        //parent takes this branch

        //assign SIGUSR1 and SIGUSR2 to the new action handler on the parent process
        sigaction(SIGUSR1, &new_action, NULL);
        sigaction(SIGUSR2, &new_action, NULL);

        //waits for signals
        while (1) {
            printf("wait...");
            fflush(stdout); //flush the standard output before calling pause()
            pause();
        }
    }
}


//function which handles SIGINT for all processes, and also handles
//SIGUSR1 and SIGUSR2 for the parent process.
void sig_handler(int sigNum) {
    if (sigNum == SIGUSR1)
        printf("\treceived a SIGUSR1 signal\n");
    else if (sigNum == SIGUSR2) {
        printf("\treceived a SIGUSR2 signal\n");
    } else if (sigNum == SIGINT) {
        if (pid != 0) {
            printf(" received. You have been gracefully shut down.\n");
        } else {
            printf("Child process %d shutting down.\n", getpid());
        }
        exit(0);
    }
}