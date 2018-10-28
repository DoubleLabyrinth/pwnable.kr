# pwnable.kr -- Toddler's Bottle -- leg

## 1. Challenge

```
Daddy told me I should study arm.
But I prefer to study my leg!

Download : http://pwnable.kr/bin/leg.c
Download : http://pwnable.kr/bin/leg.asm

ssh leg@pwnable.kr -p2222 (pw:guest)
```

## 2. Solution

Review code in `leg.c`. You can see just make sure that expression `key1()+key2()+key3()) == key` is true where the value of `key` depends on your input.

Review assembly code in `leg.asm`.

1. __key1()__

   ```
   (gdb) disass key1
   Dump of assembler code for function key1:
       0x00008cd4 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008cd8 <+4>:	add	r11, sp, #0
       0x00008cdc <+8>:	mov	r3, pc
       0x00008ce0 <+12>:	mov	r0, r3
       0x00008ce4 <+16>:	sub	sp, r11, #0
       0x00008ce8 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008cec <+24>:	bx	lr
   End of assembler dump.
   ```

   You can see `0x00008cdc <+8>:	mov	r3, pc` where the value of `pc` is `0x00008ce4`.

   So __key1()__ returns `0x00008ce4`.

2. __key2()__

   ```
   (gdb) disass key2
   Dump of assembler code for function key2:
       0x00008cf0 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008cf4 <+4>:	add	r11, sp, #0
       0x00008cf8 <+8>:	push	{r6}		; (str r6, [sp, #-4]!)
       0x00008cfc <+12>:	add	r6, pc, #1
       0x00008d00 <+16>:	bx	r6
       0x00008d04 <+20>:	mov	r3, pc
       0x00008d06 <+22>:	adds	r3, #4
       0x00008d08 <+24>:	push	{r3}
       0x00008d0a <+26>:	pop	{pc}
       0x00008d0c <+28>:	pop	{r6}		; (ldr r6, [sp], #4)
       0x00008d10 <+32>:	mov	r0, r3
       0x00008d14 <+36>:	sub	sp, r11, #0
       0x00008d18 <+40>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008d1c <+44>:	bx	lr
   End of assembler dump.
   ```

   When the program runs to 0x00008d04, `pc` is `0x00008d08` so `r3` will be assigned `0x00008d08` to.

   Then `adds	r3, #4`, `r3` will be `0x00008d0C`. After that `r3` will not be modified so __key2()__ returns `0x00008d0C`.

3. __key3()__

   ```
   (gdb) disass key3
   Dump of assembler code for function key3:
       0x00008d20 <+0>:	push	{r11}		; (str r11, [sp, #-4]!)
       0x00008d24 <+4>:	add	r11, sp, #0
       0x00008d28 <+8>:	mov	r3, lr
       0x00008d2c <+12>:	mov	r0, r3
       0x00008d30 <+16>:	sub	sp, r11, #0
       0x00008d34 <+20>:	pop	{r11}		; (ldr r11, [sp], #4)
       0x00008d38 <+24>:	bx	lr
   End of assembler dump.
   ```

   `lr` stores the address of return. So go back to see the assembly code of `main` and you will find:

   ```
   0x00008d7c <+64>:	bl	0x8d20 <key3>
   0x00008d80 <+68>:	mov	r3, r0
   ```

   So __key3()__ returns `0x00008d80`.

Obviously, the value of `key` must be `0x00008ce4 + 0x00008d0C + 0x00008d80 = 0x1a770` which is `108400` in base 10.

So connect via SSH, and in terminal:

```bash
$ ./leg
Daddy has very strong arm! :
```

Just type `108400` and you will get the flag.
  
