# SlaterPythonGames

[![Downloads](http://pepy.tech/badge/SlaterPythonGames)](http://pepy.tech/project/SlaterPythonGames)  ![PyPi](https://badge.fury.io/py/SlaterPythonGames.png)<br>

Python games by Ryan J. Slater [GitHub](https://github.com/rjslater2000/SlaterPythonGames)
[PyPi](https://pypi.org/project/SlaterPythonGames/)<br>
This is an updated replacement for [rygames](https://pypi.org/project/RyGames/)<br>

## Installation

To install: `pip install SlaterPythonGames`

## Games

Make sure to `import SlaterPythonGames as s`<br>
Here are the games currently included in this module:
- 2048
- Coin Game
- Country Guessing Game
- Tic-Tac-Toe
- Warships
- Warships2

### 2048

This is a clone of the popular mobile game under the same name. This will run with a Graphical User Interface, and with a scalable window size. You can find the original version [here](https://gabrielecirulli.github.io/2048/).<br>
Run with `s.TwentyFortyEight()`

### Coin Game

This is just a quick little game some new programmers write within their first year. Two players take turns flipping a coin, choosing from a penny, nickel, dime, or quarter. The players flip their coin, and if it lands on heads, the player gains the amount the coin is worth. If the coin lands on tails, they lose that amount. Players race to reach $1.00 first.<br>
Run with `s.CoinGame()`

### Country Guessing Game

Name as many countries as you can!

NOTE: This game was written on July 28th, 2017. The world has changed since then, so some of these countries may not exist any more and there may be new ones. I kinda don't feel like updating this though, since only my brother is crazy enough to play it seriously.

Run with `s.CountryGuessingGame()``

### Tic-Tac-Toe

If you don't know how to play this game, I'm wondering what you're doing here. Enter the number corresponding to the space you want to mark.

To play single-player: `s.TicTacToe1Player()`<br>
To play two-player: `s.TicTacToe2Player()`

### Warships

This is the game that won the high school competition at the [Shawnee State](http://www.shawnee.edu/gaming/) [17.0 Art & Gaming Conference](https://vrcfa.com/events/shawnee-17-0/) in 2017.
It's a text-based clone of the Battleship board game, with one or two player options. If you play the two-player version, you'll have access to some slightly different options.
Instructions are included in the game.

NOTE: Due to the use of colored text, this will not run on Windows 7.

Run with `s.Warships()`

### Warships2

This is the successor to Warships. Updates include a GUI, account system, and an AI that learns your personal play style and adapts to play against you!

Run with `s.Warships2()`
