from copy import deepcopy


PLAYER1 = 'X'
PLAYER2 = 'O'

BOARD_WIDTH = 3
BOARD_HEIGHT = 3
WIN_LEN = 3


class IllegalMoveException(Exception):
    pass


class Board(object):

    def __init__(self):
        self.board = [([None] * BOARD_WIDTH) for _ in range(BOARD_HEIGHT)]
        self.history = []


    def __repr__(self):
        return str(self)


    def __str__(self):
        rows = ['']
        for row in self.board:
            rows.append(''.join(['_' if piece is None else str(piece)
                                 for piece in row]))
        return '\n'.join(rows)


    def get_state(self):
        '''
        Returns ('PENDING', None) if the game is playing
        Returns ('TIE', None) if the game is tied
        Returns ('WINNER', PLAYER1|PLAYER2) if there's a winner
        '''

        def check_winner(three):
            if all(three) and three[0].player==three[1].player==three[2].player:
                if three[0].player == PLAYER1:
                    return ('WINNER', PLAYER1)
                else:
                    return ('WINNER', PLAYER2)

            return None

        # Check the rows
        for row in self.board:
            result = check_winner(row)
            if result is not None:
                return result

        # Check the columns
        for idx in range(BOARD_WIDTH):
            result = check_winner([self.board[0][idx],
                                   self.board[1][idx],
                                   self.board[2][idx]])
            if result is not None:
                return result

        # Check the diagonals
        result = check_winner([self.board[idx][idx]
                               for idx in range(WIN_LEN)])
        if result is not None:
            return result
        result = check_winner([self.board[BOARD_HEIGHT-idx-1][idx]
                               for idx in range(WIN_LEN)])
        if result is not None:
            return result

        # Check for tie game
        if all(x for y in self.board for x in y):
            return ('TIE', None)

        # Otherwise, return pending
        return ('PENDING', None)


    def get_moves(self, player):
        '''
        returns a list of possible moves
        '''
        if len(self.history) % 2 and player == PLAYER1:
            return []

        retval = []
        for idx in range(9):
            row, col = idx/3, idx%3
            if self.board[row][col] is None:
                retval.append(Move(Piece(player, row=row, col=col)))
        return retval


    def can_move(self, move):
        # Check that the player isn't executing out of turn
        if len(self.history) % 2 and move.player == PLAYER1:
            return False
        # Check that the location is still available
        return self.board[move.piece.row][move.piece.col] is None


    def add_move(self, move):
        '''
        Tries to execute the move.  Raises IllegalMoveException if
        the move is illegal
        '''
        if self.can_move(move):
            new_board = deepcopy(self)
            new_board.history.append(move)
            new_board.board[move.piece.row][move.piece.col] = move.piece
            return new_board
        else:
            raise IllegalMoveException

    def to_move(self):
        if len(self.history) % 2:
            return PLAYER2
        else:
            return PLAYER1

class Move(object):

    def __init__(self, piece, state=None):
        self.player = piece.player
        self.piece = piece
        self.state = state


    def __repr__(self):
        return str(self)


    def __str__(self):
        return '%s %d %d' % (self.player, self.piece.col, self.piece.row)


class Piece(object):

    def __init__(self, player, col, row):
        self.player = player

        if type(row) != int or type(col) != int:
            raise IllegalMoveException
        if row >= BOARD_WIDTH or row < 0:
            raise IllegalMoveException
        if col >= BOARD_HEIGHT or col < 0:
            raise IllegalMoveException

        self.row = row
        self.col = col


    def __str__(self):
        return self.player

