# pwnable.kr -- Toddler's Bottle -- blukat

## 1. Challenge

> Sometimes, pwnable is strange...  
> hint: if this challenge is hard, you are a skilled player.  
>   
> ssh blukat@pwnable.kr -p2222 (pw: guest)  

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

If you are scrupulous, you may notice that `blukat` can read `password` file which means `blukat` has `Set-UID` right.

```bash
blukat@ubuntu:~$ ls -al
total 36
drwxr-x---  4 root blukat     4096 Aug 15 22:55 .
drwxr-xr-x 93 root root       4096 Oct 10 22:56 ..
-r-xr-sr-x  1 root blukat_pwn 9144 Aug  8 06:44 blukat
-rw-r--r--  1 root root        645 Aug  8 06:43 blukat.c
dr-xr-xr-x  2 root root       4096 Aug 15 22:55 .irssi
-rw-r-----  1 root blukat_pwn   33 Jan  6  2017 password
drwxr-xr-x  2 root root       4096 Aug 15 22:55 .pwntools-cache
```

Why not we just launch `blukat` via `gdb` and dump `password` out?

```bash
blukat@ubuntu:~$ gdb ./blukat

GNU gdb (Ubuntu 7.11.1-0ubuntu1~16.04) 7.11.1
Copyright (C) 2016 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.  Type "show copying"
and "show warranty" for details.
This GDB was configured as "x86_64-linux-gnu".
Type "show configuration" for configuration details.
For bug reporting instructions, please see:
<http://www.gnu.org/software/gdb/bugs/>.
Find the GDB manual and other documentation resources online at:
<http://www.gnu.org/software/gdb/documentation/>.
For help, type "help".
Type "apropos word" to search for commands related to "word"...
Reading symbols from ./blukat...(no debugging symbols found)...done.

(gdb) b *main+110
Breakpoint 1 at 0x400868

(gdb) r
Starting program: /home/blukat/blukat
guess the password!
aaa

Breakpoint 1, 0x0000000000400868 in main ()
(gdb) x /s &password
0x6010a0 <password>:    "cat: password: Permission denied\n"

(gdb)

```

Just use `password` to get the flag:

```bash
blukat@ubuntu:~$ ./blukat
guess the password!
cat: password: Permission denied
congrats! here is your flag: Pl3as_DonT_Miss_youR_GrouP_Perm!!
```

