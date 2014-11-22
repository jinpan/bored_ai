from Queue import Empty
from Queue import Queue
from threading import Thread
from Tkinter import Tk, W, E, StringVar
from ttk import Frame, Button, Label, Style
from ttk import Entry

from strategy import AI_NAME
from tictactoe import Board
from strategy import get_best_move
from tictactoe import Move
from tictactoe import Piece
from tictactoe import PLAYER1
from tictactoe import PLAYER2


class TTTGui(Frame):

    def __init__(self, root, player=PLAYER1):
        Frame.__init__(self, root)

        self.root = root
        self.state = {
            'player': player,
            'opponent': PLAYER1 if player == PLAYER2 else PLAYER2,
            'board': Board(),
        }
        self.queue = Queue()

        self.initUI()

    def initUI(self):

        for idx in range(3):
            self.columnconfigure(idx, pad=3)
        for idx in range(4):
            self.rowconfigure(idx, pad=3)


        status_text = StringVar()
        def update_status():
            state = self.state['board'].get_state()
            if state[0] == 'PENDING':
                if self.state['board'].to_move() == self.state['player']:
                    status_text.set('Your Move')
                else:
                    status_text.set('%s is thinking...' % AI_NAME)
            elif state[0] == 'TIE':
                status_text.set('Tie game')
            else:
                status_text.set('%s wins' % state[1])

        status = Label(self, textvariable=status_text)
        status.grid(row=0, columnspan=3, sticky=W+E)
        update_status()

        button_texts = []
        for _ in range(9):
            button_texts.append(StringVar())

        def update_board(move):
            self.state['board'] = self.state['board'].add_move(move)

            for idx, text in zip(range(9), button_texts):
                row, col = idx/3, idx%3
                piece = self.state['board'].board[row][col]

                if piece is None:
                    text.set('')
                else:
                    text.set(piece.player)
            print move
            print self.state['board']

        def check_queue():
            try:
                move = self.queue.get(block=False)
            except Empty:
                self.root.after(100, check_queue)
                return

            update_board(move)

            row = move.piece.row
            col = move.piece.col
            update_status()
            text = button_texts[3 * row + col]
            text.set(move.player)
            print self.state['board']

        def get_next_move(state, queue):
            move = get_best_move(
                state['opponent'],
                state['player'],
                state['board']
            )
            queue.put(move)

        def btn_click(row, col):
            piece = Piece(self.state['player'], col=col, row=row)
            move = Move(piece)
            update_board(move)

            update_status()

            text = button_texts[3*row+col]
            text.set(self.state['player'])

            state = self.state['board'].get_state()
            if state[0] == 'PENDING':

                next_move_t = Thread(target=get_next_move,
                                     args=(self.state, self.queue))
                next_move_t.start()

                self.root.after(100, check_queue)

        buttons = []
        for idx, text in zip(range(9), button_texts):
            row = idx/3
            col = idx%3
            button = Button(
                self,
                textvariable=text,
                command=(lambda row=row, col=col: btn_click(row, col)),
            )
            button.grid(row=row+1, column=col)
            buttons.append(button)

        self.pack()

