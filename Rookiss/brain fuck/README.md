# pwnable.kr -- Rookiss -- brain fuck
Try to read items in GOT table and modify them to get shell.

## 1. Challenge
  > I made a simple brain-fuck language emulation program written in C.  
  > The [ ] commands are not implemented yet. However the rest functionality seems working fine.  
  > Find a bug and exploit it to get a shell.  
  >   
  > Download : http://pwnable.kr/bin/bf  
  > Download : http://pwnable.kr/bin/bf_libc.so  
  >   
  > Running at : nc pwnable.kr 9001  

## 2. Solution
  * Download the two binary files, `bf` and `bf_libc.so` and send them to IDA.

  * In `bf`, you can see the program initializes a pointer `p` and receives a brainfuck language string.  
    Then do something in `do_brainfuck` function.  

    In `do_brainfuck` function, we know that:

    |Char |operation |
    |-----|----------|
    |  +  |  ++(\*p) |
    |  -  |  --(\*p) |
    |  ,  |  \*p = getchar() |
    |  .  |  putchar(\*p)    |
    |  <  |  --p     |
    |  >  |  ++p     |

  * So we can use `<` to make the pointer `p` point to `.bss:0804A080 p dd ?` and `.got.plt:0804A010 off_804A010 dd offset fgets`, then use `.` to read the address of the pointer `p` and the address of function `fgets`.

  * After the program leaks the addresses, we can calculate the address of function `main`, `system` and `gets`.

  * Then use `>` and `.` to overwrite some items in GOT table. Exactly:

    ```
    fgets    -->  system
    memset   -->  gets
    putchar  -->  main
    ```

  * Finally, use `.` to call modified `putchar` which actually is `main`.

    Then in function `main`, when calls `memset`, it actually calls `gets`. Just send `/bin/sh`.

    And next it will call `fgets` which actually is `system`, so you can get shell.
