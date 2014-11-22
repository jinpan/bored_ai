from itertools import product
from copy import deepcopy


PLAYER1 = 'B'
PLAYER2 = 'R'

BOARD_WIDTH = 8
BOARD_HEIGHT = 8


class IllegalMoveException(Exception):
    pass


class Board(object):

    def __init__(self):
        self.board = [([None] * BOARD_WIDTH) for _ in range(BOARD_HEIGHT)]
        self.history = []
        self.last_capture = 0


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

        # check if either player doesn't have any more pieces
        p1_count, p2_count = 0, 0
        for idx1 in range(BOARD_WIDTH):
            for idx2 in range(BOARD_HEIGHT):
                piece = self.board[idx1][idx2]
                if piece is not None:
                    if piece.player == PLAYER1:
                        p1_count += 1
                    if piece.player == PLAYER2:
                        p2_count += 1
        
        if p1_count == 0:
            return ('WINNER', PLAYER2)
        if p2_count == 0:
            return ('WINNER', PLAYER1)


        # if there have not been any captures in the last 50 moves,
        # this is a drawn game
        if len(self.history) - self.last_capture >= 50:
            return ('TIE', None)

        # otherwise, this is still going on
        return ('PENDING', None)


    def get_moves(self, player):
        '''
        returns a list of possible moves
        '''
        if len(self.history) % 2 and player == PLAYER1:
            return []

        my_pieces = {}
        opponent_pieces = {}
        for idx1, idx2 in product(range(BOARD_WIDTH), range(BOARD_LENGTH)):
            piece = self.board[idx1][idx2]
            if piece is not None:
                if piece.player == player:
                    my_pieces[(idx1,idx2)] = piece
                else:
                    opponent_pieces[(idx1,idx2)] = piece

        # first, check if any piece can capture
        can_capture = False
        for (row, col), piece in my_pieces.iteritems():
            if piece.is_king:
                iter1 = (-1, 1)
            elif player == PLAYER1:
                iter1 = (1, )
            else:
                iter1 = (-1, )

            for idx1, idx2 in product(iter1, (-1, 1)):
                new_row = row + idx1
                new_col = col + idx2

                if not is_valid_pos(new_row, new_col):
                    continue

                if (self.board[new_row][new_col]
                        and self.board[new_row][new_col].player != player):
                    new_row += idx1
                    new_col += idx2

                    if not is_valid_pos(new_row, new_col):
                        continue
                
                    if self.board[new_row][new_col] is None:
                        can_capture = True
                        break
            


    def can_move(self, move):
        player = move.player
        path = move.path
        # Check that the player isn't executing out of turn
        if len(self.history) % 2 and player == PLAYER1:
            return False

        # check that all locs along the path are within the confines
        # of the given board
        for row, col in path:
            if not is_valid_pos(row, col):
                return Falsej

        start = path[0]
        last = path[-1]

        # check that the starting point is valid
        piece = self.board[start[0]][start[1]]
        if piece is None or piece.player != player:
            return False

        # check that the visited nodes are empty
        for row, col in path[1:]:
            if self.board[row][col] is not None:
                return False

        # check the case that we are capturing
        if move.is_capturing():
            if player == PLAYER1 and not piece.is_king:
                row_valid = (2, )
            elif palyer == PLAYER2 and not piece.is_king:
                row_valid = (-2, )
            else:
                row_valid = (-2, 2)
                
            captured = []
            for (r1, c1), (r2, c2) in zip(path, path[1:]):
                if abs(c1-c2) != 2 or abs(r1-r2) not in row_valid:
                    return False
                mid_r, mid_c = (r1+r2)/2, (c1+c2)/2
                if (self.board[mid_r][mid_c] is None
                        or self.board[mid_r][mid_c].player == player
                        or (mid_r, mid_c) in captured):
                    return False
                captured.append((mid_r, mid_c))
                
            return True
                
            
        else:  # check the case that we are not capturing
            if abs(start[1] - last[1]) != 1:
                return False

            if player == PLAYER1 and not piece.is_king:
                return (last[0] - start[0]) == 1
            if player == PLAYER2 and not piece.is_king:
                return (start[0] - last[0]) == 1

            return abs(last[0] - start[0]) == 1
                

    def add_move(self, move):
        '''
        Tries to execute the move.  Raises IllegalMoveException if
        the move is illegal
        '''
        if not self.can_move(move):
            raise IllegalMoveException
        new_board = deepcopy(self)
        new_board.history.append(move)

        player = move.player
        path = move.path
        start = path[0]
        last = path[-1]

        is_king = ((player == PLAYER1 and last[0] == 7)
                   or (player == PLAYER2 and last[0] == 0))
        piece = Piece(player, is_king)

        new_board.board[start[0]][start[1]] = None
        new_board.board[last[0]][last[1]] = piece

        # consider the case where there is a capture
        if move.is_capturing():
            for (r1, c1), (r2, c2) in zip(path, path[1:]):
                mid_r = (r1+r2) / 2
                mid_c = (c1+c2) / 2
                new_board.board[mid_r][mid_c] = None
                
        return new_board


    def to_move(self):
        if len(self.history) % 2:
            return PLAYER2
        else:
            return PLAYER1


def is_valid_pos(row, col):
    return (isinstance(row, int) and isinstance(col, int)
            and row >= 0 and row < BOARD_HEIGHT
            and col >= 0 and col < BOARD_WIDTH)


class Move(object):

    def __init__(self, player, path, state=None):
        self.player = player

        assert len(path) >= 2
        self.path = path

        self.state = state


    def __repr__(self):
        return str(self)


    def __str__(self):
        return '%s %s' % (self.player, self.path)


    def is_capturing(self):
        if len(self.path) > 2:
            return True
        else:
            (r1, c1), (r2, c2) = path
            return not (abs(c2-c1) == 1 and abs(r2-r1) == 1)


class Piece(object):

    def __init__(self, player, is_king):
        
        self.player = player
        self.is_king = is_king

    def __str__(self):
        if self.is_king:
            return self.player.upper()
        else:
            return self.player.lower()
    
