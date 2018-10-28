# pwnable.kr -- Toddler's Bottle -- input

## 1. Challenge

```
Mom? how can I pass my input to a computer program?

ssh input2@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Log in via SSH and you will see 3 files: `flag`, `input` and `input.c`. Of course you cannot use `cat flag` to see the content of file `flag`. Let's see the source code of file `input` first:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int main(int argc, char* argv[], char* envp[]){
        printf("Welcome to pwnable.kr\n");
        printf("Let's see if you know how to give input to program\n");
        printf("Just give me correct inputs then you will get the flag :)\n");

        // argv
        if(argc != 100) return 0;
        if(strcmp(argv['A'],"\x00")) return 0;
        if(strcmp(argv['B'],"\x20\x0a\x0d")) return 0;
        printf("Stage 1 clear!\n");

        // stdio
        char buf[4];
        read(0, buf, 4);
        if(memcmp(buf, "\x00\x0a\x00\xff", 4)) return 0;
        read(2, buf, 4);
        if(memcmp(buf, "\x00\x0a\x02\xff", 4)) return 0;
        printf("Stage 2 clear!\n");

        // env
        if(strcmp("\xca\xfe\xba\xbe", getenv("\xde\xad\xbe\xef"))) return 0;
        printf("Stage 3 clear!\n");

        // file
        FILE* fp = fopen("\x0a", "r");
        if(!fp) return 0;
        if( fread(buf, 4, 1, fp)!=1 ) return 0;
        if( memcmp(buf, "\x00\x00\x00\x00", 4) ) return 0;
        fclose(fp);
        printf("Stage 4 clear!\n");

        // network
        int sd, cd;
        struct sockaddr_in saddr, caddr;
        sd = socket(AF_INET, SOCK_STREAM, 0);
        if(sd == -1){
                printf("socket error, tell admin\n");
                return 0;
        }
        saddr.sin_family = AF_INET;
        saddr.sin_addr.s_addr = INADDR_ANY;
        saddr.sin_port = htons( atoi(argv['C']) );
        if(bind(sd, (struct sockaddr*)&saddr, sizeof(saddr)) < 0){
                printf("bind error, use another port\n");
                return 1;
        }
        listen(sd, 1);
        int c = sizeof(struct sockaddr_in);
        cd = accept(sd, (struct sockaddr *)&caddr, (socklen_t*)&c);
        if(cd < 0){
                printf("accept error, tell admin\n");
                return 0;
        }
        if( recv(cd, buf, 4, 0) != 4 ) return 0;
        if(memcmp(buf, "\xde\xad\xbe\xef", 4)) return 0;
        printf("Stage 5 clear!\n");

        // here's your flag
        system("/bin/cat flag");
        return 0;
}
```

It seems we have to pass these 5 stages. Let's solve them one by one.

### Stage 1

This stage is about `argv`. You can use `execve` to pass 100 arguments. 

```c
char* argv[101];
for (int i = 0; i < 100; ++i)
    argv[i] = "/home/input2/input";
argv['A'] = "\x00";
argv['B'] = "\x20\x0a\x0d";
argv[100] = NULL;
execve("/home/input2/input", argv, NULL);
```

### Stage 2

This stage is about redirecting `stdin` and `stderr`. 

We know that child process will inherit `stdin`, `stdout` and `stderr` file descriptors of parent process. So we can first create two anonymous pipes which stand for `stdin` and `stderr` respectively, then fork a child process and replace child process' `stdin` and `stderr` by the two pipes. After the child process lanuch `/home/input2/input`, the `stdin` and `stderr` of `/home/input2/input` will have been redirected.

```c
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
    execve("/home/input2/input", argv, envp);
    exit(0);
} else {
    write(STDIN_WRITE, "\x00\x0a\x00\xff", 4);
    write(STDERR_WRITE, "\x00\x0a\x02\xff", 4);
}
```

### Stage 3

This stage is about environment variables.

You can use `execve` to pass new environment variables.

```c
char* envp[2];
envp[0] = "\xde\xad\xbe\xef=\xca\xfe\xba\xbe";
envp[1] = NULL;
execve("/home/input2/input", argv, envp);
```

### Stage 4

This stage is about file.

Just create file and write required bytes to it.

```c
FILE* hFile = fopen("\x0a", "w");
if (hFile == NULL) {
    printf("Failed to create file.\n");
    exit(0);
}
fwrite("\x00\x00\x00\x00", 4, 1, hFile);
fclose(hFile);
```

### Stage 5

This stage is about network.

Use socket to pass this stage. Don't forget to specify a port in `argv['C']`.

```
argv['C'] = "33333";
```

```c
int sock;
struct sockaddr_in addr;
addr.sin_family = AF_INET;
addr.sin_port = htons(33333);
addr.sin_addr.s_addr = inet_addr("127.0.0.1");
sock = socket(AF_INET, SOCK_STREAM, 0);
connect(sock, (struct sockaddr*)&addr, sizeof(addr));
send(sock, "\xde\xad\xbe\xef", 4, 0);
close(sock);
```

Now upload your code to `/tmp` and use `gcc` to compile.

```bash
input2@ubuntu:~$ mkdir /tmp/solve2
input2@ubuntu:~$ cd /tmp/solve2
input2@ubuntu:/tmp/solve2$ vim solve.c                  # Paste your code in vim
input2@ubuntu:/tmp/solve2$ gcc ./solve.c -o solve
input2@ubuntu:/tmp/solve2$ ln -s /home/input2/flag      # Don't forget to create a symbol link to /home/input2/flag.
                                                        # Otherwise you will get nothing.

input2@ubuntu:/tmp/solve2$ ./solve
Welcome to pwnable.kr
Let's see if you know how to give input to program
Just give me correct inputs then you will get the flag :)
Stage 1 clear!
Stage 2 clear!
Stage 3 clear!
Stage 4 clear!
Stage 5 clear!
Mommy! I learned how to pass various input in Linux :)
```
