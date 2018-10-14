#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>

#define PATH_TO_TARGET "/home/input2/input"

int main() {
    // Stage 1
    // handle argv
    char* argv[101];
    for (int i = 0; i < 100; ++i)
        argv[i] = PATH_TO_TARGET;
    argv['A'] = "\x00";
    argv['B'] = "\x20\x0a\x0d";
    argv['C'] = "33333";
    argv[100] = NULL;

    // Stage 3
    // handle envp
    char* envp[2];
    envp[0] = "\xde\xad\xbe\xef=\xca\xfe\xba\xbe";
    envp[1] = NULL;

    // Stage 4
    // handle file
    FILE* hFile = fopen("\x0a", "w");
    if (hFile == NULL) {
        printf("Failed to create file.\n");
        exit(0);
    }
    fwrite("\x00\x00\x00\x00", 4, 1, hFile);
    fclose(hFile);

    // Stage 2
    // handle stdin
    pid_t child_pid;
    int pipe_stdin[2];
    int pipe_stderr[2];
    if (pipe(pipe_stdin) == -1 || pipe(pipe_stderr) == -1) {
        printf("Failed to create pipe.\n");
        exit(0);
    }
#define STDIN_READ   pipe_stdin[0]
#define STDIN_WRITE  pipe_stdin[1]
#define STDERR_READ  pipe_stderr[0]
#define STDERR_WRITE pipe_stderr[1]
    child_pid = fork();
    if (child_pid == -1) {
        printf("Failed to fork.\n");
        exit(0);
    } else if (child_pid == 0) {
        dup2(STDIN_READ, 0);
        dup2(STDERR_READ, 2);
        execve(PATH_TO_TARGET, argv, envp);
        exit(0);
    } else {
        write(STDIN_WRITE, "\x00\x0a\x00\xff", 4);
        write(STDERR_WRITE, "\x00\x0a\x02\xff", 4);
    }

    // Stage 5
    // handle network
    sleep(1);
    int sock;
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(33333);
    addr.sin_addr.s_addr = inet_addr("127.0.0.1");
    sock = socket(AF_INET, SOCK_STREAM, 0);
    connect(sock, (struct sockaddr*)&addr, sizeof(addr));
    send(sock, "\xde\xad\xbe\xef", 4, 0);
    close(sock);
    sleep(1);

    return 0;
}
