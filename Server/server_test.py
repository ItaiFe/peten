import socket
import pickle
import random


class Test:
    def __init__(self, port, side):
        if side == "A":
            self.board = [[[random.randint(1, 3) if i < 2 else 0, [
                i, j]] for j in range(7)] for i in range(6)]
            self.board[0][3] = [5, [0, 3]]
            self.board[1][3] = [4, [1, 3]]
        else:
            self.board = [[[random.randint(1, 3) if i > 3 else 0, [
                i, j]] for j in range(7)] for i in range(6)]
            self.board[5][3] = [5, [5, 3]]
            self.board[4][3] = [4, [4, 3]]

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", port))
        self.s.settimeout(15)

    def recieve(self):
        return pickle.loads(self.s.recv(1024))

    def send_ack(self):
        self.s.send(pickle.dumps(["ack"]))

    def send_board(self):
        self.s.send(pickle.dumps(["initialize", self.board]))

    def send_move(self, id, source, dest):
        self.s.send(pickle.dumps(["move", id, source, dest]))

    def kill(self):
        self.s.close()
