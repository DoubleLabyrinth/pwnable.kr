from pwn import *
import re

cookie = ''
selection = 'abcdefghijklmnopqrstuvwxyz1234567890-_'

for i in range(0, 49):
    pp = remote('pwnable.kr', 9006)
    pp.readuntil('Input your ID')
    pp.sendline()
    pp.readuntil('Input your PW')
    pp.sendline((15 + 16 + 16 + 14 - i) * '-')
    pp.readuntil('sending encrypted data')
    correct_encrypt_string = re.findall('\((.+?)\)', pp.recvall().decode('ascii'))[0]
    print(correct_encrypt_string)
    pp.close()

    for j in selection:
        p = remote('pwnable.kr', 9006)

        p.readuntil('Input your ID')
        p.sendline()
        p.readuntil('Input your PW')
        p.sendline((15 + 16 + 16 + 14 + 1 - i) * '-' + cookie + j)
        p.readuntil('sending encrypted data')
        encrypt_string = re.findall('\((.+?)\)', p.recvall().decode('ascii'))[0]

        if encrypt_string[0:4 * 16 * 2] == correct_encrypt_string[0:4 * 16 * 2]:
            cookie += j
            p.close()
            break
        p.close()
        print(j, end = '')
    print('cookie =', cookie)