import socket
import pickle
import random


class PetelPlayer:
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

    def recieve(self):
        return pickle.loads(self.s.recv(1024))

    def send_ack(self):
        self.s.send(pickle.dumps(["ack"]))

    def send_board(self):
        self.s.send(pickle.dumps(["initialize", self.board]))

    def send_move(self, id, source, dest):
        self.s.send(pickle.dumps(["move", id, source, dest]))
    
    def send_change_weapon(self, weapon):
        self.s.send(pickle.dumps(["change", weapon]))

    def kill(self):
        self.s.close()


def runPetel():
    petel = PetelPlayer(5000, "A")
    print(petel.recieve())
    petel.send_ack()
    print(petel.recieve())
    petel.send_board()

    while True:
        to_pickle = get_next_turn(petel)
        print(to_pickle)
        if to_pickle == "victory":
            print("You won!")
            return
        elif to_pickle == "change_weapon":
            petel.send_change_weapon(1)
            continue
        else:
            to_pickle = pickle.loads(to_pickle)[1]
            print(to_pickle)
        board = ""
        for row in to_pickle:
                print(row)
                for pawn in row:
                    print(pawn)
                    board += " [{weapon}] ".format(weapon=[pawn[0], pawn[1]])
                board += "\n\n"
        print(board)
        petel.send_ack()
        print(petel.recieve())
        do_next_move(petel, to_pickle)

def do_next_move(petel, board):
    for row in board:
        for pawn in row:
            source = [pawn[3][0], pawn[3][1]]
            if pawn[0] == 5 or pawn[0] == 4:
                continue
            if pawn[2] == "A" and board[source[0]+1][source[1]][2] != "A":
                petel.send_move(pawn[0], source , [source[0] +1, source[1]])
                return



def get_next_turn(t):
    is_running = True
    while is_running:
        try:
            to_pickle = t.recieve()
        except Exception:
            continue
        is_running = False
    
    return to_pickle
