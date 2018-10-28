# pwnable.kr -- Toddler's Bottle -- random

# 1. Challenge

```
Daddy, teach me how to use random value in programming!  

ssh random@pwnable.kr -p2222 (pw:guest)  
```

# 2. Solution

Just connect target via ssh and see source code:  

```c
#include <stdio.h>

int main(){
  unsigned int random;
  random = rand();	// random value!

  unsigned int key=0;
  scanf("%d", &key);

  if( (key ^ random) == 0xdeadbeef ){
    printf("Good!\n");
    system("/bin/cat flag");
    return 0;
  }

  printf("Wrong, maybe you should try 2^32 cases.\n");
  return 0;
}
```

You can see that the seed of random function is not set in the source code, which means that the integer variable `random` is predicable every time the program starts.

On Linux, the integer variable `random` must be `0x6b8b4567`.

So the key should be:

```
0x6b8b4567 ^ 0xdeadbeef = 0xB526FB88 = 3039230856
```

Just input the key and then get the flag.
