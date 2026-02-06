#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid;

    pid = fork();   // create child process

    if (pid < 0) {
        // fork failed
        perror("fork failed");
        exit(1);
    }

    else if (pid == 0) {
        // Child process
        printf("Child process (PID: %d)\n", getpid());
        execl("/bin/sleep", "sleep", "30", NULL);

        // execlp only returns if there is an error
        perror("exec failed");
        exit(1);
    }
    else {
        // Parent process
        printf("Parent process (PID: %d), waiting for child...\n", getpid());
        wait(NULL);
        printf("Child process finished.\n");
    }

    return 0;
}
