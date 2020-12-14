#include <dirent.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <string.h>
#define MAX 75
#define _XOPEN_SOURCE 700

void compare();

int main(int argc, char *argv[])
{

    // opening both file in read only mode
    FILE *f1 = fopen("temp.txt", "r");
    FILE *f2 = fopen("current.txt", "r");

    if (f1 == NULL || f2 == NULL)
    {
        printf("Error : Files not open\n");

        exit(0);
    }


    char file1 = getc(fopen("temp.txt", "r"));
    char file2 = getc(fopen("current.txt", "r"));



    // error keeps track of number of errors
    // pos keeps track of position of errors
    // line keeps track of error line
    int error = 0, pos = 0, line = 1, word = 0;

    // iterate loop till end of file
    while (file1 != EOF && file2 != EOF)
    {
        pos++;

        // if both variable encounters new
        // line then line variable is incremented
        // and pos variable is set to 0
        if (file1 == '\n' && file2 == '\n')
        {
            line++;
            pos = 0;
            //printf("\n");
        }

        if (file1 == ' ')
        {
            word++;
           // printf(" ");
            //printf(": word # %i\n", word);
        }
        else{
       
            //printf("%c", file1);
         
        }

        // if fetched data is not equal then
        // error is incremented

        if (file1 != file2)
        {
            error++;
            printf("%c ", file1);
            printf("%c", file2);
            printf("Line Number : %d \tDifferences Position : %d \n",line, pos);
        }

        // fetching character until end of file
        file1 = getc(f1);
        file2 = getc(f2);
    }

 
   printf("\nTotal Differences : %d\t\n", error);
    
}
