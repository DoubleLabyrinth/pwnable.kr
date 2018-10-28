# pwnable.kr -- Toddler's Bottle -- blukat

## 1. Challenge

```
Sometimes, pwnable is strange...
hint: if this challenge is hard, you are a skilled player.
 
ssh blukat@pwnable.kr -p2222 (pw: guest)
```

## 2. Solution

Log in via SSH and see source code:

```c
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
char flag[100];
char password[100];
char* key = "3\rG[S/%\x1c\x1d#0?\rIS\x0f\x1c\x1d\x18;,4\x1b\x00\x1bp;5\x0b\x1b\x08\x45+";
void calc_flag(char* s){
        int i;
        for(i=0; i<strlen(s); i++){
                flag[i] = s[i] ^ key[i];
        }
        printf("%s\n", flag);
}
int main(){
        FILE* fp = fopen("/home/blukat/password", "r");
        fgets(password, 100, fp);
        char buf[100];
        printf("guess the password!\n");
        fgets(buf, 128, stdin);
        if(!strcmp(password, buf)){
                printf("congrats! here is your flag: ");
                calc_flag(password);
        }
        else{
                printf("wrong guess!\n");
                exit(0);
        }
        return 0;
}

```

You can see `buf` is allocated at stack and the size of it is 100 bytes. However, `fget` can receive 128 bytes at most and store received bytes to `buf`. This is a classical BOF exploit. But we cannot use it for there is canary. I wasted a lot of time here :-(

```
    Arch:     amd64-64-little
    RELRO:    Partial RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      No PIE (0x400000)
```

After some search, here is the solution:

```
blukat@ubuntu:~$ id
uid=1104(blukat) gid=1104(blukat) groups=1104(blukat),1105(blukat_pwn)
blukat@ubuntu:~$
```

You will find that you are in `blukat_pwn` group which means you have right to read `password`

```
blukat@ubuntu:~$ cat password
cat: password: Permission denied
```

You may wander why you cannot read `password`. Well, the fact is that the content of `password` is `"cat: password: Permission denied"`. If you don't believe, you can do this:

```
blukat@ubuntu:~$ cat password 2>/dev/null
cat: password: Permission denied
blukat@ubuntu:~$
```

If you are really not allowed to read `password`, you will get nothing for errors have been redirected to `/dev/null`.

So just use the password you got to get the flag:

```bash
blukat@ubuntu:~$ ./blukat
guess the password!
cat: password: Permission denied
congrats! here is your flag: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx!!
```

