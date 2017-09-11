#!/usr/bin/python3

from pwn import *

s = ssh('memcpy', 'pwnable.kr', 2222, 'guest')
p = s.connect_remote('localhost', 9022)

p.recvuntil('specify the memcpy amount between 8 ~ 16 : ')

p.sendline(str(0 + 8))
print(str(0 + 8))
for i in range(1, 10):
    p.sendline(str(8 * 2 ** i + 8))
    print(str(8 * 2 ** i + 8))

time.sleep(2)
print(p.recvall().decode('ascii'))