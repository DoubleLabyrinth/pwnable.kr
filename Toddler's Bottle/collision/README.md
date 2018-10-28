# pwnable.kr -- Toddler's Bottle -- collision

## 1. Challenge

```
Daddy told me about cool MD5 hash collision today.
I wanna do something like that too!

ssh col@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Connect target via ssh and see source code:

```c
#include <stdio.h>
#include <string.h>

unsigned long hashcode = 0x21DD09EC;

unsigned long check_password(const char* p) {
    int* ip = (int*)p;
    int i;
    int res=0;
    for(i=0; i<5; i++){
        res += ip[i];
    }
    return res;
}

int main(int argc, char* argv[]) {
    if(argc<2){
        printf("usage : %s [passcode]\n", argv[0]);
        return 0;
    }

    if(strlen(argv[1]) != 20){
        printf("passcode length should be 20 bytes\n");
        return 0;
    }

    if(hashcode == check_password(argv[1])){
        system("/bin/cat flag");
        return 0;
    }
    else
        printf("wrong passcode.\n");

    return 0;
}
```

We can see the program receives a 20-bytes-long string and casts it into an integer array, then add 5 integers up. If result is equal to hashcode we can get the flag.

So the problem is how to build a such string that meets the requirements said above.

We can add `0x200000000` to hashcode, so the result is `0x221DD09EC`. Then divide it by `5` and we can get `0x6D2C352F`, which can be casted into `char[4] = "/5,m"`.

Now multiply `0x6D2C352F` with `5` and we can get `0x221DD09EB` which is not equal to `hashcode` in `mod 2^32`. We must add 1 to one of the 5 integers, so that we can get `0x221DD09EC` after adding the 5 integers up.

Finally,

```bash
$ ./col "/5,m/5,m/5,m/5,m05,m"
```
