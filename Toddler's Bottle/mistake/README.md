# pwnable.kr -- Toddler's Bottle -- mistake

## 1. Challenge

```
We all make mistakes, let's move on.
(don't take this too seriously, no fancy hacking skill is required at all)

This task is based on real event
Thanks to dhmonkey

hint : operator priority

ssh mistake@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
#include <stdio.h>
#include <fcntl.h>

#define PW_LEN 10
#define XORKEY 1

void xor(char* s, int len){
int i;
for(i=0; i<len; i++){
        s[i] ^= XORKEY;
}
}

int main(int argc, char* argv[]){

int fd;
if(fd=open("/home/mistake/password",O_RDONLY,0400) < 0){
        printf("can't open password %d\n", fd);
        return 0;
}

printf("do not bruteforce...\n");
sleep(time(0)%20);

char pw_buf[PW_LEN+1];
int len;
if(!(len=read(fd,pw_buf,PW_LEN) > 0)){
        printf("read error\n");
        close(fd);
        return 0;
}

char pw_buf2[PW_LEN+1];
printf("input password : ");
scanf("%10s", pw_buf2);

// xor your input
xor(pw_buf2, 10);

if(!strncmp(pw_buf, pw_buf2, PW_LEN)){
        printf("Password OK\n");
        system("/bin/cat flag\n");
}else{
        printf("Wrong Password\n");
}

close(fd);
return 0;
}
```

We can see that the operator priority is confused. So actually the password is decided by your first input.

The second input should be characters in the first input xor by `1`.

```bash
mistake@ubuntu:~$ ./mistake
do not bruteforce...
1111111111
input password : 0000000000
Password OK
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
