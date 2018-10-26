# pwnable.kr -- Rookiss -- echo2

## 1. Challenge

```
Pwn this echo service.

download : http://pwnable.kr/bin/echo2

Running at : nc pwnable.kr 9011
```

## 2. Solution

This one is a little harder than echo1. I just give you some hints:

1. A block of memory, which the global variable `o` points to, could be used after free if you try to exit and cancel exit.

2. You can use function `echo2()` to leak `$rbp` of `main()` and libc's address. Then find out addresses of `system()` and string `/bin/sh`. 

3. Use `echo3()` to trigger UAF so we can go to `main()` again.

4. Write shellcode when application asks you input your name. So the shellcode would be on stack. At the mean time, calculate the address of the shellcode based on the `$rbp` of previous `main()`.

   The shellcode can be

   ```asm
   mov rdi, libc_bin_sh_addr
   mov rax, libc_system
   call rax
   ```

5. Use `echo3()` to trigger UAF again. But this time we go to our shellcode. 

6. You will get shell. Use `cat flag` to get the flag.

