# pwnable.kr -- Grotesque -- rootkit

## 1. Challenge

```
I don't understand why my exploit is not working.
I need your help.

download : http://pwnable.kr/bin/wtf
download : http://pwnable.kr/bin/wtf.py

Running at : nc pwnable.kr 9015
```

## 2. Solution

Hint:

The buffer size of `scanf` is 4096 bytes. 

Bytes after the first 4096 bytes will not be read to `scanf`'s buffer and they will be read in the next `read` call.

```console
$ ./solve.py 
[+] Opening connection to pwnable.kr on port 9015: Done

    ---------------------------------------------------
    -              Shall we play a game?              -
    ---------------------------------------------------
    
    Hey~, I'm a newb in this pwn(?) thing...
    I'm stuck with a very easy bof task called 'wtf'
    I think this is quite easy task, however my
    exploit payload is not working... I don't know why :(
    I want you to help me out here.
    please check out the binary and give me payload
    let me try to pwn this with yours.

                                - Sincerely yours, newb
    
payload please : 
[*] Switching to interactive mode
thanks! let me try if your payload works...
hey! your payload got me this : ********************* // hidden


I admit, you are indeed an expert :)
[*] Got EOF while reading in interactive
$ 
[*] Interrupted
[*] Closed connection to pwnable.kr port 9015
```

