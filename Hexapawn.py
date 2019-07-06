
from Game import Game
from Board import *
import Log
from sys import argv
from AI import AI
from Human import Human
import os

YES = ("yes", "y", "yeah")
NO = ("no", "n", "nope")

INTRO = """Hexapawn is a deterministic two-player game invented by Martin Gardner.
It was invented in order to demonstrate,
how it could be played by a heuristic AI implemented by a mechanical computer.
Check out this link to know more:-
https://www.youtube.com/watch?v=sw7UAZNgGg8
Rules:-
1. Pawns can move forward or diagonally upward.
2. Pawn can't move forward if target position is already occupied.
3. Pawn can move diagonally only to strike out opponents pawn.
4. To win either a pawn reaches other end of board or strikes out every opponent pawn.
"""

def printHeading():
    os.system('cls')
    print(Fore.GREEN + "HEXAPAWN\n")
#Log.logging = False
if len(argv) > 1:
    Log.logging = eval(argv[1])



printHeading()
print(INTRO)

name_1 = "AI"
name_2 = ''
while len(name_2) == 0:
    name_2 = input("Player Name: ")

human = Human(name_2)

play = True
while play:
    board = Board()

    ai = AI(name_1, PLAYER_1, board, intelligent=True)
    ai.save_intelligence = True
    game = Game(ai, human, board)
    game.play()
    print("WINNER: ", game.player_names[game.board.winner()])
    play = input("Play Again(y/n): ") in YES
