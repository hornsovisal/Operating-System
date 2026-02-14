#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

DWORD Sum = 0; /* data is shared by the thread(s) */

/* The thread will execute in this function */
DWORD WINAPI Summation(LPVOID Param)
{
    DWORD Upper = *(DWORD*)Param;
    
    printf("Thread started - calculating sum from 1 to %lu...\n", Upper);
    
    for (DWORD i = 1; i <= Upper; i++) {
        Sum += i;
        Sleep(100); // Add delay in each iteration (100ms)
    }
    
    printf("Thread completed calculation.\n");
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("Usage: %s <number>\n", argv[0]);
        return 1;
    }

    DWORD ThreadId;
    HANDLE ThreadHandle;
    DWORD Param;

    Param = (DWORD)atoi(argv[1]);
    
    /* create the thread */
    Sleep(5000); // Initial delay before starting the thread
    printf("Main: Creating thread to calculate sum...\n");
    ThreadHandle = CreateThread(
        NULL,                   /* default security attributes */
        0,                      /* default stack size */
        Summation,              /* thread function */
        &Param,                /* parameter to thread function */
        0,                      /* default creation flags */
        &ThreadId);            /* returns the thread identifier */

    if (ThreadHandle == NULL) {
        fprintf(stderr, "Error creating thread: %d\n", GetLastError());
        return 1;
    }


    printf("Main: Created thread with ID: %lu\n", ThreadId);
    printf("Main: Waiting for thread to complete...\n");

    /* now wait for the thread to finish */
    WaitForSingleObject(ThreadHandle, INFINITE);

    /* close the thread handle */
    CloseHandle(ThreadHandle);

    printf("Main: Final sum = %lu\n", Sum);
    printf("Main: Press Enter to exit...\n");
    getchar(); // Keep console open longer

    return 0;
}
