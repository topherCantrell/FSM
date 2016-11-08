# Declarative Finite State Machines

# Links
8x8 LED Display:
http://www.adafruit.com/product/902

LED Button (Mouser P/N: 633-15ACBKG036CF-2SJB):
http://www.mouser.com/search/ProductDetail.aspx?R=0virtualkey0virtualkeyKP0115ACBKG036CF-2SJB

Full Tic Tac Toe State Machine Diagram:
https://github.com/topherCantrell/StateMachines

TODO: youtube video of Raspberry Pi version (maybe both?) Include screen shots of github and put github link in the comments.

HT16K133 LED Matrix Backpack Driver:
http://obex.parallax.com/object/747

Tic Tac Tome:
http://www.amazon.com/Tic-Tac-Tome-Autonomous-Playing/dp/1594746877

# Hardware

Left is the Raspberry Pi running the state machine in NodeJS. Right is the Parallax Propeller running the state machine in SPIN.
![](https://github.com/topherCantrell/FSM/blob/master/art/photo1.jpg)

The Raspberry Pi playing the Tic Tac Toe Tome. The Pi found the one winning case coded purposefully into the book.
![](https://github.com/topherCantrell/FSM/blob/master/art/photo2.jpg)

The hardware schematics and connections to the CPUs.
![](https://github.com/topherCantrell/FSM/blob/master/art/figure1.jpg)

An older version of the hardware running on the Synapse SN171 proto board.
![](https://github.com/topherCantrell/FSM/blob/master/art/SnapTacToe.jpg)

# Tic Tac Toe State Machine

The bubbles in the diagram below are the individual states. The purple function calls are made when the machine enters the state. The blue arrows show events and the target state.

## Splash Screens

This part of the state machine is an attract mode. The machine shows the individual letters for the words "TIC", "TAC", and "TOE" and sweeps the display clean with a line between. Press the button to start the game in the "PICKS" state.

![](https://github.com/topherCantrell/FSM/blob/master/art/TTTFSM1.png)

## Pick a Game

This part of the machine picks a computer player and decides who goes first.
 
![](https://github.com/topherCantrell/FSM/blob/master/art/TTTFSM2.png)

## Game Play

This part of the machine includes the player's input loop. You press the button and quickly release it to advance the cursor. If you hold the button down you enter the move. The cursor only stops at available cells. The machine alternates between player and CPU until there is a win or a tie.

![](https://github.com/topherCantrell/FSM/blob/master/art/TTTFSM3.png)

## Game Over

This part of the machine shows the winner of the game. The button flashes the color of the winner (orange for tie) until you press the button. Then the machine returns to the splash mode.

![](https://github.com/topherCantrell/FSM/blob/master/art/TTTFSM4.png)