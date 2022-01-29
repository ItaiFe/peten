from board import Board
from player import Player

PLAYER_A = "A"
PLAYER_B = "B"
BAD_MOVE = "xxx"
BOARD_WIDTH = 7
BOARD_HEIGHT = 6


class Game:
    def __init__(self):
        self.players = [Player(PLAYER_A, "red", 5000),
                        Player(PLAYER_B, "blue", 5001)]
        self.board = Board(BOARD_HEIGHT, BOARD_WIDTH)
        self.winner = None

    def initialize_player_pawns(self, player):
        player_pawns = player.get_initial_lineup()
        for pawn in player_pawns:
            self.board.set_board(pawn, pawn.location)

    def initialize_game(self):
        for player in self.players:
            self.initialize_player_pawns(player)

    def run_game(self):
        while not self.check_win():
            for player in self.players:
                player.send_board(self.board)
                move = player.get_next_move()
                self.update_board(player, move)

        for player in self.players:
            if player is self.winner:
                player.set_victory(True)
            else:
                player.set_victory(False)

    def update_board(self, player, player_move):
        move = player_move
        while not self.board.check_move(move):
            player.bad_move()
            move = player.get_next_move()

        if self.board.check_fight(move):
            self.board.fight(self.players, move)

    def check_win(self):
        self.winner = self.board.check_flag(self.players)

