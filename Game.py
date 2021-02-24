
from Player import *
from colorama import Fore, Back, Style
import colorama
colorama.init(autoreset = True)
import os
from Log import *

class Game:
    current_playing = PLAYER_2
    winner = None
    board = None
    player_names = None
    players = None
    err = ""

    def __init__(self, player_1, player_2, board):
        self.current_playing = PLAYER_2
        self.winner = None
        self.board = board
        self.player_names = {PLAYER_1: player_1.name, PLAYER_2: player_2.name}
        self.players = {PLAYER_1: player_1, PLAYER_2: player_2}
        self.err = ""

    def __repr__(self):
        self.print()
        return ""

    def move(self):
        self.setError("")
        moved = False
        while not moved:
            try:
                self.print()
                row, col, final_row, final_col = self.readPlayerMove()
                self.board.move(self.current_playing, row, col, final_row, final_col)
                moved = True
            except Exception as e:
                self.setError(e)


    def play(self):
        winner = None
        while winner is None:

            self.move()

            self.current_playing = otherPlayer(self.current_playing)
            winner = self.board.winner()
        else:
            self.print()
            self.winner = winner
            for player in self.players:
                self.players[player].result(winner)


    def readPlayerMove(self):
        try:
            coordinates = self.players[self.current_playing].readMoveCoordinates()
        except ValueError as e:
            self.print()
            self.setError("Only integers are accepted as coordinates!")
            coordinates = self.readPlayerMove()

        return coordinates
    def setError(self, e):
        self.err = str(e)
    def print(self):
        os.system('cls')
        print(Fore.GREEN + "HEXAPAWN\n")
        self.board.print()
        error(self.err)

