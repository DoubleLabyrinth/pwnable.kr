# pwnable.kr -- Toddler's Bottle -- blackjack

## 1. Challenge

```
Hey! check out this C implementation of blackjack game!
I found it online
* http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html

I like to give my flags to millionares.
how much money you got?

Running at : nc pwnable.kr 9009
```

## 2. Solution

Goto the given [link](http://cboard.cprogramming.com/c-programming/114023-simple-blackjack-program.html) and see source code.

In function `betting`:

```cpp
int betting() //Asks user amount to bet
{
  printf("\n\nEnter Bet: $");
  scanf("%d", &bet);

  if (bet > cash) //If player tries to bet more money than player has
  {
    printf("\nYou cannot bet more money than you have.");
    printf("\nEnter Bet: ");
    scanf("%d", &bet);
    return bet;
  }
  else return bet;
} // End Function
```

You can see if `bet` you input first is larger than cash you have, you will be asked to input `bet` again. Sounds reasonable.

However, the second time when you input does not validate the value of `bet`.

So just input `10000000` and win the game once, then you will see the flag.
