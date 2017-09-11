#!/usr/bin/python3
from pwn import *

num0 = 0x6d2c352f
num1 = 0x6d2c3530

arg1 = pack(num0, 32) * 4 + pack(num1, 32)
arg1 = arg1.decode('ascii')

s = ssh('col', 'pwnable.kr', 2222, 'guest')
p = s.process(['./col', arg1])

print(p.recvall().decode('ascii'))
