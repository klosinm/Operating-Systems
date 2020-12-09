/* taking inputs in argv[1]
 * -i - inode number
 * -n - group ids
 * none 
*/
#include <dirent.h>
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <errno.h>
#include <string.h>
#define MAX 75

char **sortoutput(char *names[], int count);

int main(int argc, char *argv[])
{
    printf("\n");
    struct stat statPath;
    char **names = malloc(MAX * sizeof(char *));

    for (int i = 0; i != MAX; i++)
    {
        names[i] = malloc(MAX * sizeof(char));
    }

    int count = 0;
    if (argc < 3)
    {
        DIR *dirPtr;
        struct dirent *entryPtr;
        dirPtr = opendir(".");
        char date[80];
        int type;
        while ((entryPtr = readdir(dirPtr)))
        {
            if (stat(entryPtr->d_name, &statPath) < 0)
            {
                perror("cannot read");
                exit(1);
            }
            names[count] = entryPtr->d_name;
            count += 1;
        }

        names = sortoutput(names, count);
        printf("Permissions H.Links   Size  Last Modify   Name\n");
        printf("----------------------------------------------\n");

        for (int i = 1; i <= count; i++)
        {
            if (stat(names[i], &statPath) < 0)
            {
                perror("cannot read");
                exit(1);
            }
            time_t temp = statPath.st_mtime;
            struct tm lt;
            localtime_r(&temp, &lt);
            strftime(date, sizeof date, "%b %d %H:%M", &lt);
            if (S_ISDIR(statPath.st_mode))
                type = 2;
            else if (S_ISREG(statPath.st_mode))
                type = 1;
            else
                type = 0;

            printf((S_ISDIR(statPath.st_mode)) ? "d" : "-");
            printf((statPath.st_mode & S_IRUSR) ? "r" : "-");
            printf((statPath.st_mode & S_IWUSR) ? "w" : "-");
            printf((statPath.st_mode & S_IXUSR) ? "x" : "-");
            printf((statPath.st_mode & S_IRGRP) ? "r" : "-");
            printf((statPath.st_mode & S_IWGRP) ? "w" : "-");
            printf((statPath.st_mode & S_IXGRP) ? "x" : "-");
            printf((statPath.st_mode & S_IROTH) ? "r" : "-");
            printf((statPath.st_mode & S_IWOTH) ? "w" : "-");
            printf((statPath.st_mode & S_IXOTH) ? "x" : "-");
            printf("     ");

            //permission, type, owner, groups, size, creation time, name
            printf("%-4d %5luB  %-13s %s\n",
                   type,
                   statPath.st_size,
                   date,
                   names[i]);
        }

        closedir(dirPtr);
    }
    else
    {
        if (stat(argv[2], &statPath) < 0)
        {
            perror("cannot read");
            exit(1);
        }
        char date[80];
        int type;
        time_t temp = statPath.st_mtime;
        struct tm lt;
        localtime_r(&temp, &lt);
        strftime(date, sizeof date, "%b %d %H:%M", &lt);
        if (S_ISDIR(statPath.st_mode))
            type = 2;
        else if (S_ISREG(statPath.st_mode))
            type = 1;
        else
            type = 0;
        //permission, type, owner, groups, size, creation time, name
        printf("%u %-1d %-5u %-5u %6lu %-12s %s\n",
               statPath.st_mode,
               type,
               statPath.st_uid,
               statPath.st_gid,
               statPath.st_size,
               date,
               argv[2]);
    }
}

char **sortoutput(char *names[], int count)
{
    char temp[MAX];
    for (int i = 0; i <= count; i++)
    {
        for (int j = i + 1; j <= count; j++)
        {
            if (strcmp(names[i], names[j]) > 0)
            {
                strcpy(temp, names[i]);
                strcpy(names[i], names[j]);
                strcpy(names[j], temp);
            }
        }
    }
    return names;
}
