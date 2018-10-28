# pwnable.kr -- Toddler's Bottle -- coin1

## 1. Challenge

```
Mommy, I wanna play a game!
(if your network response time is too slow, try nc 0 9007 inside pwnable.kr server)

Running at : nc pwnable.kr 9007
```

## 2. Solution

```bash
$ nc pwnable.kr 9007
   
        ---------------------------------------------------
        -              Shall we play a game?              -
        ---------------------------------------------------

        You have given some gold coins in your hand
        however, there is one counterfeit coin among them
        counterfeit coin looks exactly same as real coin
        however, its weight is different from real one
        real coin weighs 10, counterfeit coin weighes 9
        help me to find the counterfeit coin with a scale
        if you find 100 counterfeit coins, you will get reward :)
        FYI, you have 30 seconds.

        - How to play -
        1. you get a number of coins (N) and number of chances (C)
        2. then you specify a set of index numbers of coins to be weighed
        3. you get the weight information
        4. 2~3 repeats C time, then you give the answer

        - Example -
        [Server] N=4 C=2        # find counterfeit among 4 coins with 2 trial
        [Client] 0 1            # weigh first and second coin
        [Server] 20                     # scale result : 20
        [Client] 3                      # weigh fourth coin
        [Server] 10                     # scale result : 10
        [Client] 2                      # counterfeit coin is third!
        [Server] Correct!

      - Ready? starting in 3 sec... -
```

Obviously you should use dichotomy search to get the answer. Because you have a very limited number of chances.

You can login target via any account. Both `cmd1@pwnable.kr` and `asm@pwnable.kr` are ok. Then you can write your code in `vim` and then save it at the directory `/tmp`.

Just run `coin1.py` and you will see the flag.
