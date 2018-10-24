#!/usr/bin/env python2
from pwn import *

conn = None
allowed_chars = '1234567890abcdefghijklmnopqrstuvwxyz-_'

def Sendline(s):
    global conn
    sleep(0.1)
    print s
    conn.sendline(s)

def GetEncryptedData(id, pw):
    global conn
    conn = remote('pwnable.kr', 9006)
    conn.read()
    Sendline(id)
    conn.read()
    Sendline(pw)
    conn.readuntil('sending encrypted data')
    enc_data = conn.readuntil(')')
    conn.read()
    enc_data = enc_data.strip(' ')
    enc_data = enc_data.lstrip('(')
    enc_data = enc_data.rstrip(')')
    enc_data = enc_data.decode('hex')
    print enc_data.encode('hex')
    conn.close()
    return enc_data

def TryToGetCookieLength():
    enc_cookie = GetEncryptedData('', '')

    cookie_length_min = len(enc_cookie) - 2 - 16
    cookie_length_max = len(enc_cookie) - 2
    print '[*] cookie length could be [%d, %d)' % (cookie_length_min, cookie_length_max)

    i = 1
    while True:
        enc_cookie2 = GetEncryptedData('', '-' * i)
        if len(enc_cookie2) != len(enc_cookie):
            break
        else:
            i += 1
    
    cookie_length = len(enc_cookie) -i - 2
    print '[*] cookie length is %d' % cookie_length
    return cookie_length

def TryToGetCookie(cookie_expected_len):
    probe_size = (cookie_expected_len + 15) // 16 * 16
    # cookie = 'you_will_never_guess_this_sugar_honey_salt_cookie'
    cookie = ''
    for i in range(len(cookie), cookie_expected_len):
        data = GetEncryptedData('', '-' * (probe_size - 2 - i - 1))
        bFound = False
        for c in allowed_chars[::-1]:
            data2 = GetEncryptedData('', '-' * (probe_size - 1 - len(cookie) - 1) + cookie + c)
            if data[0:probe_size] == data2[0:probe_size]:
                bFound = True
                cookie += c
                break
        if not bFound:
            raise ValueError('Cannot find valid a char.')
    return cookie

cookie_length = TryToGetCookieLength()
cookie = TryToGetCookie(cookie_length)
print('cookie = %s' % cookie)
