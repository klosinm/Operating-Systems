#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int i;
    char *fileCurrent[100];
    char *filePast[100];
    FILE *file_current = fopen("current.txt", "r");
    FILE *file_past = fopen("temp.txt", "r");

    //malloc space for two files
    for (i = 0; i < 100; ++i)
    {
        fileCurrent[i] = malloc(128); /* allocate a memory slot of 128 chars */
        fscanf(file_current, "%127s", fileCurrent[i]);
    }
    for (i = 0; i < 100; ++i)
    {
        filePast[i] = malloc(128); /* allocate a memory slot of 128 chars */
        fscanf(file_past, "%127s", filePast[i]);
    }

    for (i = 7; i < 100; ++i)
    {
       // printf("%i: \n", i);
        //printf("%s  : ", filePast[i]);
        //printf("%s \n", fileCurrent[i]);
        
    }

    int count = 0;
    for (i = 7; i < 100; ++i)
    {
        if (filePast[i] == '\t'){
            count++;
        }
    }
    printf("COUNT: %i \n", count);
    //Compare two files
    for (i = 7; i < 100; ++i){
        if (strcmp(fileCurrent[i], filePast[i]) != 0)
        {
            printf("%s ->", filePast[i]);
            printf(" %s \n", fileCurrent[i]);
        }
    }

    //for (i = 0; i < 100; ++i)
    //  free(fileCurrent[i]); /* remember to deallocated the memory allocated */
    // free(filePast[i]);

    return 0;
}