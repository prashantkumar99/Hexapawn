from colorama import Style, Fore, Back
import colorama
colorama.init(autoreset = True)
PLAYER_1 = 1
PLAYER_2 = 2
PLAYER_1_COLOR = Style.BRIGHT + Fore.BLUE
PLAYER_2_COLOR = Style.BRIGHT + Fore.RED

PLAYERS = (PLAYER_1, PLAYER_2)

def otherPlayer(player):
    if player == PLAYER_1:
        return PLAYER_2
    if player == PLAYER_2:
        return PLAYER_1



class Player:
    name = ""
    def __init__(self, name):
        self.name = name

    def readMoveCoordinates(self):
        pass
    def result(self, won):
        pass