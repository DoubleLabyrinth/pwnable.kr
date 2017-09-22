# pwnable.kr -- Toddler's Bottle -- codemap

## 1. Challenge
  > I have a binary that has a lot information inside heap.  
  > How fast can you reverse-engineer this?  
  > (hint: see the information inside EAX,EBX when 0x403E65 is executed)  
  >   
  > download: http://pwnable.kr/bin/codemap.exe  
  >   
  >   
  > ssh codemap@pwnable.kr -p2222 (pw:guest)  

## 2. Solution
  * Connect target via ssh and read `readme`:
    > reverse engineer the 'codemap.exe' binary, then connect to codemap daemon(nc 0 9021),  
    > the daemon will ask you some question, provide the correct answer to get flag.  

  * So type `nc 0 9021` at ssh-shell to see what the questions are:
    > 1. What is the string inside 2nd biggest chunk?  
    > 2. What is the string inside 3rd biggest chunk?  

  * As it it a reversing task, so we can try to open the target exe file in IDA. We can find the program will tell 1st biggest chunk's size and the string inside it. We can try our best to find out the algorithms that generate chunks' size and strings. The algorithm that generates strings is easy to get while the algorithm that generates chunks' size is too hard to find out.

  * However, we can find that in function `main()` the program will check whether the size of new generated chunk is bigger than the size of the current biggest chunk. If it is, the current biggest chunk will be updated.

  * So we can set up a breakpoint at where the current chunk is updating. Exactly speaking, it is at `main() + 0x135`. Then set the action after the breakpoint is triggered:

    ![set_bp](set_bp.png)

  * Every time the breakpoint is triggered, you can see something printed out at `Output` window:

    ![output](output.png)

  * There wound be approximately 1000 lines. We can send it to python and find out 2nd biggest one and 3rd biggest one. The corresponding string is `"roKBkoIZGMUKrMb"` and `"2ckbnDUabcsMA2s"`.
