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
