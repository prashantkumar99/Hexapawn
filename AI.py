from Player import *
from Board import PLAYER_PAWN, EMPTY_PAWN
import random
from Log import log, error

PLAYER_TAG = 1
OPPONENT_TAG = -1
EMPTY_TAG = 0


CORRECT_MOVE = 1
UNCHECKED_MOVE = 0
INCORRECT_MOVE = -1

INTELLIGENCE_FILE_EXTENSION = '.ai'
INTELLIGENCE_FILE_HEADER = 'intelli'

'''
ai_moves = {board_state : moves, ...}
moves = {(row, col, move): tag, ...}
'''

CLASS_NAME = "AI"

class AI(Player):
    board = None
    player = None
    player_pawn = None
    opponent_pawn = None
    last_move = None
    last_board_state = None
    tage = None
    ai_moves = {}
    save_intelligence = True

    def __init__(self, name, player, board, intelligent = True,):
        '''

        :param name:
        :param player:
        :param board:
        :param intelligent:
        '''
        Player.__init__(self, name)
        self.board = board
        self.player = player
        self.player_pawn = PLAYER_PAWN[player]
        self.opponent_pawn = PLAYER_PAWN[otherPlayer(self.player)]
        self.tags = {self.player_pawn: PLAYER_TAG, self.opponent_pawn: OPPONENT_TAG, EMPTY_PAWN: EMPTY_TAG}
        self.save_intelligence = intelligent
        if intelligent:
            self.ai_moves = self.readIntelligence()

    def intelligenceFileName(self):
        '''
        :return: file name  intelli<row>x<col>.ai
        '''
        return INTELLIGENCE_FILE_HEADER + str(self.board.row) + 'x' + str(self.board.col) + INTELLIGENCE_FILE_EXTENSION

    def saveIntelligence(self):
        '''

        :return: saves intelligence file to intelli<row>x<col>.ai
        '''
        try:
            with open(self.intelligenceFileName(), 'w') as file:
                file.write(str(self.ai_moves))
        except Exception as e:
            error(str(e))
            raise Warning("Intelligence couldn't be saved.")
        pass

    def readIntelligence(self):
        '''
        and updates ai_moves
        :return:
        '''
        try:
            file_name = self.intelligenceFileName()
            with open(file_name, 'r') as file:
                intelligence = eval(file.readline())
        except:
            raise FileNotFoundError("Intelligence file named " + file_name + "not found.")
        return intelligence

    def boardState(self):
        '''
        :return: board state with tags
        '''
        log(CLASS_NAME + ": boardState()")
        board_state = ''
        for row in self.board.board:
            for col in row:
                board_state = board_state + str(self.tags[col])
        log("Returned board_state")
        return board_state

    def addBoardState(self):
        '''
        Algo: -
        1. check weather board state is present or not
        2. if present: return
        3. if not: add it
            a. get boardState()
            b. get board.validMoves()
            c. joint it in dict with UNCHECKED_MOVE
        adds new board state if not present
        '''
        log(CLASS_NAME + ": addBoardState()")
        board_state = self.boardState()
        if board_state not in self.ai_moves.keys():
            log("Adding board_state.")
            moves = {}
            valid_moves = self.board.validMoves(self.player)
            for move in valid_moves:
                moves[move] = UNCHECKED_MOVE
            self.ai_moves[board_state] = moves
            log("Added Moves: " + str(moves))

    def bestMove(self, board_state):
        '''
        Algo: -
        1. move with CORRECT_MOVE
        2. if CORRECT_MOVE not present
        3. return any with UNCHECKED_MOVE
        4. if UNCHECKED_MOVE not present
        5. return any from INCORRECT_MOVE
        :return: MOVE
        '''

        moves = self.ai_moves[board_state]
        correct_moves = []
        for move in moves:
            if moves[move] == CORRECT_MOVE:
                correct_moves.append(move)
        if len(correct_moves) > 0:
            return random.choice(correct_moves)

        unchecked_moves = []
        for move in moves:
            if moves[move] == UNCHECKED_MOVE:
                unchecked_moves.append(move)
        if len(unchecked_moves) > 0:
            return random.choice(unchecked_moves)

        incorrect_moves = []
        for move in moves:
            if moves[move] == INCORRECT_MOVE:
                incorrect_moves.append(move)
            return random.choice(incorrect_moves)


    def updateMove(self, board_state, move, tag):
        #updates move value
        self.ai_moves[board_state][move] = tag

    def move(self, row, col, move):
        self.board.checkCoordinateValidity(row, col)
        self.board.checkPlayerMoveValidity(self.player, move)
        return (row, col, move)

    def setLastState(self, board_state, last_move):
        self.last_board_state = board_state
        self.last_move = last_move

    def readMoveCoordinates(self):
        '''
        Alog:-
        1. Get board state
        2. if board state not present add it
        3. *Get all possible moves from ai_moves of current board state
        4. Get best move
        5. get final coordinate
        5. move it
        6. save last move
        :return: (row, col, final_row, final_col)
        '''
        log(str(CLASS_NAME) + ": readMoveCoordinates()")
        print("Playing:", self.name)
        board_state = self.boardState()
        self.addBoardState()
        best_move = self.bestMove(board_state)
        log("best_move = " + str(best_move))
        row, col, move_type = best_move

        print("Select Pawn:-")
        print("Row:", row)
        print("Column:", col)

        final_row, final_col = self.board.finalCoordinateForMove(self.player, row, col, move_type)
        self.setLastState(board_state, best_move)

        print("Select Position to move to:-")
        print("Row:", final_row)
        print("Column", final_col)

        return int(row), int(col), int(final_row), int(final_col)

    def result(self, won):
        if won == self.player:
            self.updateMove(self.last_board_state, self.last_move, CORRECT_MOVE)
        else:
            self.updateMove(self.last_board_state, self.last_move, INCORRECT_MOVE)

        if self.save_intelligence:
            self.saveIntelligence()


