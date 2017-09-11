#!/usr/bin/python3
from pwn import *

rand = 0x6b8b4567

s = ssh('random', 'pwnable.kr', 2222, 'guest')
p = s.process('./random')

key = rand ^ 0xdeadbeef

p.sendline(str(key))
print(p.recvall().decode('ascii'))