from colorama import Fore, Back, Style
import colorama
colorama.init(autoreset = True)
from Player import *
from Log import log



PLAYER_1_PAWN = PLAYER_1_COLOR + '&' + Style.RESET_ALL
PLAYER_2_PAWN = PLAYER_2_COLOR + '@' + Style.RESET_ALL
EMPTY_PAWN = ' '


PAWNS = (PLAYER_1_PAWN, PLAYER_2_PAWN, EMPTY_PAWN)
PLAYER_PAWN = {PLAYER_1: PLAYER_1_PAWN, PLAYER_2: PLAYER_2_PAWN}

UP = 7
DOWN = 8
DIAGONAL_UP_RIGHT = 3
DIAGONAL_UP_LEFT = 4
DIAGONAL_DOWN_LEFT = 5
DIAGONAL_DOWN_RIGHT = 6
VALID_MOVES = (UP, DOWN, DIAGONAL_UP_RIGHT, DIAGONAL_UP_LEFT, DIAGONAL_DOWN_LEFT, DIAGONAL_DOWN_RIGHT)
PLAYER_1_VALID_MOVES = (DOWN, DIAGONAL_DOWN_LEFT, DIAGONAL_DOWN_RIGHT)
PLAYER_2_VALID_MOVES = (UP, DIAGONAL_UP_LEFT, DIAGONAL_UP_RIGHT)
PLAYER_VALID_MOVES = {PLAYER_1: PLAYER_1_VALID_MOVES, PLAYER_2: PLAYER_2_VALID_MOVES}
UPWARD_MOVES = (UP, DIAGONAL_UP_LEFT, DIAGONAL_UP_RIGHT)
DOWNWARD_MOVES = (DOWN, DIAGONAL_DOWN_LEFT, DIAGONAL_DOWN_RIGHT)
LEFTWARD_MOVES = (DIAGONAL_DOWN_LEFT, DIAGONAL_UP_LEFT)
RIGHTWARD_MOVES = (DIAGONAL_DOWN_RIGHT, DIAGONAL_UP_RIGHT)
DIAGONAL_MOVES = (DIAGONAL_DOWN_RIGHT, DIAGONAL_DOWN_LEFT, DIAGONAL_UP_RIGHT, DIAGONAL_UP_LEFT)
FORWARD_MOVES = (UP, DOWN)
MOVE_NAMES = {UP: "UP",
              DOWN: "DOWN",
              DIAGONAL_DOWN_LEFT: "DIAGONAL DOWN LEFT",
              DIAGONAL_DOWN_RIGHT: "DIAGONAL DOWN RIGHT",
              DIAGONAL_UP_LEFT: "DIAGONAL UP LEFT",
              DIAGONAL_UP_RIGHT: "DIAGONAL UP RIGHT"}

SEPERATOR_COLOR = Fore.GREEN
INDEX_COLOR = Style.DIM
COL_SEPERATOR = SEPERATOR_COLOR + "|" + Style.RESET_ALL
ROW_SEPERATOR = SEPERATOR_COLOR + "-" + Style.RESET_ALL

CLASS_NAME = "Board"


class InvalidPlayer(Exception):
    def __init__(self, description):
        self.description = description
    def __repr__(self):
        return self.description

class InvalidMove(Exception):
    def __init__(self, description):
        self.description = description
    def __repr__(self):
        return self.description

