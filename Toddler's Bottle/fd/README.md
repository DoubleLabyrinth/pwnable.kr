# pwnable.kr -- Toddler's Bottle -- fd

# 1. Challenge

```
Mommy! what is a file descriptor in Linux?

try to play the wargame your self but if you are ABSOLUTE beginner, follow
this tutorial link: https://www.youtube.com/watch?v=blAxTfcW9VU

ssh fd@pwnable.kr -p2222 (pw:guest)
```

# 2. Solution

Since the challenge gives us a ssh connection, let's connect target first.

After you get shell via ssh, use `ls` and you can find there are three files at current directory: `fd`, `fd.c`, `flag`.

Of course, you do not have permissions to read `flag`, but ELF file `fd` has. And `fd.c` is the source code of `fd`.

Let's use `cat fd.c` to see the source code:

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char buf[32];
int main(int argc, char* argv[], char* envp[]){
    if(argc<2){
        printf("pass argv[1] a number\n");
        return 0;
    }
    int fd = atoi( argv[1] ) - 0x1234;
    int len = 0;
    len = read(fd, buf, 32);
    if(!strcmp("LETMEWIN\n", buf)){
        printf("good job :)\n");
        system("/bin/cat flag");
        exit(0);
    }
    printf("learn about Linux file IO\n");
    return 0;
}
```

Obviously, if we set fd to 0 (which stands for `stdin`), then the program will read something from `stdin`. 

So we just type `LETMEWIN`, then the flag will display.
