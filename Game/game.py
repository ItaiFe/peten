import socket
from board import Board

IP = "192.168.1.1"
PORT = 8000
GOOD = True
BAD = False

class Game:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((IP, PORT))
        self.board = Board(6,7)
        self.good = []
        self.bad = []
        self.turn = None
    
    def start_game():
        self.sock.send(b"start")
        self.turn = GOOD
    
    def run_game():
        while True:
            if self.turn:
                self.do_next_move()
                self.update_board()

            else:
                self.get_enemy_move()
                self.update_board()
            self.check_win()
            self.is_my_turn()
    
    def do_next_move():
        pass

    def get_enemy_move():
        pass

    def update_board():
        pass

    def is_my_turn():
        pass

    def check_win():
        pass

    
