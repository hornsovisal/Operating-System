#include <unistd.h>     // read(), write(), close()
#include <fcntl.h>      // open()
#include <sys/stat.h>   // file permission macros
#include <errno.h>

#define BUFFER_SIZE 1024

int main() {
    int src_fd, dst_fd;
    char buffer[BUFFER_SIZE];
    ssize_t bytesRead;

    /* Open source file */
    src_fd = open("result.txt", O_RDONLY);
    if (src_fd < 0) {
        write(2, "Error: Cannot open result.txt\n", 30);
        return 1;
    }

    /* Create destination file */
    dst_fd = open("copyresult.txt",
                  O_WRONLY | O_CREAT | O_TRUNC,
                  0644);
    if (dst_fd < 0) {
        write(2, "Error: Cannot create copyresult.txt\n", 37);
        close(src_fd);
        return 1;
    }

    /* Copy file content */
    while ((bytesRead = read(src_fd, buffer, BUFFER_SIZE)) > 0) {
        write(dst_fd, buffer, bytesRead);
    }

    /* Close files */
    close(src_fd);
    close(dst_fd);

    return 0;
}
