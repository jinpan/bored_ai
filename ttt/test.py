from random import choice
from sys import argv

from strategy import get_best_move
from tictactoe import Board
from tictactoe import Move
from tictactoe import PLAYER1
from tictactoe import PLAYER2
from tictactoe import Piece


def run_gui():
    from Tkinter import Tk
    from gui import TTTGui

    root = Tk()
    app = TTTGui(root)
    root.mainloop()


def check_over(board):
    print board
    state, winner = board.get_state()
    if state == 'WINNER':
        print state, winner
        return True
    elif state == 'TIE':
        print state
        return True
    return False


if __name__ == '__main__':
    if len(argv) > 1 and argv[1] == '--nogui':
        board = Board()
        print board
        print '\n---'

        while True:
            i, j = map(int, raw_input().split(' '))
            board = board.add_move(Move(Piece(PLAYER1, col=i, row=j)))
            if check_over(board):
                break
            print '\n---'

            move = get_best_move(PLAYER2, PLAYER1, board)
            board = board.add_move(move)
            if check_over(board):
                break
            print '\n---'

    elif len(argv) > 1 and argv[1] == 'auto':
        iterations = int(argv[2])
        for _ in range(iterations):
            board = Board()
            smart = choice([PLAYER1, PLAYER2])
            to_move = PLAYER1
            not_to_move = PLAYER2

            while board.get_state()[0] == 'PENDING':
                if smart == to_move:
                    move = get_best_move(to_move, not_to_move, board)
                    board = board.add_move(move)
                else:
                    move = choice(board.get_moves(to_move))
                    board = board.add_move(move)

                to_move, not_to_move = not_to_move, to_move

            final_state = board.get_state()
            if final_state[0] == 'TIE':
                print _, 'TIE'
            else:
                print _, 'WIN', smart == final_state[1], final_state


    else:
        run_gui()

