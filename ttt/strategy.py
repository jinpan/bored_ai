from random import choice

from tictactoe import Board
from tictactoe import Move
from tictactoe import Piece
from tictactoe import PLAYER1
from tictactoe import PLAYER2


AI_NAME = 'DEEP THOUGHT'

def get_best_move(player, opponent, board):
    moves = board.get_moves(player)
    return choice(moves)

