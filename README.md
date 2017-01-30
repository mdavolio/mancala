# Mancala - Oware Version
Simulator for Mancala

## How To Play
Run play.py file

Play moves clock-wise for both players

Player 1 moves cells 0-5
Player 2 moves cells 7-12

An incorect move will NOT produce an error message however the game always shows which player's move is currently in progress

Player 1's score is located in cell 6
Player 2's score is located in cell 13

A player moves again when their last stone in a move ends in their scoring bin

Capturing occurs when the last stone of a move ends in an empty cell on the player's side of the board. This will capture all stones on both side of the board at this cell's location.
(ex: if player 1's last stone ends in cell 5 and it was empty, player 1 collects this stone as well as any in cell 7)

Game currently ends when one player's side is empty

### Still working on
-Need to change when the game ends

-Need to construct bot to play
