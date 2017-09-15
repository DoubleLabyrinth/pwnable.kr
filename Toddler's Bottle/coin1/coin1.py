#!/usr/bin/python3
import socket
import re
import time

pattern = re.compile('N=\d+\sC=\d+')

s = socket.socket()
s.connect(('localhost', 9007))
s.recv(1024)        # what received is just a introduction, we do not need it.
time.sleep(4)

while True:
    received = s.recv(1024).decode('ascii')
    print(received, end='')
    received = received.replace('\n', '')
    matches = re.findall(pattern, received)

    if len(matches) == 0:
        break

    match = matches[0].split(' ')
    N = int(match[0].replace('N=', ''))
    C = int(match[1].replace('C=', ''))

    start = 0
    end = N
    for i in range(0, C):
        if end - start == 1:
            print(start)
            s.send(str(start).encode('ascii') + b'\n')
        else:
            sd = ' '.join(str(j) for j in range(start, (end + start) // 2))
            print(sd)
            s.send(sd.encode('ascii') + b'\n')

        result = s.recv(1024).decode('ascii')
        print(result, end = '')
        if result.startswith('Correct'):
            break

        try:
            result = int(result.replace('\n', ''))
        except:
            exit(-1)

        if result == ((end + start) // 2 - start) * 10:
            start = (end + start) // 2
        else:
            end = (end + start) // 2

    s.send(str(start).encode('ascii') + b'\n')
    print(s.recv(1024).decode('ascii'), end = '')
