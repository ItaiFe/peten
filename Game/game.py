import socket
from board import Board
import moves

IP = "localhost"
PORT = 8000
GOOD = True
BAD = False

class Game:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((IP, PORT))
        self.sock.listen(1)
        self.board = Board(6,7)
        self.good = []
        self.bad = []
        self.turn = None
    
    def start_game(self):
        self.sock.send(b"start")
        self.turn = GOOD
    
    def run_game(self):
        while True:
            if self.turn:
                self.do_next_move()
                self.update_board()

            else:
                self.get_enemy_move()
                self.update_board()
            self.check_win()
            self.is_my_turn()
    
    def do_next_move(self):
        pass

    def get_enemy_move(self):
        pass

    def update_board(self):
        pass

    def is_my_turn(self):
        pass

    def check_win():
        pass

    
