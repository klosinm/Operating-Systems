
#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <stdlib.h>

int main()
{
    pid_t pid;
    char *msg;
    FILE *infile;

// BEGIN BLOCK A
    if ((infile = fopen("message.txt", "r")) == NULL) {
        perror("could not open");
        exit(1);
    }
// END BLOCK A

    pid = fork();

    if (pid < 0) {
        perror("fork failed");
        exit(1);
    }

// BLOCK B GOES HERE

    if (pid == 0) {
        fscanf(infile, "%ms", &msg);
        printf("%s\n", msg);
        free(msg);
        exit(0);
    }

    wait(NULL);

    fscanf(infile, "%ms", &msg);
    printf("%s\n", msg);
    free(msg);

    fclose(infile);

    return 0;
}

