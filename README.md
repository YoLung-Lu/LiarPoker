Liar Poker
==========

A Hold'em like poker game between 2 players that allow players to tell a lie on card he has.


## Game Flow

  * Game start:
    Each player got 5 cards and 500 chips. Also, 2 cards are opened as board cards.

    A game round has 4 turns.

    Players has to show card(s) he has to his opponent and select bet type (large, middle, small or fold) in the first three turns.

    In the last turn, players can suspect his opponent on made a lie.

  * Turn 1: Players select bet and reveal 3 cards.

  * Turn 2: Players select bet and reveal 1 card.

  * Turn 3: Players select bet. He can then decide to reveal his last card or **lie** on the card he has.
    If a player lied on his card, the last card he revealed will become the card he demanded.

  * Turn 4: Players confirm the result of round or **suspect** on his opponent lied.
    If the suspect stand, the player  caught will be punished for his lie.

The game repeated until one player out of chip.



## Win A Game Round

Like Hold'em, this game has a **card winner**, who has better card rank.

However, card winner might not be the **round winner** if he is caught lied.

**Round winner** defined in this game is: the player receive more chip in the round.

The shift of chip is related to card winner, action on lie and suspect.



## Chip Shift

  Each turn has different bet:

  Turn  \t1\t2\t3

  Large \t30\t40\t50

  Middle\t20\t20\t30

  Small \t10\t10\t20


  * Fold:
    - If one player fold, all the bet in the round gave to his opponent.
    - If both player fold, all the bet are added into "bonus" pool.

  * Lie:
    - Tell a lie has its cost.
    - If a player choose to tell a lie, the potential cost is half of bet chip this round.
    - The cost only paid if he got caught on lie.

  * Suspect:
    - Suspect also cost half of bet chip this round.
    - If suspect stands, player not only receive lie cost of his opponent, but also get his suspect fee back.
    - If suspect not stand, the suspect cost are add to the "bonus" pool.

  * When card winner caught:
    - Unfortunately, the chip he won in this round will be kept in the "bonus" pool.

  * Bonus:
    - All bonus become the extra price of next round.
    - The round winner of next round will take away all bonus.
    - When a round has no winner, bonus continuous to grow.


## Note

* 12/16/2016 First day.
* 01/09/2017 Prototype.


## Powered by

[`Kivy`](https://github.com/kivy/kivy) for android framework.

[`Deuces`](https://github.com/worldveil/deuces) for poker rules and evaluation of hands.


## Screenshot

![Screenshot](/screenshots/screenshot_v0.1.1.png)