class Board:
    board = []
    row = 3
    col = 3
    player_1_pawn_coordinates = []
    player_2_pawn_coordinates = []
    player_pawn_coordinates = {PLAYER_1: player_1_pawn_coordinates, PLAYER_2: player_2_pawn_coordinates}
    last_player = None

    def __init__(self, row = 3, col = 3):
        """
        :param row:
        :param col:
        """
        if row < 3 or col < 3: raise ValueError("Row or Column size can't be less than 3!")
        self.board = []
        self.row = row
        self.col = col

        self.resetBoard()

    def __repr__(self):
        self.print()
        return ""


    def resetBoard(self):
        self.board = []
        self.player_1_pawn_coordinates = []
        self.player_2_pawn_coordinates = []
        self.player_pawn_coordinates = {PLAYER_1: self.player_1_pawn_coordinates, PLAYER_2: self.player_2_pawn_coordinates}
        self.last_player = None
        for i in range(self.col):
            self.player_1_pawn_coordinates.append((0, i))
            self.player_2_pawn_coordinates.append((self.row - 1, i))

        row = []
        for i in range(self.col):
            row.append(PLAYER_1_PAWN)
        self.board.append(row)

        for i in range(1, self.row - 1):
            row = []
            for j in range(self.col):
                row.append(EMPTY_PAWN)
            self.board.append(row)

        row = []
        for i in range(self.col):
            row.append(PLAYER_2_PAWN)
        self.board.append(row)


    def checkCoordinateValidity(self, row, col):
        '''

        :param row:
        :param col:
        :return:
        '''
        log(CLASS_NAME + ": checkCoordinateValidity(): " + str(row) + ", " + str(col))
        if row < 0 or row >= self.row: raise ValueError("Row Range: 0 - " + str(self.row - 1)\
                                                        + "; You entered: " + str(row))
        if col < 0 or col >= self.col: raise ValueError("Column Range: 0 - " + str(self.col  - 1)\
                                                        + "; You entered: " + str(col))

    def pawn(self, row, col):
        '''

        :param row:
        :param col:
        :return:
        '''
        self.checkCoordinateValidity(row, col)
        return self.board[row][col]

    def moveType(self, current_row, current_col, final_row, final_col):
        '''

        :param current_row:
        :param current_col:
        :param final_row:
        :param final_col:
        :return:
        '''
        self.checkCoordinateValidity(current_row, current_col)
        self.checkCoordinateValidity(final_row, final_col)
        if current_row == final_row: raise InvalidMove("Can't move in same row!")
        if current_row == final_row + 1:
            if current_col == final_col:
                return UP
            if current_col == final_col + 1:
                return DIAGONAL_UP_LEFT
            return DIAGONAL_UP_RIGHT
        if current_row == final_row - 1:
            if current_col == final_col:
                return DOWN
            if current_col == final_col + 1:
                return DIAGONAL_DOWN_LEFT
            return DIAGONAL_DOWN_RIGHT

    def __movePawn(self, player, current_row, current_col, final_row, final_col):
        '''

        :param player:
        :param current_row:
        :param current_col:
        :param final_row:
        :param final_col:
        :return:
        '''
        self.checkCoordinateValidity(current_row, current_col)
        self.checkCoordinateValidity(final_row, final_col)
        if self.pawn(final_row, final_col) != EMPTY_PAWN:
            if player == PLAYER_1:
                self.player_pawn_coordinates[PLAYER_2].remove((final_row, final_col))
            if player == PLAYER_2:
                self.player_pawn_coordinates[PLAYER_1].remove((final_row, final_col))
        self.board[current_row][current_col] = EMPTY_PAWN
        self.board[final_row][final_col] = PLAYER_PAWN[player]
        self.player_pawn_coordinates[player].remove((current_row, current_col))
        self.player_pawn_coordinates[player].append((final_row, final_col))


    def checkPlayerValidity(self, player):
        '''

        :param player:
        :return:
        '''
        if player not in PLAYERS: raise ValueError("Acceptable Player: " + str(PLAYERS))

    def finalCoordinateForMove(self, player, row, col, move):
        '''

        :param player:
        :param row:
        :param col:
        :param move:
        :return:
        '''
        log(CLASS_NAME + ": finalCoordinateForMove()")
        log ("Initial: " + str(row) + ", " + str(col) + "; Move: " + MOVE_NAMES[move])
        self.checkPlayerValidity(player)
        self.checkCoordinateValidity(row, col)
        self.checkPlayerMoveValidity(player, move)

        if move == UP:
            final_row, final_col = (row - 1, col)
        elif move == DOWN:
            final_row, final_col = (row + 1, col)
        elif move == DIAGONAL_UP_LEFT:
            final_row, final_col = (row - 1, col - 1)
        elif move == DIAGONAL_UP_RIGHT:
            final_row, final_col = (row - 1, col + 1)
        elif move == DIAGONAL_DOWN_LEFT:
            final_row, final_col = (row + 1, col - 1)
        elif move == DIAGONAL_DOWN_RIGHT:
            final_row, final_col = (row + 1, col + 1)

        return final_row, final_col

    def checkMoveValidity(self,  player, move, row = 1, col = 1):
        '''

        :param player:
        :param move:
        :param row:
        :param col:
        :return:
        '''
        log("checkMoveValidity()")
        log("Initial: " + str(row) + "," + str(col) + "; Move: " + MOVE_NAMES[move])

        final_row, final_col = self.finalCoordinateForMove(player, row, col, move)
        log("Final:" + str(final_row) + "," + str(final_col))
        final_coordinate_piece = self.pawn(final_row, final_col)

        self.checkCoordinateValidity(final_row, final_col)

        if move not in VALID_MOVES:
            raise InvalidMove("Entered move is not acceptable in Hexapawn!")
        if move in UPWARD_MOVES and row == 0: raise InvalidMove("Upward move is not valid from row 0!")
        if move in DOWNWARD_MOVES and row == self.row - 1:
            raise InvalidMove("Downward move is not valid from row " + str(self.row - 1) + "!")
        if move in LEFTWARD_MOVES and col == 0: raise InvalidMove("Leftward move is not valid from column 0!")
        if move in RIGHTWARD_MOVES and col == self.col - 1:
            raise InvalidMove("Rightward move is not valid from column " + str(self.col - 1) + "!")

        if move in (UP, DOWN):
            if final_coordinate_piece != EMPTY_PAWN:
                raise InvalidMove("Pawn can't move forward if target location is occupied!")
        elif move in (DIAGONAL_UP_LEFT, DIAGONAL_UP_RIGHT, DIAGONAL_DOWN_RIGHT, DIAGONAL_DOWN_LEFT):
            if final_coordinate_piece not in PLAYER_PAWN[otherPlayer(player)]:
                raise InvalidMove("Pawn can move diagonally only to strike out opponent's pawn!")

    def checkPlayerMoveValidity(self, player, move):
        '''

        :param player:
        :param move:
        :return:
        '''
        if move not in PLAYER_VALID_MOVES[player]: raise InvalidMove(MOVE_NAMES[move] + " is invalid move for your Pawn!")


    def checkPlayerPawnValidity(self, player, row, col):
        '''

        :param player:
        :param row:
        :param col:
        :return:
        '''
        if self.pawn(row, col) != PLAYER_PAWN[player]:
            raise InvalidPlayer("Player Pawn is not at given location!")


    def validMovesForPawn(self, player, row, col):
        '''

        :param player:
        :param row:
        :param col:
        :return:
        '''
        log(CLASS_NAME + ": validMovesForPawn()")

        self.checkPlayerValidity(player)
        self.checkCoordinateValidity(row, col)
        self.checkPlayerPawnValidity(player, row, col)
        valid_moves = []
        for move in PLAYER_VALID_MOVES[player]:
            try:
                self.checkMoveValidity(player, move, row, col)
                valid_moves.append(move)
            except Exception as e:
                log(str(move) + ": " + str(e))
        log("Valid Moves" + str(valid_moves))
        if len(valid_moves) != 0: return valid_moves

    def validMoves(self, player):
        '''

        :param player:
        :return: [(row, col, move)]
        '''
        log("validMoves():")
        self.checkPlayerValidity(player)
        valid_moves = []
        for row, col in self.player_pawn_coordinates[player]:
            log("Pawn:" + str(row) + "," + str(col))
            moves = self.validMovesForPawn(player, row, col)
            if moves is not None:
                for move in moves:
                    valid_moves.append((row, col, move))
        return valid_moves

    def opponentMovesBlocked(self):
        log(CLASS_NAME + " :opponentMovesBlocked()")
        log("Last Player: " + str(self.last_player))
        player = otherPlayer(self.last_player)
        valid_moves = self.validMoves(player)
        log("Valid Moves Count: " + str(len(valid_moves)))
        return len(valid_moves) == 0

    def winner(self):
        if self.last_player is None:
            return None
        opponent = otherPlayer(self.last_player)

        # any pawn reached opponent border
        for row, col in self.player_pawn_coordinates[self.last_player]:
            self.checkPlayerPawnValidity(self.last_player, row, col)
            if self.last_player == PLAYER_1 and row == self.row - 1:
                return PLAYER_1
            if self.last_player == PLAYER_2 and row == 0:
                return PLAYER_2

        # opponent all pawns killed or not
        if len(self.player_pawn_coordinates[opponent]) == 0: # killed
            return self.last_player

        # blocked all move for opponent
        if self.opponentMovesBlocked():
            return self.last_player

    def move(self, player, current_row, current_col, move_type):
        '''

        :param player:
        :param current_row:
        :param current_col:
        :param move_type:
        :return:
        '''
        self.checkPlayerMoveValidity(player, move_type)
        self.checkPlayerPawnValidity(player, current_row, current_col)
        self.checkMoveValidity(player, move_type, current_row, current_col)
        self.checkPlayerValidity(player)
        final_row, final_col = self.finalCoordinateForMove(player, current_row, current_col, move_type)
        self.move(player, current_row, current_col, final_row, final_col)


    def move(self, player, current_row, current_col, final_row, final_col):
        """
        :param player:
        :param current_row:
        :param current_col:
        :param final_row:
        :param final_col:
        :raises Invalid
        """
        log(CLASS_NAME + ": move()")
        self.checkPlayerValidity(player)
        self.checkCoordinateValidity(current_row, current_col)
        self.checkCoordinateValidity(final_row, final_col)
        self.checkPlayerPawnValidity(player, current_row, current_col)
        move_type = self.moveType(current_row, current_col, final_row, final_col)
        self.checkPlayerMoveValidity(player, move_type)
        self.checkMoveValidity(player, move_type, current_row, current_col)

        self.__movePawn(player, current_row, current_col, final_row, final_col)
        log("move(); Current Player: " + str(player))
        self.last_player = player
        log("move(); Last Player: " + str(self.last_player))


    def rowSeperatorString(self):
        row = ""
        for i in range((self.col + 1) * 4 + 1):
            row = row + ROW_SEPERATOR
        row = row + "\n"
        return row

    def print(self):
        """
        Prints board on command line.
        """
        print(self.rowSeperatorString(), end = "")
        print(COL_SEPERATOR + Style.DIM + " * " + Style.RESET_ALL, end = "")
        for i in range(self.col):
            print( COL_SEPERATOR + " " + INDEX_COLOR + str(i) + Style.RESET_ALL + " ", end = "")
        print(COL_SEPERATOR + "\n", end = "")
        print(self.rowSeperatorString(), end = "")

        for i in range(self.row):
            print(COL_SEPERATOR + " " + INDEX_COLOR + str(i) + Style.RESET_ALL + " ", end = "")
            for j in range(self.col):
                print(COL_SEPERATOR + " " + str(self.board[i][j]) + " ", end = "")
            print(COL_SEPERATOR + "\n", end = "")
            print(self.rowSeperatorString(), end = "")
    

