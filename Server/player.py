import socket
import pickle


IP = "0.0.0.0"


class Player:

    def __init__(self, side, color, port):
        self.side = side
        self.color = color
        self.port = port
        self.ip = IP
        self.sock = None
        self.client_sock = None
        self.actions = {
            "move": self.move,
            "change": self.parse_change_weapon,
            "initialize": self.initialize_board
        }

    def _initialize_player_socket(self):
        print("initializing player socket")
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)
        self.sock.settimeout(10)
        self.client_sock, _ = self.sock.accept()

    def start_game(self):
        print("starting game")
        self._initialize_player_socket()
        print("sending player his side")
        self._send(["side", self.side])
        while self._recieve() != ["ack"]:
            pass
            

    def get_next_move(self):
        print("sending player his turn")
        self._send("turn")
        return self._parse_action(self._recieve())

    def get_initial_lineup(self):
        print("sending player to initialize board")
        self._send("initialize_board")
        return self._parse_action(self._recieve())

    def _send(self, data):
        self.client_sock.send(pickle.dumps(data))

    def _recieve(self):
        try:
            return pickle.loads(self.client_sock.recv(1024))
        except TimeoutError:
            return None

    def send_board(self, board):
        print("sending player the new board")
        self._send(pickle.dumps(["board", board.to_serializeable()]))

    def bad_move(self):
        print("sending player he did a illegal move")
        self._send("bad")

    def change_weapon(self):
        print("sending player to change weapon")
        self._send("change_weapon")
        return self._parse_action(self._recieve())

    def set_victory(self, is_victorious):
        if is_victorious:
            print("sending player he won")
            self._send("victory")
        else:
            print("sending player he lost")
            self._send("loser")

    def move(self, data):
        return data.remove(data[0])

    def parse_change_weapon(self, data):
        return data.remove(data[0])

    def initialize_board(self, data):
        return data[1]
    def _parse_action(self, data):
        if data is None:
            return data
        return self.actions[data[0]](data)
