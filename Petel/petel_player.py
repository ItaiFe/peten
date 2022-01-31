import socket
import pickle
import random


class PetelPlayer:
    def __init__(self, ip, port, side):
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
        self.s.connect((ip, port))

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


def runPetel(ip="127.0.0.1", port=5000, side="A"):
    petel = PetelPlayer(ip, port, side)
    print(petel.recieve())
    petel.send_ack()
    print(petel.recieve())
    petel.send_board()
    current_board = []
    while True:

        to_pickle = get_next_turn(petel)
        print(to_pickle)
        if to_pickle == "victory":
            print("You won!")
            return
        if to_pickle == "loser":
            print("You lost!")
            return
        elif to_pickle == "change_weapon":
            print("change weapon")
            petel.send_change_weapon(random.randint(1, 3))
            continue
        elif to_pickle == "bad":
            print("bad move")
            do_next_move(petel, current_board, side)
            continue
        elif to_pickle == ["illegal"]:
            print("illegal action")
            continue
        elif to_pickle == "turn":
            print("my turn")
            print(current_board)
            do_next_move(petel, current_board, side)
            continue
        else:
            to_pickle = pickle.loads(to_pickle)[1]
            current_board = to_pickle
        print_board = ""
        for row in to_pickle:
                print(row)
                for pawn in row:
                    print(pawn)
                    print_board += " [{weapon}] ".format(
                        weapon=[pawn[0], pawn[1]])
                print_board += "\n\n"
        print(print_board)
        petel.send_ack()
        print(petel.recieve())
        do_next_move(petel, current_board, side)


def do_next_move(petel, board, side):
    for row in board:
        for pawn in row:
            source = [pawn[3][0], pawn[3][1]]
            if pawn[1] == 5 or pawn[1] == 4:
                continue
            if side == "A":
                if pawn[2] == "A":
                    dest = generate_next_step(source)
                    print(board, dest)
                    if board[dest[0]][dest[1]][2] == side:
                        continue
                    print("move")
                    print([pawn[0], source , dest])    
                    petel.send_move(pawn[0], source , dest)
                    return
            else:
                if pawn[2] == "B":
                    dest = generate_next_step(source)
                    if board[dest[0]][dest[1]][2] == side:
                        continue
                    print("move")
                    print([pawn[0], source , dest])     
                    petel.send_move(pawn[0], source , dest)
                    return

def generate_next_step(source):
    x = source[0] + random.randint(-1,1)
    y = source[1] + random.randint(-1,1)
    if x > 5:
        x = 5
    if y > 6:
        y = 6
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    return [x,y]

def get_next_turn(t):
    is_running = True
    while is_running:
        try:
            to_pickle = t.recieve()
        except Exception:
            continue
        is_running = False
    
    return to_pickle
