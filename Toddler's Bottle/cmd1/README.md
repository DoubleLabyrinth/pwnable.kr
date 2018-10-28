# pwnable.kr -- Toddler's Bottle -- cmd1

## 1. Challenge

```
Mommy! what is PATH environment in Linux?

ssh cmd1@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect via SSH and see source code.

```c
// cmd.c
#include <stdio.h>
#include <string.h>

int filter(char* cmd){
    int r=0;
    r += strstr(cmd, "flag")!=0;
    r += strstr(cmd, "sh")!=0;
    r += strstr(cmd, "tmp")!=0;
    return r;
}
int main(int argc, char* argv[], char** envp){
    putenv("PATH=/fuckyouverymuch");
    if(filter(argv[1])) return 0;
    system( argv[1] );
    return 0;
}
```

`"flag"`, `"sh"` and `"tmp"` are filtered. But we can use wildcard.

```bash
$ ./cmd1 "/bin/cat fla*"
```
